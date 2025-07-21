#!/usr/bin/env python3
"""
Test utility functions for Claude Code Hooks

Provides functions for running tests, parsing results, managing test databases,
and generating test coverage reports.
"""

import os
import re
import json
import sqlite3
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .file_utils import get_use_case_root, get_project_root


def run_pytest_and_capture(test_path: str = None, coverage: bool = True) -> Dict:
    """
    Run pytest and capture the output.
    
    Args:
        test_path: Specific test file or directory to run (optional)
        coverage: Whether to include coverage analysis
        
    Returns:
        Dictionary with test results including stdout, stderr, return_code
    """
    use_case_root = get_use_case_root()
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    if test_path:
        cmd.append(test_path)
    else:
        cmd.append("tests/")
    
    # Add coverage options if requested
    if coverage:
        cmd.extend([
            "--cov=src",
            "--cov-report=term-missing",
            "--cov-report=json:coverage.json"
        ])
    
    # Add verbose output and JSON report
    cmd.extend(["-v", "--tb=short", "--json-report", "--json-report-file=test_report.json"])
    
    try:
        # Change to use-case directory
        original_dir = os.getcwd()
        if os.path.exists(use_case_root):
            os.chdir(use_case_root)
        
        # Run pytest
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "return_code": result.returncode,
            "command": " ".join(cmd)
        }
        
    except subprocess.TimeoutExpired:
        return {
            "stdout": "",
            "stderr": "Test execution timed out after 5 minutes",
            "return_code": -1,
            "command": " ".join(cmd)
        }
    except Exception as e:
        return {
            "stdout": "",
            "stderr": f"Error running tests: {str(e)}",
            "return_code": -1,
            "command": " ".join(cmd)
        }
    finally:
        # Restore original directory
        if 'original_dir' in locals():
            os.chdir(original_dir)


def parse_test_results(test_output: Dict) -> Dict:
    """
    Parse pytest output and extract meaningful information.
    
    Args:
        test_output: Output from run_pytest_and_capture
        
    Returns:
        Parsed test results with summary information
    """
    result = {
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "skipped": 0,
        "total": 0,
        "success": test_output["return_code"] == 0,
        "failures": [],
        "coverage_percent": None,
        "missing_coverage": [],
        "execution_time": None
    }
    
    stdout = test_output["stdout"]
    stderr = test_output["stderr"]
    
    # Parse test counts from output
    test_summary_pattern = r"(\d+) failed,?\s*(\d+) passed"
    passed_only_pattern = r"(\d+) passed"
    failed_only_pattern = r"(\d+) failed"
    
    if re.search(test_summary_pattern, stdout):
        match = re.search(test_summary_pattern, stdout)
        result["failed"] = int(match.group(1))
        result["passed"] = int(match.group(2))
    elif re.search(passed_only_pattern, stdout):
        match = re.search(passed_only_pattern, stdout)
        result["passed"] = int(match.group(1))
    elif re.search(failed_only_pattern, stdout):
        match = re.search(failed_only_pattern, stdout)
        result["failed"] = int(match.group(1))
    
    result["total"] = result["passed"] + result["failed"] + result["errors"] + result["skipped"]
    
    # Parse coverage information
    coverage_pattern = r"TOTAL\s+\d+\s+\d+\s+(\d+)%"
    coverage_match = re.search(coverage_pattern, stdout)
    if coverage_match:
        result["coverage_percent"] = int(coverage_match.group(1))
    
    # Parse missing coverage lines
    missing_pattern = r"(.+?)\s+\d+\s+\d+\s+\d+%\s+(.+?)$"
    for line in stdout.split('\n'):
        if 'src/' in line and '%' in line:
            match = re.search(missing_pattern, line)
            if match and match.group(2).strip():
                result["missing_coverage"].append({
                    "file": match.group(1).strip(),
                    "lines": match.group(2).strip()
                })
    
    # Parse failure information
    if "FAILURES" in stdout:
        failure_section = stdout.split("FAILURES")[1].split("=")[0]
        result["failures"].append(failure_section.strip()[:500])  # Limit length
    
    # Try to read JSON report if available
    try:
        use_case_root = get_use_case_root()
        json_report_path = os.path.join(use_case_root, "test_report.json")
        if os.path.exists(json_report_path):
            with open(json_report_path, 'r') as f:
                json_data = json.load(f)
                result["execution_time"] = json_data.get("duration", None)
                
                # More detailed test information from JSON
                if "tests" in json_data:
                    for test in json_data["tests"]:
                        if test["outcome"] == "failed":
                            result["failures"].append({
                                "test": test["nodeid"],
                                "message": test.get("call", {}).get("longrepr", "")[:200]
                            })
    except Exception:
        pass  # JSON parsing is optional
    
    return result


def get_test_coverage(file_path: str = None) -> Dict:
    """
    Get test coverage information for a specific file or overall.
    
    Args:
        file_path: Specific file to get coverage for (optional)
        
    Returns:
        Coverage information dictionary
    """
    use_case_root = get_use_case_root()
    coverage_file = os.path.join(use_case_root, "coverage.json")
    
    if not os.path.exists(coverage_file):
        return {"error": "No coverage file found. Run tests with coverage first."}
    
    try:
        with open(coverage_file, 'r') as f:
            coverage_data = json.load(f)
        
        if file_path:
            # Get coverage for specific file
            files_data = coverage_data.get("files", {})
            file_coverage = files_data.get(file_path, {})
            return {
                "file": file_path,
                "coverage_percent": file_coverage.get("summary", {}).get("percent_covered", 0),
                "missing_lines": file_coverage.get("missing_lines", []),
                "excluded_lines": file_coverage.get("excluded_lines", [])
            }
        else:
            # Get overall coverage
            totals = coverage_data.get("totals", {})
            return {
                "overall_percent": totals.get("percent_covered", 0),
                "lines_covered": totals.get("covered_lines", 0),
                "lines_missing": totals.get("missing_lines", 0),
                "total_lines": totals.get("num_statements", 0)
            }
    except Exception as e:
        return {"error": f"Error reading coverage file: {str(e)}"}


def clean_test_database(db_path: str = None) -> bool:
    """
    Clean the test database by removing all data.
    
    Args:
        db_path: Path to the database file (optional, defaults to test_hsa.db)
        
    Returns:
        True if successful, False otherwise
    """
    if db_path is None:
        use_case_root = get_use_case_root()
        db_path = os.path.join(use_case_root, "db", "test_hsa.db")
    
    try:
        if not os.path.exists(db_path):
            return True  # Database doesn't exist, consider it clean
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        # Delete all data from each table
        for table in tables:
            table_name = table[0]
            if table_name != 'sqlite_sequence':  # Skip system table
                cursor.execute(f"DELETE FROM {table_name};")
        
        # Reset auto-increment counters
        cursor.execute("DELETE FROM sqlite_sequence;")
        
        conn.commit()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error cleaning test database: {str(e)}")
        return False


def setup_test_database(schema_path: str = None) -> bool:
    """
    Set up the test database with the schema.
    
    Args:
        schema_path: Path to the schema file (optional)
        
    Returns:
        True if successful, False otherwise
    """
    use_case_root = get_use_case_root()
    
    if schema_path is None:
        schema_path = os.path.join(use_case_root, "db", "schema.sql")
    
    db_path = os.path.join(use_case_root, "db", "test_hsa.db")
    
    try:
        # Ensure db directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Remove existing database
        if os.path.exists(db_path):
            os.remove(db_path)
        
        # Create new database with schema
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            conn = sqlite3.connect(db_path)
            conn.executescript(schema_sql)
            conn.close()
        
        return True
        
    except Exception as e:
        print(f"Error setting up test database: {str(e)}")
        return False


def generate_factory_fixtures(factory_name: str, count: int = 10) -> bool:
    """
    Generate test fixtures using Factory Boy factories.
    
    Args:
        factory_name: Name of the factory to use
        count: Number of fixtures to generate
        
    Returns:
        True if successful, False otherwise
    """
    try:
        use_case_root = get_use_case_root()
        
        # This would typically import and use Factory Boy factories
        # For now, we'll create a simple implementation
        script_content = f"""
import sys
sys.path.append('{use_case_root}')

try:
    from src.test_utils.factories import {factory_name}
    
    # Generate {count} fixtures
    fixtures = []
    for i in range({count}):
        fixture = {factory_name}.create()
        fixtures.append(fixture)
    
    print(f"Generated {{len(fixtures)}} {{'{factory_name}'}} fixtures")
except ImportError as e:
    print(f"Could not import factory {{'{factory_name}'}}: {{e}}")
except Exception as e:
    print(f"Error generating fixtures: {{e}}")
"""
        
        # Execute the script
        result = subprocess.run(
            ["python", "-c", script_content],
            capture_output=True,
            text=True,
            cwd=use_case_root
        )
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error generating factory fixtures: {str(e)}")
        return False