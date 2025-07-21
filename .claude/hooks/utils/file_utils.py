#!/usr/bin/env python3
"""
File utility functions for Claude Code Hooks

Provides functions for file path manipulation, Python file detection,
and project structure navigation.
"""

import os
import re
from pathlib import Path
from typing import Optional, List


def get_corresponding_test_file(source_file: str) -> str:
    """
    Get the corresponding test file path for a source file.
    
    Args:
        source_file: Path to the source file
        
    Returns:
        Path to the corresponding test file
        
    Example:
        src/agents/user_input.py -> tests/test_user_input.py
        src/models/hsa_profile.py -> tests/test_hsa_profile.py
    """
    source_path = Path(source_file)
    
    # Extract the filename without extension
    filename = source_path.stem
    
    # Remove 'src/' prefix if present and construct test path
    if 'src/' in str(source_path):
        # For files in src/, put tests in tests/ directory
        test_filename = f"test_{filename}.py"
        return f"tests/{test_filename}"
    else:
        # For files not in src/, put test alongside
        test_filename = f"test_{filename}.py"
        return str(source_path.parent / test_filename)


def get_corresponding_source_file(test_file: str) -> str:
    """
    Get the corresponding source file path for a test file.
    
    Args:
        test_file: Path to the test file
        
    Returns:
        Path to the corresponding source file
    """
    test_path = Path(test_file)
    
    # Remove 'test_' prefix from filename
    filename = test_path.stem
    if filename.startswith('test_'):
        source_filename = filename[5:] + '.py'
    else:
        source_filename = filename + '.py'
    
    # If test is in tests/ directory, source is likely in src/
    if 'tests/' in str(test_path):
        return f"src/{source_filename}"
    else:
        return str(test_path.parent / source_filename)


def ensure_directory_exists(file_path: str) -> None:
    """
    Ensure the directory for the given file path exists.
    
    Args:
        file_path: Path to the file whose directory should exist
    """
    directory = Path(file_path).parent
    directory.mkdir(parents=True, exist_ok=True)


def is_python_file(file_path: str) -> bool:
    """
    Check if the file is a Python file.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if the file has a .py extension
    """
    return file_path.endswith('.py')


def is_test_file(file_path: str) -> bool:
    """
    Check if the file is a test file.
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if the file is a test file
    """
    filename = Path(file_path).name
    return (filename.startswith('test_') and filename.endswith('.py')) or \
           ('tests/' in file_path and filename.endswith('.py'))


def is_model_file(file_path: str) -> bool:
    """
    Check if the file contains data models (SQLAlchemy, Pydantic, etc.).
    
    Args:
        file_path: Path to the file to check
        
    Returns:
        True if the file likely contains data models
    """
    if not is_python_file(file_path):
        return False
    
    # Check file path patterns
    path_patterns = [
        r'/models/',
        r'/model\.py$',
        r'_model\.py$',
        r'/entities/',
        r'/schemas/',
    ]
    
    for pattern in path_patterns:
        if re.search(pattern, file_path):
            return True
    
    return False


def get_project_root() -> str:
    """
    Get the project root directory (where .claude directory is located).
    
    Returns:
        Path to the project root directory
    """
    current_dir = Path.cwd()
    while current_dir != current_dir.parent:
        if (current_dir / '.claude').exists():
            return str(current_dir)
        current_dir = current_dir.parent
    
    # Fallback to current directory
    return str(Path.cwd())


def get_use_case_root() -> str:
    """
    Get the use-case directory where all project code should be located.
    
    Returns:
        Path to the use-case directory
    """
    project_root = get_project_root()
    return os.path.join(project_root, 'use-case')


def find_python_files(directory: str, pattern: str = "*.py") -> List[str]:
    """
    Find all Python files in a directory matching a pattern.
    
    Args:
        directory: Directory to search in
        pattern: File pattern to match (default: "*.py")
        
    Returns:
        List of file paths matching the pattern
    """
    directory_path = Path(directory)
    if not directory_path.exists():
        return []
    
    return [str(path) for path in directory_path.rglob(pattern)]


def get_relative_path(file_path: str, base_path: str = None) -> str:
    """
    Get the relative path from the base path.
    
    Args:
        file_path: The file path to make relative
        base_path: The base path (defaults to project root)
        
    Returns:
        Relative path string
    """
    if base_path is None:
        base_path = get_project_root()
    
    try:
        return str(Path(file_path).relative_to(Path(base_path)))
    except ValueError:
        # If file_path is not relative to base_path, return as-is
        return file_path