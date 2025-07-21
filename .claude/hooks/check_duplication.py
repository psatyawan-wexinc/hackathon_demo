#!/usr/bin/env python3
"""
Check Duplication Hook

This hook analyzes code for duplications in real-time after file modifications.
It enforces DRY (Don't Repeat Yourself) principles by detecting code duplication
and providing refactoring suggestions.

Hook Type: PostToolUse
Trigger: After Write/Edit operations on Python files
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add hooks utils to path
hooks_dir = Path(__file__).parent
sys.path.insert(0, str(hooks_dir))

from utils.file_utils import (
    get_use_case_root,
    is_python_file,
    get_relative_path
)
from utils.duplication_detector import (
    DuplicationDetector,
    detect_duplications_in_file,
    calculate_dry_score,
    generate_dry_recommendations
)


def should_check_duplication(file_path: str, tool: str) -> bool:
    """
    Determine if we should check for duplications in the given file.
    
    Args:
        file_path: Path to the file that was written/edited
        tool: The tool that was used (Write/Edit)
        
    Returns:
        True if duplication check should be performed
    """
    # Only process Write and Edit operations
    if tool not in ["Write", "Edit"]:
        return False
    
    # Only process Python files
    if not is_python_file(file_path):
        return False
    
    # Skip test files (they often have similar structure patterns)
    if "/test" in file_path or file_path.endswith("_test.py"):
        return False
    
    # Skip hook files
    if "/.claude/hooks/" in file_path:
        return False
    
    # Skip __init__.py files (usually minimal)
    if file_path.endswith("__init__.py"):
        return False
    
    # Skip migration files
    if "/migrations/" in file_path or "/alembic/" in file_path:
        return False
    
    # Only process files in the use-case directory
    use_case_root = get_use_case_root()
    if use_case_root and use_case_root not in file_path:
        return False
    
    # Check if file is substantial enough to analyze
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Skip very small files (less than 10 non-empty lines)
            non_empty_lines = [line.strip() for line in content.split('\n') if line.strip()]
            if len(non_empty_lines) < 10:
                return False
    except Exception:
        return False
    
    return True


def analyze_file_duplications(file_path: str) -> Dict:
    """
    Analyze the given file for code duplications.
    
    Args:
        file_path: Path to the file to analyze
        
    Returns:
        Dictionary with duplication analysis results
    """
    try:
        return detect_duplications_in_file(
            file_path, 
            min_lines=3, 
            similarity_threshold=0.75  # Slightly lower threshold for real-time checking
        )
    except Exception as e:
        return {
            "file": file_path,
            "total_duplications": 0,
            "high_severity": 0,
            "medium_severity": 0,
            "low_severity": 0,
            "duplications": [],
            "dry_score": 100,
            "recommendations": [],
            "error": str(e)
        }


def categorize_duplication_severity(analysis: Dict) -> str:
    """
    Categorize the overall duplication severity for the file.
    
    Args:
        analysis: Duplication analysis results
        
    Returns:
        Severity level: "critical", "warning", "info", or "clean"
    """
    high_count = analysis.get("high_severity", 0)
    medium_count = analysis.get("medium_severity", 0)
    total_count = analysis.get("total_duplications", 0)
    dry_score = analysis.get("dry_score", 100)
    
    if high_count >= 3 or dry_score < 60:
        return "critical"
    elif high_count >= 1 or medium_count >= 3 or dry_score < 80:
        return "warning"
    elif total_count > 0:
        return "info"
    else:
        return "clean"


def generate_feedback_message(analysis: Dict, file_path: str) -> str:
    """
    Generate a feedback message about duplication analysis.
    
    Args:
        analysis: Duplication analysis results
        file_path: Path to the analyzed file
        
    Returns:
        Formatted feedback message
    """
    lines = []
    
    use_case_root = get_use_case_root()
    relative_path = get_relative_path(file_path, use_case_root)
    dry_score = analysis.get("dry_score", 100)
    
    # Header
    severity = categorize_duplication_severity(analysis)
    severity_icons = {
        "critical": "🚨",
        "warning": "⚠️", 
        "info": "💡",
        "clean": "✅"
    }
    
    lines.append(f"{severity_icons.get(severity, '📊')} DRY COMPLIANCE CHECK: {relative_path}")
    lines.append("=" * 50)
    
    # DRY Score
    score_icon = "✅" if dry_score >= 80 else "⚠️" if dry_score >= 60 else "🚨"
    lines.append(f"DRY Score: {dry_score}/100 {score_icon}")
    
    # Duplication summary
    total_duplications = analysis.get("total_duplications", 0)
    high_severity = analysis.get("high_severity", 0)
    medium_severity = analysis.get("medium_severity", 0)
    low_severity = analysis.get("low_severity", 0)
    
    if total_duplications == 0:
        lines.append("🎉 No code duplications detected!")
        lines.append("Code follows DRY principles well.")
    else:
        lines.append(f"📊 Duplications found: {total_duplications} total")
        if high_severity > 0:
            lines.append(f"   🚨 High severity: {high_severity}")
        if medium_severity > 0:
            lines.append(f"   ⚠️ Medium severity: {medium_severity}")
        if low_severity > 0:
            lines.append(f"   💡 Low severity: {low_severity}")
    
    # Show detailed duplications for high severity cases
    duplications = analysis.get("duplications", [])
    high_severity_dups = [d for d in duplications if d["severity"] == "high"]
    
    if high_severity_dups:
        lines.append("")
        lines.append("🚨 HIGH SEVERITY DUPLICATIONS:")
        
        for i, dup in enumerate(high_severity_dups[:2]):  # Show first 2 high severity
            lines.append(f"   {i+1}. Similarity: {dup['similarity']:.1%}")
            for block in dup["blocks"]:
                block_path = get_relative_path(block["file"], use_case_root)
                lines.append(f"      📁 {block_path}:{block['lines']} ({block['line_count']} lines)")
            
            # Show first suggestion
            if dup["suggestions"]:
                lines.append(f"      💡 {dup['suggestions'][0]}")
        
        if len(high_severity_dups) > 2:
            lines.append(f"   ... and {len(high_severity_dups) - 2} more high-severity duplications")
    
    # Recommendations
    recommendations = analysis.get("recommendations", [])
    if recommendations and severity in ["critical", "warning"]:
        lines.append("")
        lines.append("🔧 REFACTORING RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations[:3], 1):  # Show first 3 recommendations
            lines.append(f"   {i}. {rec}")
    
    # Next steps based on severity
    lines.append("")
    if severity == "critical":
        lines.append("🚨 IMMEDIATE ACTION REQUIRED:")
        lines.append("   • Address high-severity duplications before proceeding")
        lines.append("   • Extract common logic into shared utilities")
        lines.append("   • Consider refactoring for better code organization")
    elif severity == "warning":
        lines.append("⚠️ IMPROVEMENT RECOMMENDED:")
        lines.append("   • Review duplicated code for refactoring opportunities")
        lines.append("   • Consider extracting common patterns")
    elif severity == "info":
        lines.append("💡 MINOR IMPROVEMENTS POSSIBLE:")
        lines.append("   • Small duplications detected - consider minor refactoring")
    else:
        lines.append("✅ EXCELLENT DRY COMPLIANCE:")
        lines.append("   • Code is well-organized with minimal duplication")
    
    # Error handling
    if analysis.get("error"):
        lines.append("")
        lines.append(f"⚠️ Analysis error: {analysis['error']}")
    
    return "\n".join(lines)


def should_block_operation(analysis: Dict) -> bool:
    """
    Determine if the operation should be blocked due to severe duplications.
    
    Args:
        analysis: Duplication analysis results
        
    Returns:
        True if operation should be blocked (for very severe cases)
    """
    # Generally, don't block operations for duplication issues
    # This is informational feedback to encourage good practices
    # Only block in extreme cases
    
    high_severity = analysis.get("high_severity", 0)
    dry_score = analysis.get("dry_score", 100)
    
    # Block only in extreme cases where there are many high-severity duplications
    # and very low DRY score
    return high_severity >= 5 and dry_score < 40


def generate_duplication_summary(analysis: Dict) -> str:
    """
    Generate a brief summary for less severe cases.
    
    Args:
        analysis: Duplication analysis results
        
    Returns:
        Brief summary message
    """
    dry_score = analysis.get("dry_score", 100)
    total_duplications = analysis.get("total_duplications", 0)
    severity = categorize_duplication_severity(analysis)
    
    if severity == "clean":
        return f"✅ DRY compliance: {dry_score}/100 - No duplications detected"
    elif severity == "info":
        return f"💡 DRY compliance: {dry_score}/100 - {total_duplications} minor duplications"
    else:
        high_count = analysis.get("high_severity", 0)
        if high_count > 0:
            return f"⚠️ DRY compliance: {dry_score}/100 - {high_count} high-severity duplications detected"
        else:
            return f"⚠️ DRY compliance: {dry_score}/100 - {total_duplications} duplications detected"


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
        
        # Check if we should analyze for duplications
        if not should_check_duplication(file_path, tool):
            print(json.dumps({"action": "continue"}))
            return
        
        # Analyze the file for duplications
        analysis = analyze_file_duplications(file_path)
        
        # Determine severity and response
        severity = categorize_duplication_severity(analysis)
        should_block = should_block_operation(analysis)
        
        if severity in ["critical", "warning"]:
            # Provide detailed feedback for significant issues
            feedback_message = generate_feedback_message(analysis, file_path)
            
            if should_block:
                # Block operation for extreme cases
                print(json.dumps({
                    "action": "continue",
                    "feedback": feedback_message,
                    "prompt": (
                        "🚨 CRITICAL DRY VIOLATION: Significant code duplication detected. "
                        "Please review the duplication analysis above and refactor the code "
                        "to eliminate redundancy before proceeding. This will improve code "
                        "maintainability and follow DRY principles."
                    )
                }))
            else:
                # Continue with detailed feedback
                print(json.dumps({
                    "action": "continue",
                    "message": feedback_message
                }))
        
        elif severity == "info":
            # Brief feedback for minor issues
            summary = generate_duplication_summary(analysis)
            print(json.dumps({
                "action": "continue",
                "message": summary
            }))
        
        else:
            # Clean code - minimal feedback
            summary = generate_duplication_summary(analysis)
            print(json.dumps({
                "action": "continue",
                "message": summary
            }))
    
    except Exception as e:
        # Handle any unexpected errors gracefully
        error_message = f"⚠️ Duplication check hook error: {str(e)}. Continuing with operation."
        print(json.dumps({
            "action": "continue",
            "message": error_message
        }))


if __name__ == "__main__":
    main()