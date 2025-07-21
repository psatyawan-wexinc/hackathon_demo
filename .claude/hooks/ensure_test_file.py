#!/usr/bin/env python3
"""
Ensure Test File Hook

This hook enforces TDD by ensuring that test files exist when writing new Python modules.
It automatically generates test stubs using Factory Boy templates when needed.

Hook Type: PreToolUse
Trigger: Before Write/Edit operations on .py files
"""

import os
import json
import sys
from pathlib import Path

# Add hooks utils to path
hooks_dir = Path(__file__).parent
sys.path.insert(0, str(hooks_dir))

from utils.file_utils import (
    get_corresponding_test_file,
    ensure_directory_exists,
    is_python_file,
    is_test_file,
    get_use_case_root,
    get_relative_path
)


def should_create_test_file(file_path: str) -> bool:
    """
    Determine if we should create a test file for the given source file.
    
    Args:
        file_path: Path to the source file being written
        
    Returns:
        True if a test file should be created
    """
    # Only process Python files
    if not is_python_file(file_path):
        return False
    
    # Don't create tests for test files themselves
    if is_test_file(file_path):
        return False
    
    # Skip hook files
    if '/.claude/hooks/' in file_path:
        return False
    
    # Skip __init__.py files
    if file_path.endswith('__init__.py'):
        return False
    
    # Skip migration files
    if '/migrations/' in file_path or '/alembic/' in file_path:
        return False
    
    # Only process files in the use-case directory
    use_case_root = get_use_case_root()
    if use_case_root and use_case_root not in file_path:
        return False
    
    return True


def extract_class_and_method_info(file_path: str) -> dict:
    """
    Extract class and method information from a Python file to customize the test template.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Dictionary with class and method information
    """
    info = {
        "class_name": "Module",
        "method_name": "process", 
        "import_path": "src.module",
        "factory_class": "ModuleFactory"
    }
    
    try:
        # Extract module name from file path
        file_stem = Path(file_path).stem
        
        # Generate class name (PascalCase from file name)
        class_name = ''.join(word.capitalize() for word in file_stem.split('_'))
        info["class_name"] = class_name
        
        # Generate import path
        relative_path = get_relative_path(file_path, get_use_case_root())
        if relative_path.startswith('src/'):
            import_path = relative_path[4:]  # Remove 'src/' prefix
            import_path = import_path.replace('/', '.').replace('.py', '')
            info["import_path"] = f"src.{import_path}"
        
        # Generate factory class name
        info["factory_class"] = f"{class_name}Factory"
        
        # Try to detect primary method name from common patterns
        method_patterns = [
            "process", "calculate", "validate", "create", "update", 
            "delete", "get", "handle", "execute", "run"
        ]
        
        for pattern in method_patterns:
            if pattern in file_stem.lower():
                info["method_name"] = pattern
                break
        
        # HSA-specific method detection
        if "hsa" in file_stem.lower() or "contribution" in file_stem.lower():
            if "calc" in file_stem.lower() or "limit" in file_stem.lower():
                info["method_name"] = "calculate_limit"
            elif "input" in file_stem.lower():
                info["method_name"] = "collect_input"
            elif "planner" in file_stem.lower():
                info["method_name"] = "generate_plan"
        
    except Exception as e:
        # Use defaults if extraction fails
        pass
    
    return info


def generate_test_file_content(file_path: str, test_file_path: str) -> str:
    """
    Generate the content for a new test file using the template.
    
    Args:
        file_path: Path to the source file
        test_file_path: Path to the test file to create
        
    Returns:
        String content for the test file
    """
    try:
        # Read the test template
        template_path = hooks_dir / "templates" / "test_template.py"
        with open(template_path, 'r') as f:
            template_content = f.read()
        
        # Extract information about the source file
        info = extract_class_and_method_info(file_path)
        
        # Replace template placeholders
        content = template_content.format(
            module_name=info["class_name"],
            class_name=info["class_name"],
            method_name=info["method_name"],
            import_path=info["import_path"],
            factory_class=info["factory_class"]
        )
        
        return content
        
    except Exception as e:
        # Fallback to basic test file if template processing fails
        class_name = Path(file_path).stem.replace('_', ' ').title().replace(' ', '')
        
        return f'''#!/usr/bin/env python3
"""
Test file for {class_name}

This file was automatically generated by Claude Code Hooks to enforce TDD.
Please implement the actual test cases following the Red-Green-Refactor cycle.
"""

import pytest
from unittest.mock import Mock

# TODO: Import the module under test
# from {info.get("import_path", "src.module")} import {class_name}


class Test{class_name}:
    """Test cases for {class_name}."""
    
    @pytest.mark.skip(reason="TDD Red Phase - Implementation needed")
    def test_{info.get("method_name", "process")}_happy_path(self):
        """Test the happy path."""
        # TODO: Implement test
        assert True
    
    @pytest.mark.skip(reason="TDD Red Phase - Implementation needed")
    def test_{info.get("method_name", "process")}_edge_cases(self):
        """Test edge cases."""
        # TODO: Implement test
        assert True
    
    @pytest.mark.skip(reason="TDD Red Phase - Implementation needed")
    def test_{info.get("method_name", "process")}_error_handling(self):
        """Test error handling."""
        # TODO: Implement test
        assert True
'''


def create_test_file(file_path: str) -> bool:
    """
    Create a test file for the given source file.
    
    Args:
        file_path: Path to the source file
        
    Returns:
        True if test file was created successfully
    """
    try:
        test_file_path = get_corresponding_test_file(file_path)
        
        # Make path absolute and ensure it's in the use-case directory
        use_case_root = get_use_case_root()
        if not test_file_path.startswith('/'):
            test_file_path = os.path.join(use_case_root, test_file_path)
        
        # Check if test file already exists
        if os.path.exists(test_file_path):
            return True  # Test file already exists
        
        # Create the test file directory
        ensure_directory_exists(test_file_path)
        
        # Generate test file content
        content = generate_test_file_content(file_path, test_file_path)
        
        # Write the test file
        with open(test_file_path, 'w') as f:
            f.write(content)
        
        return True
        
    except Exception as e:
        print(f"Error creating test file: {str(e)}", file=sys.stderr)
        return False


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
        
        # Extract file path
        file_path = data.get("path", "")
        tool = data.get("tool", "")
        
        # Check if we should process this file
        if not should_create_test_file(file_path):
            print(json.dumps({"action": "continue"}))
            return
        
        # Check if test file exists
        test_file_path = get_corresponding_test_file(file_path)
        use_case_root = get_use_case_root()
        if not test_file_path.startswith('/'):
            test_file_path = os.path.join(use_case_root, test_file_path)
        
        if os.path.exists(test_file_path):
            # Test file exists, continue with operation
            print(json.dumps({"action": "continue"}))
            return
        
        # Create the test file
        success = create_test_file(file_path)
        
        if success:
            # Test file created successfully, continue with operation
            relative_test_path = get_relative_path(test_file_path, get_use_case_root())
            message = f"✅ TDD Enforced: Created test file {relative_test_path} for {get_relative_path(file_path, get_use_case_root())}"
            
            print(json.dumps({
                "action": "continue",
                "message": message
            }))
        else:
            # Failed to create test file, but don't block the operation
            print(json.dumps({
                "action": "continue",
                "message": "⚠️ Warning: Could not create test file, but continuing with operation"
            }))
    
    except Exception as e:
        # Handle any unexpected errors gracefully
        print(json.dumps({
            "action": "continue",
            "message": f"⚠️ Hook error: {str(e)}, continuing with operation"
        }))


if __name__ == "__main__":
    main()