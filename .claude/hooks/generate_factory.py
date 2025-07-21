#!/usr/bin/env python3
"""
Generate Factory Hook

This hook automatically generates Factory Boy factory definitions when
model files are created or modified. It enforces consistent test data
generation patterns and supports DRY principles.

Hook Type: PostToolUse
Trigger: After Write/Edit operations on Python files containing models
"""

import os
import json
import sys
import ast
from pathlib import Path
from typing import Dict, List, Optional

# Add hooks utils to path
hooks_dir = Path(__file__).parent
sys.path.insert(0, str(hooks_dir))

from utils.file_utils import (
    get_use_case_root,
    ensure_directory_exists,
    is_python_file,
    is_model_file,
    get_relative_path
)
from utils.factory_generator import (
    FactoryGenerator,
    ModelParser
)


def should_generate_factory(file_path: str, tool: str) -> bool:
    """
    Determine if we should generate a factory for the given file.
    
    Args:
        file_path: Path to the file that was written/edited
        tool: The tool that was used (Write/Edit)
        
    Returns:
        True if a factory should be generated
    """
    # Only process Write and Edit operations
    if tool not in ["Write", "Edit"]:
        return False
    
    # Only process Python files
    if not is_python_file(file_path):
        return False
    
    # Skip test files
    if "/test" in file_path or file_path.endswith("_test.py"):
        return False
    
    # Skip hook files
    if "/.claude/hooks/" in file_path:
        return False
    
    # Skip factory files themselves
    if "factory" in file_path.lower():
        return False
    
    # Only process files in the use-case directory
    use_case_root = get_use_case_root()
    if use_case_root and use_case_root not in file_path:
        return False
    
    # Check if the file contains models
    return is_model_file(file_path)


def get_factory_file_path(model_file_path: str) -> str:
    """
    Determine where the factory file should be created.
    
    Args:
        model_file_path: Path to the model file
        
    Returns:
        Path where the factory file should be created
    """
    use_case_root = get_use_case_root()
    
    # Extract model name from file path
    model_name = Path(model_file_path).stem
    
    # Common factory file locations (in order of preference)
    potential_locations = [
        os.path.join(use_case_root, "tests", "factories", f"{model_name}_factory.py"),
        os.path.join(use_case_root, "tests", f"{model_name}_factory.py"),
        os.path.join(use_case_root, "src", "test_utils", f"{model_name}_factory.py"),
        os.path.join(use_case_root, "factories", f"{model_name}_factory.py")
    ]
    
    # Check if any existing factory directory exists
    for factory_path in potential_locations:
        factory_dir = os.path.dirname(factory_path)
        if os.path.exists(factory_dir):
            return factory_path
    
    # Default to tests/factories/ directory
    return potential_locations[0]


def extract_models_from_file(file_path: str) -> List[Dict]:
    """
    Extract model information from a Python file.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        List of model information dictionaries
    """
    models = []
    
    try:
        parser = ModelParser()
        parsed_models = parser.parse_file(file_path)
        
        for model_info in parsed_models:
            models.append({
                "name": model_info["name"],
                "fields": model_info["fields"],
                "base_classes": model_info.get("base_classes", []),
                "file_path": file_path
            })
    
    except Exception as e:
        print(f"Error parsing models from {file_path}: {str(e)}", file=sys.stderr)
    
    return models


def generate_factory_file(model_file_path: str, factory_file_path: str) -> Dict:
    """
    Generate a Factory Boy factory file for the given model file.
    
    Args:
        model_file_path: Path to the model file
        factory_file_path: Path where the factory file should be created
        
    Returns:
        Dictionary with generation results
    """
    results = {
        "success": False,
        "factory_path": factory_file_path,
        "models_processed": 0,
        "factories_created": 0,
        "errors": []
    }
    
    try:
        # Extract models from the file
        models = extract_models_from_file(model_file_path)
        
        if not models:
            results["errors"].append("No models found in the file")
            return results
        
        results["models_processed"] = len(models)
        
        # Check if factory file already exists
        if os.path.exists(factory_file_path):
            # Factory already exists, don't overwrite
            results["errors"].append("Factory file already exists - not overwriting")
            return results
        
        # Ensure the factory directory exists
        ensure_directory_exists(factory_file_path)
        
        # Generate factory content using the generator
        generator = FactoryGenerator()
        
        # For now, generate factory for the first model in the file
        # (In a real implementation, you might want to handle multiple models)
        primary_model = models[0]
        
        # Generate the factory content
        factory_content = generator.generate_factory_file_content(
            model_name=primary_model["name"],
            model_fields=primary_model["fields"],
            model_import_path=_get_model_import_path(model_file_path, primary_model["name"])
        )
        
        # Write the factory file
        with open(factory_file_path, 'w') as f:
            f.write(factory_content)
        
        results["factories_created"] = 1
        results["success"] = True
        
        # Create __init__.py in the factories directory if needed
        factory_dir = os.path.dirname(factory_file_path)
        init_file = os.path.join(factory_dir, "__init__.py")
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write('"""Factory Boy factories for test data generation."""\n')
        
    except Exception as e:
        results["errors"].append(f"Error generating factory: {str(e)}")
    
    return results


def _get_model_import_path(model_file_path: str, model_name: str) -> str:
    """
    Generate the import path for a model.
    
    Args:
        model_file_path: Path to the model file
        model_name: Name of the model class
        
    Returns:
        Import path string
    """
    try:
        use_case_root = get_use_case_root()
        relative_path = get_relative_path(model_file_path, use_case_root)
        
        # Remove src/ prefix if present
        if relative_path.startswith('src/'):
            relative_path = relative_path[4:]
        
        # Convert path to import format
        import_path = relative_path.replace('/', '.').replace('.py', '')
        
        # Add src prefix for imports
        return f"src.{import_path}"
    
    except Exception:
        # Fallback
        return f"src.{Path(model_file_path).stem}"


def generate_feedback_message(results: Dict, model_file_path: str) -> str:
    """
    Generate a feedback message about factory generation.
    
    Args:
        results: Generation results dictionary
        model_file_path: Path to the model file
        
    Returns:
        Formatted feedback message
    """
    lines = []
    
    use_case_root = get_use_case_root()
    relative_model_path = get_relative_path(model_file_path, use_case_root)
    
    if results["success"]:
        relative_factory_path = get_relative_path(results["factory_path"], use_case_root)
        
        lines.append(f"🏭 FACTORY GENERATED: Created Factory Boy factory for {relative_model_path}")
        lines.append(f"📁 Factory location: {relative_factory_path}")
        lines.append(f"📊 Models processed: {results['models_processed']}")
        lines.append(f"✅ Factories created: {results['factories_created']}")
        
        # Add usage example
        factory_name = Path(results["factory_path"]).stem
        lines.append("")
        lines.append("💡 Usage example:")
        lines.append(f"   from tests.factories.{factory_name} import *")
        lines.append(f"   instance = ModelFactory.create()")
        
    else:
        lines.append(f"⚠️ Factory generation skipped for {relative_model_path}")
        
        if results["errors"]:
            lines.append("Reasons:")
            for error in results["errors"]:
                lines.append(f"  • {error}")
    
    return "\n".join(lines)


def update_conftest_py(factory_file_path: str) -> None:
    """
    Update conftest.py to include the new factory in fixtures.
    
    Args:
        factory_file_path: Path to the generated factory file
    """
    try:
        use_case_root = get_use_case_root()
        conftest_path = os.path.join(use_case_root, "tests", "conftest.py")
        
        # Create conftest.py if it doesn't exist
        if not os.path.exists(conftest_path):
            conftest_content = '''"""
Test configuration and fixtures.

This file contains pytest fixtures and configuration for the test suite.
"""

import pytest
import os
import sqlite3
from pathlib import Path

# Test database fixture
@pytest.fixture
def test_db():
    """Provide a clean test database for each test."""
    db_path = "tests/test_data.db"
    
    # Remove existing database
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Create new database
    # Add your schema creation logic here
    
    yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


# Add more fixtures as needed
'''
            
            ensure_directory_exists(conftest_path)
            with open(conftest_path, 'w') as f:
                f.write(conftest_content)
    
    except Exception as e:
        print(f"Warning: Could not update conftest.py: {str(e)}", file=sys.stderr)


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
        
        # Check if we should generate a factory
        if not should_generate_factory(file_path, tool):
            print(json.dumps({"action": "continue"}))
            return
        
        # Determine factory file path
        factory_file_path = get_factory_file_path(file_path)
        
        # Generate the factory
        results = generate_factory_file(file_path, factory_file_path)
        
        # Update conftest.py if factory was created successfully
        if results["success"]:
            update_conftest_py(factory_file_path)
        
        # Generate feedback message
        feedback_message = generate_feedback_message(results, file_path)
        
        # Always continue (don't block the operation)
        print(json.dumps({
            "action": "continue",
            "message": feedback_message
        }))
    
    except Exception as e:
        # Handle any unexpected errors gracefully
        error_message = f"⚠️ Factory generation hook error: {str(e)}. Continuing with operation."
        print(json.dumps({
            "action": "continue",
            "message": error_message
        }))


if __name__ == "__main__":
    main()