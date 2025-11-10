"""
Language detection utilities for multi-language codebase analysis.
"""

import os
import re
from typing import Dict, List, Optional, Set
from pathlib import Path


class LanguageDetector:
    """Detects programming languages in a codebase."""
    
    # File extensions mapped to languages
    EXTENSION_MAP = {
        '.py': 'python',
        '.jac': 'jac',
        '.js': 'javascript',
        '.jsx': 'javascript',
        '.ts': 'typescript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.c': 'c',
        '.h': 'c',
        '.hpp': 'cpp',
        '.rs': 'rust',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.r': 'r',
        '.m': 'matlab',
        '.jl': 'julia',
        '.sh': 'shell',
        '.bash': 'shell',
        '.zsh': 'shell',
        '.fish': 'shell',
        '.ps1': 'powershell',
        '.bat': 'batch',
        '.cmd': 'batch',
        '.sql': 'sql',
        '.html': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.sass': 'sass',
        '.less': 'less',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.json': 'json',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'config',
        '.conf': 'config',
        '.dockerfile': 'dockerfile',
        '.dockerignore': 'dockerignore',
        '.gitignore': 'gitignore',
        '.md': 'markdown',
        '.rst': 'restructuredtext',
        '.tex': 'latex',
        '.txt': 'text',
    }
    
    # Language-specific patterns for detection
    LANGUAGE_PATTERNS = {
        'python': [
            r'^#!/usr/bin/env python',
            r'^#!/usr/bin/python',
            r'import\s+\w+',
            r'from\s+\w+\s+import',
            r'def\s+\w+\s*\(',
            r'class\s+\w+',
        ],
        'jac': [
            r'node\s+\w+',
            r'walker\s+\w+',
            r'edge\s+\w+',
            r'graph\s+\w+',
            r'can\s+\w+',
            r'with\s+entry',
        ],
        'javascript': [
            r'^#!/usr/bin/env node',
            r'^#!/usr/bin/node',
            r'function\s+\w+\s*\(',
            r'const\s+\w+\s*=',
            r'let\s+\w+\s*=',
            r'var\s+\w+\s*=',
            r'=>\s*{',
            r'require\s*\(',
            r'import\s+.*from',
        ],
        'java': [
            r'public\s+class\s+\w+',
            r'package\s+\w+',
            r'import\s+\w+',
            r'public\s+static\s+void\s+main',
            r'@Override',
            r'@Component',
            r'@Service',
        ],
        'cpp': [
            r'#include\s*<.*>',
            r'#include\s*".*"',
            r'using\s+namespace\s+\w+',
            r'class\s+\w+\s*{',
            r'int\s+main\s*\(',
            r'std::',
        ],
        'rust': [
            r'use\s+\w+',
            r'fn\s+\w+\s*\(',
            r'struct\s+\w+',
            r'impl\s+\w+',
            r'let\s+\w+\s*=',
            r'match\s+\w+',
        ],
        'go': [
            r'package\s+\w+',
            r'import\s+\(',
            r'func\s+\w+\s*\(',
            r'type\s+\w+\s+struct',
            r'interface\s+\w+',
            r'var\s+\w+\s*=',
        ],
    }
    
    def __init__(self):
        self.detected_languages: Set[str] = set()
        self.file_counts: Dict[str, int] = {}
    
    def detect_languages_in_repo(self, repo_path: str) -> Dict[str, any]:
        """
        Detect all programming languages in a repository.
        
        Args:
            repo_path: Path to the repository
            
        Returns:
            Dictionary with language detection results
        """
        repo_path = Path(repo_path)
        if not repo_path.exists():
            raise ValueError(f"Repository path does not exist: {repo_path}")
        
        self.detected_languages.clear()
        self.file_counts.clear()
        
        # Scan all files
        for file_path in self._get_code_files(repo_path):
            language = self._detect_file_language(file_path)
            if language:
                self.detected_languages.add(language)
                self.file_counts[language] = self.file_counts.get(language, 0) + 1
        
        # Determine primary language
        primary_language = self._get_primary_language()
        
        return {
            'primary_language': primary_language,
            'detected_languages': list(self.detected_languages),
            'file_counts': self.file_counts,
            'total_files': sum(self.file_counts.values()),
            'confidence': self._calculate_confidence()
        }
    
    def _get_code_files(self, repo_path: Path) -> List[Path]:
        """Get all code files, excluding common non-code directories."""
        code_files = []
        exclude_dirs = {
            '.git', 'node_modules', '__pycache__', '.pytest_cache',
            'venv', 'env', '.venv', '.env', 'build', 'dist',
            'target', '.cargo', '.idea', '.vscode', '.vs',
            'coverage', '.coverage', 'htmlcov', '.tox',
            'site-packages', '.mypy_cache', '.ruff_cache'
        }
        
        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                # Skip excluded directories
                if any(excluded in file_path.parts for excluded in exclude_dirs):
                    continue
                
                # Skip binary files and very large files
                if self._is_binary_file(file_path) or file_path.stat().st_size > 10 * 1024 * 1024:
                    continue
                
                code_files.append(file_path)
        
        return code_files
    
    def _is_binary_file(self, file_path: Path) -> bool:
        """Check if a file is binary."""
        try:
            with open(file_path, 'rb') as f:
                chunk = f.read(1024)
                return b'\0' in chunk
        except:
            return True
    
    def _detect_file_language(self, file_path: Path) -> Optional[str]:
        """Detect language of a single file."""
        # First try extension-based detection
        extension = file_path.suffix.lower()
        if extension in self.EXTENSION_MAP:
            return self.EXTENSION_MAP[extension]
        
        # Try content-based detection for files without clear extensions
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read(1024)  # Read first 1KB
                
                for language, patterns in self.LANGUAGE_PATTERNS.items():
                    for pattern in patterns:
                        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                            return language
        except:
            pass
        
        return None
    
    def _get_primary_language(self) -> str:
        """Determine the primary language based on file counts."""
        if not self.file_counts:
            return 'unknown'
        
        # Sort by file count
        sorted_languages = sorted(
            self.file_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return sorted_languages[0][0]
    
    def _calculate_confidence(self) -> float:
        """Calculate confidence score for language detection."""
        if not self.file_counts:
            return 0.0
        
        total_files = sum(self.file_counts.values())
        if total_files == 0:
            return 0.0
        
        # Confidence based on how dominant the primary language is
        primary_count = max(self.file_counts.values())
        return primary_count / total_files
    
    def get_language_info(self, language: str) -> Dict[str, str]:
        """Get information about a specific language."""
        language_info = {
            'python': {
                'name': 'Python',
                'description': 'High-level programming language with dynamic semantics',
                'parser': 'tree-sitter-python',
                'extensions': ['.py', '.pyi', '.pyc', '.pyo']
            },
            'jac': {
                'name': 'Jac',
                'description': 'Multi-paradigm programming language for AI applications',
                'parser': 'custom',
                'extensions': ['.jac']
            },
            'javascript': {
                'name': 'JavaScript',
                'description': 'High-level, interpreted programming language',
                'parser': 'tree-sitter-javascript',
                'extensions': ['.js', '.jsx', '.mjs']
            },
            'java': {
                'name': 'Java',
                'description': 'Object-oriented programming language',
                'parser': 'tree-sitter-java',
                'extensions': ['.java', '.class', '.jar']
            },
            'cpp': {
                'name': 'C++',
                'description': 'General-purpose programming language',
                'parser': 'tree-sitter-cpp',
                'extensions': ['.cpp', '.cc', '.cxx', '.hpp', '.h']
            },
            'rust': {
                'name': 'Rust',
                'description': 'Systems programming language focused on safety',
                'parser': 'tree-sitter-rust',
                'extensions': ['.rs']
            },
            'go': {
                'name': 'Go',
                'description': 'Statically typed, compiled programming language',
                'parser': 'tree-sitter-go',
                'extensions': ['.go']
            }
        }
        
        return language_info.get(language, {
            'name': language.title(),
            'description': 'Unknown programming language',
            'parser': 'unknown',
            'extensions': []
        })


def detect_repository_language(repo_path: str) -> Dict[str, any]:
    """
    Convenience function to detect languages in a repository.
    
    Args:
        repo_path: Path to the repository
        
    Returns:
        Language detection results
    """
    detector = LanguageDetector()
    return detector.detect_languages_in_repo(repo_path)