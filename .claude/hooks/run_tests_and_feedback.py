#!/usr/bin/env python3
"""
Run Tests and Feedback Hook

This hook implements continuous testing feedback by automatically running pytest
after development tasks and providing feedback to Claude if tests fail.

Hook Type: Stop
Trigger: After Claude finishes a development task
"""

import os
import json
import sys
from pathlib import Path

# Add hooks utils to path
hooks_dir = Path(__file__).parent
sys.path.insert(0, str(hooks_dir))

from utils.test_utils import (
    run_pytest_and_capture,
    parse_test_results,
    get_test_coverage
)
from utils.file_utils import (
    get_use_case_root,
    find_python_files
)


def should_run_tests() -> bool:
    """
    Determine if tests should be run based on the current state.
    
    Returns:
        True if tests should be run
    """
    use_case_root = get_use_case_root()
    
    # Check if use-case directory exists
    if not os.path.exists(use_case_root):
        return False
    
    # Check if there are any Python files in src/
    src_dir = os.path.join(use_case_root, "src")
    if not os.path.exists(src_dir):
        return False
    
    python_files = find_python_files(src_dir)
    if not python_files:
        return False
    
    # Check if there are any test files
    tests_dir = os.path.join(use_case_root, "tests")
    if not os.path.exists(tests_dir):
        return False
    
    test_files = find_python_files(tests_dir, "test_*.py")
    if not test_files:
        return False
    
    return True


def analyze_test_failures(test_results: dict) -> dict:
    """
    Analyze test failures and provide actionable feedback.
    
    Args:
        test_results: Parsed test results from parse_test_results
        
    Returns:
        Dictionary with analysis and recommendations
    """
    analysis = {
        "critical_issues": [],
        "recommendations": [],
        "next_steps": [],
        "tdd_guidance": []
    }
    
    # Analyze test failures
    if test_results["failed"] > 0:
        analysis["critical_issues"].append(f"{test_results['failed']} test(s) are failing")
        
        # Extract specific failure information
        if test_results["failures"]:
            for failure in test_results["failures"][:3]:  # Limit to first 3 failures
                if isinstance(failure, dict):
                    analysis["critical_issues"].append(f"Failed test: {failure['test']}")
                    if failure.get("message"):
                        analysis["critical_issues"].append(f"Error: {failure['message'][:200]}...")
                else:
                    analysis["critical_issues"].append(f"Failure details: {str(failure)[:200]}...")
        
        # TDD guidance for failures
        analysis["tdd_guidance"].extend([
            "🔴 RED PHASE DETECTED: Tests are failing as expected in TDD",
            "📝 Next: Implement minimal code to make these tests pass",
            "✅ Goal: Move to GREEN phase where all tests pass"
        ])
        
        analysis["next_steps"].extend([
            "Review the failing test assertions",
            "Implement the minimum code needed to pass tests",
            "Run tests again to verify fixes",
            "Refactor code while keeping tests green"
        ])
    
    # Analyze coverage
    coverage_percent = test_results.get("coverage_percent", 0)
    if coverage_percent < 80:
        analysis["critical_issues"].append(f"Test coverage is {coverage_percent}% (minimum: 80%)")
        analysis["recommendations"].extend([
            "Add more test cases to improve coverage",
            "Focus on testing edge cases and error conditions",
            "Review uncovered code paths"
        ])
        
        # Add specific missing coverage information
        if test_results.get("missing_coverage"):
            analysis["recommendations"].append("Missing coverage in:")
            for missing in test_results["missing_coverage"][:5]:  # Limit to first 5
                analysis["recommendations"].append(f"  - {missing['file']}: lines {missing['lines']}")
    
    # Analyze error patterns
    if test_results["errors"] > 0:
        analysis["critical_issues"].append(f"{test_results['errors']} test error(s) detected")
        analysis["next_steps"].extend([
            "Fix test setup/teardown issues",
            "Check import statements and dependencies",
            "Verify test database configuration"
        ])
    
    # Success guidance
    if test_results["success"]:
        analysis["tdd_guidance"].extend([
            "✅ GREEN PHASE: All tests are passing!",
            "🔄 Consider: Refactor code to improve quality while keeping tests green",
            "➕ Next: Add more tests for additional functionality"
        ])
        
        if coverage_percent >= 80:
            analysis["recommendations"].append("✅ Excellent! Test coverage meets requirements")
        
        analysis["next_steps"].extend([
            "Review code for potential improvements",
            "Consider adding more edge case tests",
            "Ensure code follows DRY principles"
        ])
    
    return analysis


def generate_feedback_message(test_results: dict, analysis: dict) -> str:
    """
    Generate a comprehensive feedback message for Claude.
    
    Args:
        test_results: Parsed test results
        analysis: Test failure analysis
        
    Returns:
        Formatted feedback message
    """
    lines = []
    
    # Test summary
    total_tests = test_results["total"]
    passed = test_results["passed"]
    failed = test_results["failed"]
    coverage = test_results.get("coverage_percent", 0)
    
    lines.append("🧪 AUTOMATED TEST RESULTS")
    lines.append("=" * 50)
    lines.append(f"Tests: {passed} passed, {failed} failed, {total_tests} total")
    lines.append(f"Coverage: {coverage}% {'✅' if coverage >= 80 else '⚠️'}")
    
    if test_results.get("execution_time"):
        lines.append(f"Execution time: {test_results['execution_time']:.2f}s")
    
    lines.append("")
    
    # TDD guidance
    if analysis["tdd_guidance"]:
        lines.append("🔄 TDD CYCLE GUIDANCE:")
        for guidance in analysis["tdd_guidance"]:
            lines.append(f"  {guidance}")
        lines.append("")
    
    # Critical issues
    if analysis["critical_issues"]:
        lines.append("🚨 CRITICAL ISSUES TO ADDRESS:")
        for issue in analysis["critical_issues"]:
            lines.append(f"  • {issue}")
        lines.append("")
    
    # Next steps
    if analysis["next_steps"]:
        lines.append("📋 NEXT STEPS:")
        for i, step in enumerate(analysis["next_steps"], 1):
            lines.append(f"  {i}. {step}")
        lines.append("")
    
    # Recommendations
    if analysis["recommendations"]:
        lines.append("💡 RECOMMENDATIONS:")
        for rec in analysis["recommendations"]:
            lines.append(f"  • {rec}")
        lines.append("")
    
    # Footer
    if test_results["success"]:
        lines.append("✅ All tests passing! Ready to continue development.")
    else:
        lines.append("⚠️ Tests need attention before proceeding.")
        lines.append("Focus on making tests pass following TDD principles.")
    
    return "\n".join(lines)


def should_block_completion(test_results: dict) -> bool:
    """
    Determine if the completion should be blocked due to test failures.
    
    Args:
        test_results: Parsed test results
        
    Returns:
        True if completion should be blocked
    """
    # Block if there are test failures
    if test_results["failed"] > 0:
        return True
    
    # Block if coverage is critically low (less than 50%)
    coverage = test_results.get("coverage_percent", 0)
    if coverage < 50:
        return True
    
    # Block if there are test errors
    if test_results["errors"] > 0:
        return True
    
    return False


def main():
    """
    Main hook function called by Claude Code.
    
    This hook runs after Claude finishes a development task and provides
    feedback about test results.
    """
    try:
        # Check if we should run tests
        if not should_run_tests():
            # No tests to run, allow completion
            print(json.dumps({"action": "continue"}))
            return
        
        # Run the tests
        test_output = run_pytest_and_capture(coverage=True)
        test_results = parse_test_results(test_output)
        
        # Analyze the results
        analysis = analyze_test_failures(test_results)
        
        # Generate feedback message
        feedback_message = generate_feedback_message(test_results, analysis)
        
        # Determine if we should block completion
        should_block = should_block_completion(test_results)
        
        if should_block:
            # Block completion and ask Claude to fix the tests
            print(json.dumps({
                "action": "continue",
                "feedback": feedback_message,
                "prompt": (
                    "🔴 TDD RED PHASE: Tests are failing and need your attention. "
                    "Please review the test results above and implement the necessary "
                    "changes to make all tests pass. This follows the TDD Red-Green-Refactor "
                    "cycle where we write failing tests first, then implement code to make "
                    "them pass. Once tests are green, you can refactor the code while "
                    "keeping tests passing."
                )
            }))
        else:
            # Tests are passing, allow completion with feedback
            print(json.dumps({
                "action": "continue",
                "message": feedback_message
            }))
    
    except Exception as e:
        # Don't block completion due to hook errors
        error_message = f"⚠️ Test hook error: {str(e)}. Continuing without test validation."
        print(json.dumps({
            "action": "continue",
            "message": error_message
        }))


if __name__ == "__main__":
    main()