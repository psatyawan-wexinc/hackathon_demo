#!/usr/bin/env python3
"""
Format and Lint Hook

This hook automatically formats and lints Python code after file modifications.
It focuses on critical issues and provides intelligent feedback to improve
code quality while avoiding overwhelming users with minor style issues.

Hook Type: PostToolUse
Trigger: After Write/Edit operations on Python files
"""

import os
import json
import sys
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add hooks utils to path
hooks_dir = Path(__file__).parent
sys.path.insert(0, str(hooks_dir))

from utils.file_utils import (
    get_use_case_root,
    is_python_file,
    get_relative_path
)


def should_format_and_lint(file_path: str, tool: str) -> bool:
    """
    Determine if we should format and lint the given file.
    
    Args:
        file_path: Path to the file that was written/edited
        tool: The tool that was used (Write/Edit)
        
    Returns:
        True if formatting and linting should be performed
    """
    # Only process Write and Edit operations
    if tool not in ["Write", "Edit"]:
        return False
    
    # Only process Python files
    if not is_python_file(file_path):
        return False
    
    # Skip hook files to avoid recursive issues
    if "/.claude/hooks/" in file_path:
        return False
    
    # Skip __init__.py files if they're very small
    if file_path.endswith("__init__.py"):
        try:
            with open(file_path, 'r') as f:
                content = f.read().strip()
                # Skip if it's just docstring or imports
                if len(content.split('\n')) < 5:
                    return False
        except Exception:
            return False
    
    # Only process files in the use-case directory
    use_case_root = get_use_case_root()
    if use_case_root and use_case_root not in file_path:
        return False
    
    return True


def check_tool_availability() -> Dict[str, bool]:
    """
    Check which formatting and linting tools are available.
    
    Returns:
        Dictionary mapping tool names to availability
    """
    tools = {}
    
    # Formatting tools
    for tool in ["black", "autopep8", "ruff"]:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True, timeout=5)
            tools[tool] = True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            tools[tool] = False
    
    # Linting tools
    for tool in ["flake8", "pylint", "pycodestyle", "mypy"]:
        try:
            subprocess.run([tool, "--version"], capture_output=True, check=True, timeout=5)
            tools[tool] = True
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            tools[tool] = False
    
    # Special case for ruff (can do both formatting and linting)
    if tools.get("ruff", False):
        tools["ruff_format"] = True
        tools["ruff_check"] = True
    
    return tools


def format_file(file_path: str, available_tools: Dict[str, bool]) -> Dict:
    """
    Format the Python file using available formatting tools.
    
    Args:
        file_path: Path to the file to format
        available_tools: Dictionary of available tools
        
    Returns:
        Dictionary with formatting results
    """
    results = {
        "formatted": False,
        "tool_used": None,
        "changes_made": False,
        "errors": []
    }
    
    try:
        # Read original file content
        with open(file_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
        
        # Determine which formatter to use (in order of preference)
        formatter = None
        if available_tools.get("ruff", False):
            formatter = "ruff"
        elif available_tools.get("black", False):
            formatter = "black"
        elif available_tools.get("autopep8", False):
            formatter = "autopep8"
        
        if not formatter:
            results["errors"].append("No formatting tools available")
            return results
        
        # Create a temporary file for formatting
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(original_content)
            temp_path = temp_file.name
        
        try:
            # Run the formatter
            if formatter == "ruff":
                # Use ruff format
                cmd = ["ruff", "format", "--stdin-filename", file_path]
                process = subprocess.run(
                    cmd,
                    input=original_content,
                    text=True,
                    capture_output=True,
                    timeout=30
                )
                if process.returncode == 0:
                    formatted_content = process.stdout
                else:
                    results["errors"].append(f"Ruff formatting failed: {process.stderr}")
                    return results
            
            elif formatter == "black":
                # Use black
                cmd = ["black", "--quiet", "--code", original_content]
                process = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if process.returncode == 0:
                    formatted_content = process.stdout
                else:
                    results["errors"].append(f"Black formatting failed: {process.stderr}")
                    return results
            
            elif formatter == "autopep8":
                # Use autopep8
                cmd = ["autopep8", "--aggressive", "--aggressive", "-"]
                process = subprocess.run(
                    cmd,
                    input=original_content,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if process.returncode == 0:
                    formatted_content = process.stdout
                else:
                    results["errors"].append(f"Autopep8 formatting failed: {process.stderr}")
                    return results
            
            # Check if content was actually changed
            if formatted_content != original_content:
                # Write the formatted content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(formatted_content)
                
                results["changes_made"] = True
            
            results["formatted"] = True
            results["tool_used"] = formatter
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    except Exception as e:
        results["errors"].append(f"Formatting error: {str(e)}")
    
    return results


def lint_file(file_path: str, available_tools: Dict[str, bool]) -> Dict:
    """
    Lint the Python file using available linting tools.
    
    Args:
        file_path: Path to the file to lint
        available_tools: Dictionary of available tools
        
    Returns:
        Dictionary with linting results
    """
    results = {
        "linted": False,
        "tool_used": None,
        "issues": [],
        "critical_issues": 0,
        "warning_issues": 0,
        "style_issues": 0,
        "errors": []
    }
    
    try:
        # Determine which linter to use (in order of preference)
        linter = None
        if available_tools.get("ruff", False):
            linter = "ruff"
        elif available_tools.get("flake8", False):
            linter = "flake8"
        elif available_tools.get("pycodestyle", False):
            linter = "pycodestyle"
        
        if not linter:
            results["errors"].append("No linting tools available")
            return results
        
        # Run the linter
        if linter == "ruff":
            cmd = ["ruff", "check", "--output-format", "json", file_path]
        elif linter == "flake8":
            cmd = ["flake8", "--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s", file_path]
        elif linter == "pycodestyle":
            cmd = ["pycodestyle", "--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s", file_path]
        
        process = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Parse results based on tool
        if linter == "ruff" and process.stdout.strip():
            try:
                import json as json_module
                ruff_results = json_module.loads(process.stdout)
                for issue in ruff_results:
                    severity = categorize_issue_severity(issue.get("code", ""), issue.get("message", ""))
                    results["issues"].append({
                        "line": issue.get("location", {}).get("row", 0),
                        "column": issue.get("location", {}).get("column", 0),
                        "code": issue.get("code", ""),
                        "message": issue.get("message", ""),
                        "severity": severity
                    })
                    
                    if severity == "critical":
                        results["critical_issues"] += 1
                    elif severity == "warning":
                        results["warning_issues"] += 1
                    else:
                        results["style_issues"] += 1
            except Exception as e:
                results["errors"].append(f"Error parsing ruff output: {str(e)}")
        
        elif process.stdout.strip():
            # Parse flake8/pycodestyle output
            for line in process.stdout.strip().split('\n'):
                if ':' in line:
                    try:
                        # Parse format: path:line:col: code message
                        parts = line.split(':', 3)
                        if len(parts) >= 4:
                            line_num = int(parts[1])
                            col_num = int(parts[2])
                            code_message = parts[3].strip()
                            
                            # Extract code and message
                            if ' ' in code_message:
                                code, message = code_message.split(' ', 1)
                            else:
                                code, message = code_message, ""
                            
                            severity = categorize_issue_severity(code, message)
                            results["issues"].append({
                                "line": line_num,
                                "column": col_num,
                                "code": code,
                                "message": message,
                                "severity": severity
                            })
                            
                            if severity == "critical":
                                results["critical_issues"] += 1
                            elif severity == "warning":
                                results["warning_issues"] += 1
                            else:
                                results["style_issues"] += 1
                    except (ValueError, IndexError):
                        continue
        
        results["linted"] = True
        results["tool_used"] = linter
        
    except Exception as e:
        results["errors"].append(f"Linting error: {str(e)}")
    
    return results


def categorize_issue_severity(code: str, message: str) -> str:
    """
    Categorize the severity of a linting issue.
    
    Args:
        code: Error/warning code
        message: Error/warning message
        
    Returns:
        Severity level: "critical", "warning", or "style"
    """
    critical_patterns = [
        "F", "E9",  # Flake8 syntax errors and runtime errors
        "SIM", "C90",  # Complexity issues
        "B", "S",  # Security and bug issues
        "undefined", "not defined", "imported but unused",
        "syntax error", "indentation"
    ]
    
    warning_patterns = [
        "W", "N", "D",  # Warning, naming, docstring issues
        "E1", "E2", "E3", "E4", "E5", "E7",  # Various error types
        "unused variable", "too many", "too complex"
    ]
    
    code_upper = code.upper()
    message_lower = message.lower()
    
    # Check for critical issues
    for pattern in critical_patterns:
        if pattern in code_upper or pattern in message_lower:
            return "critical"
    
    # Check for warning issues
    for pattern in warning_patterns:
        if pattern in code_upper or pattern in message_lower:
            return "warning"
    
    # Everything else is style
    return "style"


def generate_feedback_message(format_results: Dict, lint_results: Dict, file_path: str) -> str:
    """
    Generate a feedback message about formatting and linting results.
    
    Args:
        format_results: Formatting results
        lint_results: Linting results
        file_path: Path to the processed file
        
    Returns:
        Formatted feedback message
    """
    lines = []
    
    use_case_root = get_use_case_root()
    relative_path = get_relative_path(file_path, use_case_root)
    
    # Header
    lines.append(f"🔧 CODE QUALITY CHECK: {relative_path}")
    lines.append("=" * 50)
    
    # Formatting results
    if format_results.get("formatted", False):
        tool = format_results.get("tool_used", "formatter")
        if format_results.get("changes_made", False):
            lines.append(f"✨ Code formatted with {tool} - changes applied")
        else:
            lines.append(f"✅ Code already properly formatted ({tool})")
    else:
        if format_results.get("errors"):
            lines.append(f"⚠️ Formatting failed: {format_results['errors'][0]}")
        else:
            lines.append("⚠️ No formatter available")
    
    # Linting results
    if lint_results.get("linted", False):
        tool = lint_results.get("tool_used", "linter")
        critical = lint_results.get("critical_issues", 0)
        warnings = lint_results.get("warning_issues", 0)
        style = lint_results.get("style_issues", 0)
        total = critical + warnings + style
        
        if total == 0:
            lines.append(f"✅ No linting issues found ({tool})")
        else:
            lines.append(f"📊 Linting results ({tool}): {total} issues found")
            if critical > 0:
                lines.append(f"   🚨 Critical: {critical}")
            if warnings > 0:
                lines.append(f"   ⚠️ Warnings: {warnings}")
            if style > 0:
                lines.append(f"   💅 Style: {style}")
            
            # Show critical issues
            critical_issues = [issue for issue in lint_results.get("issues", []) 
                             if issue["severity"] == "critical"]
            if critical_issues:
                lines.append("")
                lines.append("🚨 CRITICAL ISSUES TO FIX:")
                for issue in critical_issues[:3]:  # Show first 3 critical issues
                    lines.append(f"   Line {issue['line']}: {issue['code']} - {issue['message']}")
                
                if len(critical_issues) > 3:
                    lines.append(f"   ... and {len(critical_issues) - 3} more critical issues")
            
            # Show some warning issues
            warning_issues = [issue for issue in lint_results.get("issues", []) 
                            if issue["severity"] == "warning"]
            if warning_issues and critical < 3:  # Only show warnings if not too many critical issues
                lines.append("")
                lines.append("⚠️ WARNINGS TO CONSIDER:")
                show_count = min(2, len(warning_issues))
                for issue in warning_issues[:show_count]:
                    lines.append(f"   Line {issue['line']}: {issue['code']} - {issue['message']}")
                
                if len(warning_issues) > show_count:
                    lines.append(f"   ... and {len(warning_issues) - show_count} more warnings")
    else:
        if lint_results.get("errors"):
            lines.append(f"⚠️ Linting failed: {lint_results['errors'][0]}")
        else:
            lines.append("⚠️ No linter available")
    
    # Summary and next steps
    total_critical = lint_results.get("critical_issues", 0)
    total_warnings = lint_results.get("warning_issues", 0)
    
    lines.append("")
    if total_critical > 0:
        lines.append("🚨 ACTION REQUIRED:")
        lines.append("   • Fix critical issues before proceeding")
        lines.append("   • Run tests to ensure functionality is preserved")
    elif total_warnings > 0:
        lines.append("💡 IMPROVEMENTS RECOMMENDED:")
        lines.append("   • Address warnings to improve code quality")
        lines.append("   • Consider refactoring for better maintainability")
    else:
        lines.append("✅ CODE QUALITY EXCELLENT:")
        lines.append("   • Well-formatted and clean code")
        lines.append("   • Ready for production use")
    
    return "\n".join(lines)


def generate_summary_message(format_results: Dict, lint_results: Dict) -> str:
    """
    Generate a brief summary message for cases with minimal issues.
    
    Args:
        format_results: Formatting results
        lint_results: Linting results
        
    Returns:
        Brief summary message
    """
    formatted = format_results.get("formatted", False)
    changes_made = format_results.get("changes_made", False)
    critical = lint_results.get("critical_issues", 0)
    warnings = lint_results.get("warning_issues", 0)
    total_issues = critical + warnings + lint_results.get("style_issues", 0)
    
    if formatted and changes_made:
        format_msg = "formatted"
    elif formatted:
        format_msg = "already formatted"
    else:
        format_msg = "formatting unavailable"
    
    if total_issues == 0:
        return f"✅ Code quality: {format_msg}, no linting issues"
    elif critical > 0:
        return f"🚨 Code quality: {format_msg}, {critical} critical issues detected"
    elif warnings > 0:
        return f"⚠️ Code quality: {format_msg}, {warnings} warnings detected"
    else:
        return f"💅 Code quality: {format_msg}, {total_issues} style issues detected"


def main():
    """
    Main hook function called by Claude Code.
    
    Expected input format (from stdin):
    {
        "tool": "Write" | "Edit",
        "path": "/path/to/file.py",
        "content": "file content...",
        "arguments": {...}
    }
    """
    try:
        # Read input from stdin
        input_data = sys.stdin.read().strip()
        if not input_data:
            # No input, allow operation to continue
            print(json.dumps({"action": "continue"}))
            return
        
        # Parse the input
        try:
            data = json.loads(input_data)
        except json.JSONDecodeError:
            # Invalid JSON, allow operation to continue
            print(json.dumps({"action": "continue"}))
            return
        
        # Extract file path and tool
        file_path = data.get("path", "")
        tool = data.get("tool", "")
        
        # Check if we should format and lint
        if not should_format_and_lint(file_path, tool):
            print(json.dumps({"action": "continue"}))
            return
        
        # Check tool availability
        available_tools = check_tool_availability()
        
        # Format the file
        format_results = format_file(file_path, available_tools)
        
        # Lint the file
        lint_results = lint_file(file_path, available_tools)
        
        # Determine response based on severity
        critical_issues = lint_results.get("critical_issues", 0)
        warning_issues = lint_results.get("warning_issues", 0)
        
        if critical_issues >= 3:
            # Many critical issues - provide detailed feedback
            feedback_message = generate_feedback_message(format_results, lint_results, file_path)
            print(json.dumps({
                "action": "continue",
                "feedback": feedback_message,
                "prompt": (
                    "🚨 Multiple critical code quality issues detected. Please review "
                    "the linting results above and fix the critical issues to improve "
                    "code reliability and maintainability."
                )
            }))
        
        elif critical_issues > 0 or warning_issues >= 5:
            # Some critical issues or many warnings - provide detailed feedback
            feedback_message = generate_feedback_message(format_results, lint_results, file_path)
            print(json.dumps({
                "action": "continue",
                "message": feedback_message
            }))
        
        else:
            # Minor issues or clean code - provide summary
            summary = generate_summary_message(format_results, lint_results)
            print(json.dumps({
                "action": "continue",
                "message": summary
            }))
    
    except Exception as e:
        # Handle any unexpected errors gracefully
        error_message = f"⚠️ Format/lint hook error: {str(e)}. Continuing with operation."
        print(json.dumps({
            "action": "continue",
            "message": error_message
        }))


if __name__ == "__main__":
    main()