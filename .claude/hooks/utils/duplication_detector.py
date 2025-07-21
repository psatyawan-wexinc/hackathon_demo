#!/usr/bin/env python3
"""
Code duplication detection utility for Claude Code Hooks

Detects code duplication across the codebase and provides suggestions
for refactoring to maintain DRY principles.
"""

import ast
import hashlib
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

from .file_utils import find_python_files, get_use_case_root


class CodeBlock:
    """Represents a block of code for duplication analysis."""
    
    def __init__(self, content: str, file_path: str, start_line: int, end_line: int):
        self.content = content.strip()
        self.file_path = file_path
        self.start_line = start_line
        self.end_line = end_line
        self.normalized_content = self._normalize_content(content)
        self.hash = self._calculate_hash()
        self.line_count = end_line - start_line + 1
    
    def _normalize_content(self, content: str) -> str:
        """Normalize content for comparison by removing whitespace and comments."""
        # Remove comments
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
        
        # Remove extra whitespace
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        # Remove string literals for structural comparison
        content = re.sub(r'["\'].*?["\']', '""', content)
        
        return content
    
    def _calculate_hash(self) -> str:
        """Calculate a hash of the normalized content."""
        return hashlib.md5(self.normalized_content.encode()).hexdigest()
    
    def similarity_score(self, other: 'CodeBlock') -> float:
        """Calculate similarity score with another code block (0.0 to 1.0)."""
        if self.hash == other.hash:
            return 1.0
        
        # Use a simple similarity measure based on common tokens
        tokens1 = set(self.normalized_content.split())
        tokens2 = set(other.normalized_content.split())
        
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))
        
        return intersection / union if union > 0 else 0.0
    
    def __repr__(self):
        return f"CodeBlock({self.file_path}:{self.start_line}-{self.end_line})"


class DuplicationDetector:
    """Detects code duplication in Python files."""
    
    def __init__(self, min_lines: int = 3, similarity_threshold: float = 0.8):
        self.min_lines = min_lines
        self.similarity_threshold = similarity_threshold
        self.code_blocks = []
        self.duplications = []
    
    def analyze_directory(self, directory: str) -> List[Dict]:
        """
        Analyze all Python files in a directory for duplications.
        
        Args:
            directory: Directory to analyze
            
        Returns:
            List of duplication reports
        """
        self.code_blocks = []
        self.duplications = []
        
        python_files = find_python_files(directory)
        
        for file_path in python_files:
            # Skip test files and __init__.py files
            if self._should_skip_file(file_path):
                continue
            
            self._extract_code_blocks(file_path)
        
        self._find_duplications()
        return self._generate_report()
    
    def analyze_file(self, file_path: str) -> List[Dict]:
        """
        Analyze a specific file for duplications with existing codebase.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            List of duplication reports
        """
        # First analyze the entire codebase to build a baseline
        use_case_root = get_use_case_root()
        src_directory = os.path.join(use_case_root, "src")
        
        if os.path.exists(src_directory):
            self.analyze_directory(src_directory)
        
        # Then analyze the specific file
        if not self._should_skip_file(file_path):
            file_blocks = self._extract_code_blocks(file_path)
            
            # Find duplications involving the new file
            new_duplications = []
            for new_block in file_blocks:
                for existing_block in self.code_blocks:
                    if (existing_block.file_path != new_block.file_path and
                        new_block.similarity_score(existing_block) >= self.similarity_threshold):
                        new_duplications.append({
                            "block1": new_block,
                            "block2": existing_block,
                            "similarity": new_block.similarity_score(existing_block),
                            "type": "cross_file"
                        })
            
            return self._format_duplications(new_duplications)
        
        return []
    
    def _should_skip_file(self, file_path: str) -> bool:
        """Check if a file should be skipped during analysis."""
        filename = os.path.basename(file_path)
        
        # Skip test files, __init__.py, and hook files
        skip_patterns = [
            "__init__.py",
            "test_",
            "conftest.py",
            "_test.py",
            "/.claude/hooks/",
            "/migrations/",
            "/alembic/"
        ]
        
        return any(pattern in file_path for pattern in skip_patterns)
    
    def _extract_code_blocks(self, file_path: str) -> List[CodeBlock]:
        """Extract code blocks from a Python file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
            
            tree = ast.parse(content)
            blocks = []
            
            # Extract function and class definitions
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)):
                    start_line = node.lineno
                    end_line = node.end_lineno or start_line
                    
                    if end_line - start_line + 1 >= self.min_lines:
                        block_content = '\n'.join(lines[start_line-1:end_line])
                        block = CodeBlock(block_content, file_path, start_line, end_line)
                        blocks.append(block)
                        self.code_blocks.append(block)
            
            # Extract significant code blocks (consecutive non-empty lines)
            self._extract_statement_blocks(file_path, lines)
            
            return blocks
            
        except Exception as e:
            print(f"Error analyzing file {file_path}: {str(e)}")
            return []
    
    def _extract_statement_blocks(self, file_path: str, lines: List[str]) -> None:
        """Extract blocks of consecutive statements."""
        current_block = []
        start_line = 0
        
        for i, line in enumerate(lines):
            stripped_line = line.strip()
            
            # Skip empty lines, comments, and imports
            if (not stripped_line or 
                stripped_line.startswith('#') or 
                stripped_line.startswith('import ') or 
                stripped_line.startswith('from ') or
                stripped_line.startswith('"""') or
                stripped_line.startswith("'''")):
                
                if current_block and len(current_block) >= self.min_lines:
                    # End current block
                    block_content = '\n'.join(current_block)
                    block = CodeBlock(block_content, file_path, start_line + 1, i)
                    self.code_blocks.append(block)
                
                current_block = []
                start_line = i + 1
            else:
                current_block.append(line)
        
        # Handle final block
        if current_block and len(current_block) >= self.min_lines:
            block_content = '\n'.join(current_block)
            block = CodeBlock(block_content, file_path, start_line + 1, len(lines))
            self.code_blocks.append(block)
    
    def _find_duplications(self) -> None:
        """Find duplications among extracted code blocks."""
        self.duplications = []
        processed_pairs = set()
        
        for i, block1 in enumerate(self.code_blocks):
            for j, block2 in enumerate(self.code_blocks[i+1:], i+1):
                # Skip if same file and overlapping lines
                if (block1.file_path == block2.file_path and 
                    self._blocks_overlap(block1, block2)):
                    continue
                
                # Skip if already processed
                pair_key = (min(i, j), max(i, j))
                if pair_key in processed_pairs:
                    continue
                processed_pairs.add(pair_key)
                
                similarity = block1.similarity_score(block2)
                if similarity >= self.similarity_threshold:
                    duplication_type = "same_file" if block1.file_path == block2.file_path else "cross_file"
                    
                    self.duplications.append({
                        "block1": block1,
                        "block2": block2,
                        "similarity": similarity,
                        "type": duplication_type
                    })
    
    def _blocks_overlap(self, block1: CodeBlock, block2: CodeBlock) -> bool:
        """Check if two blocks overlap in line numbers."""
        return not (block1.end_line < block2.start_line or block2.end_line < block1.start_line)
    
    def _generate_report(self) -> List[Dict]:
        """Generate a detailed duplication report."""
        return self._format_duplications(self.duplications)
    
    def _format_duplications(self, duplications: List[Dict]) -> List[Dict]:
        """Format duplications for reporting."""
        formatted_duplications = []
        
        for dup in duplications:
            block1 = dup["block1"]
            block2 = dup["block2"]
            
            # Calculate severity based on line count and similarity
            severity = self._calculate_severity(block1, block2, dup["similarity"])
            
            # Generate refactoring suggestions
            suggestions = self._generate_refactoring_suggestions(block1, block2)
            
            formatted_duplications.append({
                "severity": severity,
                "similarity": dup["similarity"],
                "type": dup["type"],
                "blocks": [
                    {
                        "file": block1.file_path,
                        "lines": f"{block1.start_line}-{block1.end_line}",
                        "line_count": block1.line_count,
                        "content_preview": block1.content[:200] + "..." if len(block1.content) > 200 else block1.content
                    },
                    {
                        "file": block2.file_path,
                        "lines": f"{block2.start_line}-{block2.end_line}",
                        "line_count": block2.line_count,
                        "content_preview": block2.content[:200] + "..." if len(block2.content) > 200 else block2.content
                    }
                ],
                "suggestions": suggestions
            })
        
        # Sort by severity (high to low)
        severity_order = {"high": 3, "medium": 2, "low": 1}
        formatted_duplications.sort(key=lambda x: severity_order.get(x["severity"], 0), reverse=True)
        
        return formatted_duplications
    
    def _calculate_severity(self, block1: CodeBlock, block2: CodeBlock, similarity: float) -> str:
        """Calculate the severity of a duplication."""
        avg_lines = (block1.line_count + block2.line_count) / 2
        
        if similarity >= 0.95 and avg_lines >= 10:
            return "high"
        elif similarity >= 0.85 and avg_lines >= 5:
            return "medium"
        else:
            return "low"
    
    def _generate_refactoring_suggestions(self, block1: CodeBlock, block2: CodeBlock) -> List[str]:
        """Generate refactoring suggestions for duplicated code."""
        suggestions = []
        
        # Determine the type of duplication and suggest appropriate refactoring
        if "def " in block1.normalized_content:
            suggestions.append("Extract common logic into a shared utility function")
            suggestions.append("Consider creating a base class with shared methods")
        elif "class " in block1.normalized_content:
            suggestions.append("Extract common functionality into a mixin or base class")
            suggestions.append("Consider composition over inheritance")
        else:
            suggestions.append("Extract common code into a shared utility function")
            suggestions.append("Consider using a configuration-driven approach")
        
        # Add file-specific suggestions
        if block1.file_path != block2.file_path:
            suggestions.append("Move shared code to a common utilities module")
        else:
            suggestions.append("Refactor within the same file to reduce duplication")
        
        return suggestions


def detect_duplications_in_file(file_path: str, min_lines: int = 3, similarity_threshold: float = 0.8) -> Dict:
    """
    Detect duplications for a specific file.
    
    Args:
        file_path: Path to the file to analyze
        min_lines: Minimum number of lines for a duplication
        similarity_threshold: Minimum similarity score (0.0 to 1.0)
        
    Returns:
        Dictionary with duplication analysis results
    """
    detector = DuplicationDetector(min_lines, similarity_threshold)
    duplications = detector.analyze_file(file_path)
    
    # Calculate summary statistics
    total_duplications = len(duplications)
    high_severity = len([d for d in duplications if d["severity"] == "high"])
    medium_severity = len([d for d in duplications if d["severity"] == "medium"])
    low_severity = len([d for d in duplications if d["severity"] == "low"])
    
    return {
        "file": file_path,
        "total_duplications": total_duplications,
        "high_severity": high_severity,
        "medium_severity": medium_severity,
        "low_severity": low_severity,
        "duplications": duplications,
        "dry_score": calculate_dry_score(duplications),
        "recommendations": generate_dry_recommendations(duplications)
    }


def calculate_dry_score(duplications: List[Dict]) -> int:
    """
    Calculate a DRY compliance score (0-100).
    
    Args:
        duplications: List of duplication reports
        
    Returns:
        DRY score from 0 (many duplications) to 100 (no duplications)
    """
    if not duplications:
        return 100
    
    # Weight by severity
    penalty = 0
    for dup in duplications:
        if dup["severity"] == "high":
            penalty += 20
        elif dup["severity"] == "medium":
            penalty += 10
        else:
            penalty += 5
    
    score = max(0, 100 - penalty)
    return score


def generate_dry_recommendations(duplications: List[Dict]) -> List[str]:
    """
    Generate DRY improvement recommendations.
    
    Args:
        duplications: List of duplication reports
        
    Returns:
        List of actionable recommendations
    """
    if not duplications:
        return ["Code follows DRY principles well - no significant duplications found"]
    
    recommendations = []
    
    high_severity = [d for d in duplications if d["severity"] == "high"]
    if high_severity:
        recommendations.append(f"Address {len(high_severity)} high-severity duplications immediately")
        recommendations.append("Extract common functions and classes to shared utilities")
    
    medium_severity = [d for d in duplications if d["severity"] == "medium"]
    if medium_severity:
        recommendations.append(f"Refactor {len(medium_severity)} medium-severity duplications")
        recommendations.append("Consider creating base classes or mixins for shared behavior")
    
    cross_file_dups = [d for d in duplications if d["type"] == "cross_file"]
    if cross_file_dups:
        recommendations.append("Move shared code to common utility modules")
        recommendations.append("Establish clear separation of concerns between modules")
    
    return recommendations