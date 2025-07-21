#!/usr/bin/env python3
"""
Prepare Test Database Hook

This hook automatically prepares the test database before running pytest.
It clears the existing test database and pre-populates it with necessary
mock data using Factory Boy factories.

Hook Type: PreToolUse
Trigger: Before Bash commands containing "pytest"
"""

import os
import json
import sys
import sqlite3
import importlib
import inspect
from pathlib import Path
from typing import Dict, List, Optional

# Add hooks utils to path
hooks_dir = Path(__file__).parent
sys.path.insert(0, str(hooks_dir))

from utils.file_utils import (
    get_use_case_root,
    find_python_files,
    is_model_file
)
from utils.factory_generator import (
    FactoryGenerator,
    ModelParser
)


def should_prepare_database(command: str) -> bool:
    """
    Determine if we should prepare the test database based on the command.
    
    Args:
        command: The bash command being executed
        
    Returns:
        True if database preparation is needed
    """
    # Check if this is a pytest command
    if "pytest" not in command.lower():
        return False
    
    # Skip if running hooks themselves
    if ".claude/hooks" in command:
        return False
    
    # Check if we have a use-case project
    use_case_root = get_use_case_root()
    if not os.path.exists(use_case_root):
        return False
    
    # Check if we have src directory with Python files
    src_dir = os.path.join(use_case_root, "src")
    if not os.path.exists(src_dir):
        return False
    
    return True


def get_test_database_path() -> str:
    """
    Get the path to the test database.
    
    Returns:
        Path to the test database file
    """
    use_case_root = get_use_case_root()
    return os.path.join(use_case_root, "tests", "test_data.db")


def clear_test_database(db_path: str) -> bool:
    """
    Clear the test database by removing the file.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        True if successful
    """
    try:
        if os.path.exists(db_path):
            os.remove(db_path)
        
        # Ensure the tests directory exists
        db_dir = os.path.dirname(db_path)
        os.makedirs(db_dir, exist_ok=True)
        
        return True
    except Exception as e:
        print(f"Error clearing test database: {str(e)}", file=sys.stderr)
        return False


def create_test_database_schema(db_path: str) -> bool:
    """
    Create the test database schema if needed.
    
    Args:
        db_path: Path to the database file
        
    Returns:
        True if successful
    """
    try:
        use_case_root = get_use_case_root()
        
        # Look for database initialization files
        potential_schema_files = [
            os.path.join(use_case_root, "src", "database.py"),
            os.path.join(use_case_root, "src", "models.py"),
            os.path.join(use_case_root, "src", "db.py"),
            os.path.join(use_case_root, "schema.sql"),
            os.path.join(use_case_root, "tests", "schema.sql")
        ]
        
        # Try to find and execute schema initialization
        for schema_file in potential_schema_files:
            if os.path.exists(schema_file):
                if schema_file.endswith('.sql'):
                    # Execute SQL schema file
                    with sqlite3.connect(db_path) as conn:
                        with open(schema_file, 'r') as f:
                            conn.executescript(f.read())
                    return True
                elif schema_file.endswith('.py'):
                    # Try to import and run database initialization
                    try:
                        # Add the src directory to Python path
                        src_dir = os.path.join(use_case_root, "src")
                        if src_dir not in sys.path:
                            sys.path.insert(0, src_dir)
                        
                        # Import the module and look for initialization functions
                        module_name = os.path.basename(schema_file).replace('.py', '')
                        module = importlib.import_module(module_name)
                        
                        # Look for common initialization function names
                        init_functions = [
                            'create_tables', 'init_db', 'initialize_database',
                            'setup_database', 'create_schema'
                        ]
                        
                        for func_name in init_functions:
                            if hasattr(module, func_name):
                                func = getattr(module, func_name)
                                if callable(func):
                                    # Try to call with database path
                                    sig = inspect.signature(func)
                                    if len(sig.parameters) > 0:
                                        func(db_path)
                                    else:
                                        func()
                                    return True
                    except Exception as e:
                        print(f"Warning: Could not initialize schema from {schema_file}: {str(e)}", file=sys.stderr)
                        continue
        
        # If no schema file found, create a minimal database
        with sqlite3.connect(db_path) as conn:
            # Create a basic table structure for testing
            conn.execute("""
                CREATE TABLE IF NOT EXISTS test_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    value TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        return True
        
    except Exception as e:
        print(f"Error creating database schema: {str(e)}", file=sys.stderr)
        return False


def find_factory_files() -> List[str]:
    """
    Find Factory Boy factory files in the project.
    
    Returns:
        List of factory file paths
    """
    use_case_root = get_use_case_root()
    factory_files = []
    
    # Common locations for factory files
    potential_dirs = [
        os.path.join(use_case_root, "tests", "factories"),
        os.path.join(use_case_root, "tests"),
        os.path.join(use_case_root, "src", "test_utils"),
        os.path.join(use_case_root, "factories")
    ]
    
    for directory in potential_dirs:
        if os.path.exists(directory):
            python_files = find_python_files(directory, pattern="*factory*.py")
            factory_files.extend(python_files)
    
    return factory_files


def populate_test_data(db_path: str) -> Dict:
    """
    Populate the test database with Factory Boy data.
    
    Args:
        db_path: Path to the test database
        
    Returns:
        Dictionary with population results
    """
    results = {
        "factories_found": 0,
        "data_created": 0,
        "errors": []
    }
    
    try:
        use_case_root = get_use_case_root()
        
        # Add necessary paths to Python path
        src_dir = os.path.join(use_case_root, "src")
        tests_dir = os.path.join(use_case_root, "tests")
        
        for path in [src_dir, tests_dir]:
            if path not in sys.path and os.path.exists(path):
                sys.path.insert(0, path)
        
        # Find factory files
        factory_files = find_factory_files()
        
        if not factory_files:
            # If no factories exist, generate them automatically
            model_files = []
            if os.path.exists(src_dir):
                model_files = [f for f in find_python_files(src_dir) if is_model_file(f)]
            
            if model_files:
                generator = FactoryGenerator()
                for model_file in model_files[:3]:  # Limit to first 3 models
                    try:
                        generator.generate_factory_for_file(model_file)
                        results["factories_found"] += 1
                    except Exception as e:
                        results["errors"].append(f"Error generating factory for {model_file}: {str(e)}")
            
            return results
        
        # Import and use existing factories
        for factory_file in factory_files:
            try:
                # Get module name from file path
                relative_path = os.path.relpath(factory_file, use_case_root)
                module_name = relative_path.replace('/', '.').replace('.py', '')
                
                # Remove common prefixes
                if module_name.startswith('tests.'):
                    module_name = module_name[6:]
                if module_name.startswith('src.'):
                    module_name = module_name[4:]
                
                # Import the factory module
                factory_module = importlib.import_module(module_name)
                results["factories_found"] += 1
                
                # Find factory classes in the module
                for name, obj in inspect.getmembers(factory_module):
                    if (inspect.isclass(obj) and 
                        name.endswith('Factory') and 
                        hasattr(obj, 'create')):
                        
                        try:
                            # Create a few instances using the factory
                            for _ in range(3):  # Create 3 instances per factory
                                obj.create()
                                results["data_created"] += 1
                        except Exception as e:
                            results["errors"].append(f"Error creating data with {name}: {str(e)}")
                            
            except Exception as e:
                results["errors"].append(f"Error importing factory file {factory_file}: {str(e)}")
        
        return results
        
    except Exception as e:
        results["errors"].append(f"General error populating test data: {str(e)}")
        return results


def prepare_database() -> Dict:
    """
    Prepare the test database by clearing and populating it.
    
    Returns:
        Dictionary with preparation results
    """
    results = {
        "success": False,
        "database_cleared": False,
        "schema_created": False,
        "data_populated": False,
        "factories_used": 0,
        "records_created": 0,
        "errors": []
    }
    
    try:
        db_path = get_test_database_path()
        
        # Step 1: Clear existing database
        if clear_test_database(db_path):
            results["database_cleared"] = True
        else:
            results["errors"].append("Failed to clear test database")
            return results
        
        # Step 2: Create database schema
        if create_test_database_schema(db_path):
            results["schema_created"] = True
        else:
            results["errors"].append("Failed to create database schema")
            return results
        
        # Step 3: Populate with test data
        population_results = populate_test_data(db_path)
        results["factories_used"] = population_results["factories_found"]
        results["records_created"] = population_results["data_created"]
        results["errors"].extend(population_results["errors"])
        
        if population_results["factories_found"] > 0 or population_results["data_created"] > 0:
            results["data_populated"] = True
        
        # Overall success if we managed to clear and create schema
        results["success"] = results["database_cleared"] and results["schema_created"]
        
        return results
        
    except Exception as e:
        results["errors"].append(f"Database preparation failed: {str(e)}")
        return results


def generate_feedback_message(results: Dict) -> str:
    """
    Generate a feedback message about database preparation.
    
    Args:
        results: Preparation results dictionary
        
    Returns:
        Formatted feedback message
    """
    lines = []
    
    lines.append("🗄️ TEST DATABASE PREPARATION")
    lines.append("=" * 50)
    
    if results["success"]:
        lines.append("✅ Database preparation completed successfully")
        
        if results["database_cleared"]:
            lines.append("🧹 Test database cleared")
        
        if results["schema_created"]:
            lines.append("📋 Database schema initialized")
        
        if results["data_populated"]:
            lines.append(f"📊 Test data populated: {results['records_created']} records from {results['factories_used']} factories")
        else:
            lines.append("📊 No factory data populated (will use fixture data)")
        
    else:
        lines.append("⚠️ Database preparation had issues")
        
        if not results["database_cleared"]:
            lines.append("❌ Failed to clear database")
        
        if not results["schema_created"]:
            lines.append("❌ Failed to create schema")
    
    # Show errors if any
    if results["errors"]:
        lines.append("")
        lines.append("🚨 Issues encountered:")
        for error in results["errors"][:3]:  # Show first 3 errors
            lines.append(f"  • {error}")
        
        if len(results["errors"]) > 3:
            lines.append(f"  • ... and {len(results['errors']) - 3} more issues")
    
    lines.append("")
    lines.append("🧪 Ready for test execution")
    
    return "\n".join(lines)


def main():
    """
    Main hook function called by Claude Code.
    
    Expected input format (from stdin):
    {
        "tool": "Bash",
        "arguments": {
            "command": "pytest ...",
            "description": "..."
        }
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
        
        # Extract command from bash tool
        command = ""
        if data.get("tool") == "Bash":
            command = data.get("arguments", {}).get("command", "")
        
        # Check if we should prepare the database
        if not should_prepare_database(command):
            print(json.dumps({"action": "continue"}))
            return
        
        # Prepare the test database
        results = prepare_database()
        
        # Generate feedback message
        feedback_message = generate_feedback_message(results)
        
        # Always continue (don't block test execution even if preparation fails)
        print(json.dumps({
            "action": "continue",
            "message": feedback_message
        }))
    
    except Exception as e:
        # Handle any unexpected errors gracefully
        error_message = f"⚠️ Database preparation hook error: {str(e)}. Continuing with test execution."
        print(json.dumps({
            "action": "continue",
            "message": error_message
        }))


if __name__ == "__main__":
    main()