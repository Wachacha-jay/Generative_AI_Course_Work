"""
Repo Mapper Agent - Handles repository cloning and file-tree generation.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

from utils.git_utils import GitManager
from utils.language_detector import LanguageDetector


@dataclass
class FileNode:
    """Represents a file in the repository tree."""
    name: str
    path: str
    type: str  # 'file' or 'directory'
    size: int
    language: Optional[str] = None
    children: Optional[List['FileNode']] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = asdict(self)
        if self.children:
            result['children'] = [child.to_dict() for child in self.children]
        return result


@dataclass
class RepoMap:
    """Repository mapping structure."""
    repo_info: Dict[str, Any]
    file_tree: FileNode
    readme_summary: Optional[str] = None
    language_detection: Optional[Dict[str, Any]] = None
    entry_points: List[str] = None
    
    def __post_init__(self):
        if self.entry_points is None:
            self.entry_points = []


class RepoMapper:
    """Maps repository structure and extracts key information."""
    
    def __init__(self):
        self.git_manager = GitManager()
        self.language_detector = LanguageDetector()
        self.ignore_patterns = {
            '.git', 'node_modules', '__pycache__', '.pytest_cache',
            'venv', 'env', '.venv', '.env', 'build', 'dist',
            'target', '.cargo', '.idea', '.vscode', '.vs',
            'coverage', '.coverage', 'htmlcov', '.tox',
            'site-packages', '.mypy_cache', '.ruff_cache',
            '.gitignore', '.dockerignore', '.DS_Store',
            'Thumbs.db', '*.pyc', '*.pyo', '*.pyd'
        }
    
    def map_repository(self, repo_url: str, branch: Optional[str] = None) -> RepoMap:
        """
        Map a repository and extract key information.
        
        Args:
            repo_url: GitHub repository URL
            branch: Specific branch to analyze
            
        Returns:
            RepoMap object with repository information
        """
        # Clone repository
        clone_result = self.git_manager.clone_repository(repo_url, branch)
        if not clone_result['success']:
            raise Exception(f"Failed to clone repository: {clone_result['error']}")
        
        local_path = clone_result['local_path']
        
        try:
            # Generate file tree
            file_tree = self._generate_file_tree(local_path)
            
            # Detect languages
            language_detection = self.language_detector.detect_languages_in_repo(local_path)
            
            # Extract README summary
            readme_summary = self._extract_readme_summary(local_path)
            
            # Find entry points
            entry_points = self._find_entry_points(local_path, language_detection['primary_language'])
            
            return RepoMap(
                repo_info=clone_result['repo_info'],
                file_tree=file_tree,
                readme_summary=readme_summary,
                language_detection=language_detection,
                entry_points=entry_points
            )
            
        except Exception as e:
            # Cleanup on error
            self.git_manager.cleanup_repository(repo_url)
            raise Exception(f"Failed to map repository: {str(e)}")
    
    def _generate_file_tree(self, repo_path: str) -> FileNode:
        """Generate a file tree structure."""
        repo_path = Path(repo_path)
        return self._build_tree_node(repo_path, repo_path)
    
    def _build_tree_node(self, root_path: Path, current_path: Path) -> FileNode:
        """Recursively build tree node."""
        is_dir = current_path.is_dir()
        
        # Get file size
        size = 0
        if is_dir:
            try:
                size = sum(f.stat().st_size for f in current_path.rglob('*') if f.is_file())
            except:
                size = 0
        else:
            try:
                size = current_path.stat().st_size
            except:
                size = 0
        
        # Detect language for files
        language = None
        if not is_dir and current_path.suffix:
            language = self.language_detector._detect_file_language(current_path)
        
        # Create node
        node = FileNode(
            name=current_path.name,
            path=str(current_path.relative_to(root_path)),
            type='directory' if is_dir else 'file',
            size=size,
            language=language
        )
        
        # Add children for directories
        if is_dir:
            children = []
            try:
                for item in sorted(current_path.iterdir()):
                    # Skip ignored items
                    if self._should_ignore(item):
                        continue
                    
                    child_node = self._build_tree_node(root_path, item)
                    children.append(child_node)
                
                node.children = children
            except PermissionError:
                # Skip directories we can't read
                pass
        
        return node
    
    def _should_ignore(self, path: Path) -> bool:
        """Check if a path should be ignored."""
        path_str = str(path)
        
        # Check against ignore patterns
        for pattern in self.ignore_patterns:
            if pattern.startswith('*'):
                # Wildcard pattern
                if path_str.endswith(pattern[1:]):
                    return True
            else:
                # Exact match or directory
                if pattern in path.parts or path.name == pattern:
                    return True
        
        return False
    
    def _extract_readme_summary(self, repo_path: str) -> Optional[str]:
        """Extract and summarize README content."""
        repo_path = Path(repo_path)
        
        # Look for README files
        readme_files = [
            'README.md', 'README.rst', 'README.txt', 'README',
            'readme.md', 'readme.rst', 'readme.txt', 'readme'
        ]
        
        for readme_file in readme_files:
            readme_path = repo_path / readme_file
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        return self._summarize_readme(content)
                except:
                    continue
        
        return None
    
    def _summarize_readme(self, content: str) -> str:
        """Summarize README content."""
        lines = content.split('\n')
        
        # Find the first meaningful section
        summary_lines = []
        in_code_block = False
        
        for line in lines[:50]:  # Only look at first 50 lines
            line = line.strip()
            
            # Skip empty lines and code blocks
            if not line:
                continue
            
            if line.startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                continue
            
            # Skip headers and metadata
            if line.startswith('#') or line.startswith('[') or line.startswith('|'):
                continue
            
            summary_lines.append(line)
            
            # Stop after getting enough content
            if len(summary_lines) >= 5:
                break
        
        return ' '.join(summary_lines)[:500] + '...' if len(' '.join(summary_lines)) > 500 else ' '.join(summary_lines)
    
    def _find_entry_points(self, repo_path: str, primary_language: str) -> List[str]:
        """Find entry point files based on language."""
        repo_path = Path(repo_path)
        entry_points = []
        
        # Language-specific entry point patterns
        entry_patterns = {
            'python': ['main.py', 'app.py', 'run.py', '__main__.py', 'setup.py'],
            'jac': ['main.jac', 'app.jac', 'run.jac'],
            'javascript': ['index.js', 'app.js', 'main.js', 'server.js', 'package.json'],
            'java': ['Main.java', 'App.java', 'Application.java'],
            'cpp': ['main.cpp', 'app.cpp', 'main.c'],
            'rust': ['main.rs', 'lib.rs', 'Cargo.toml'],
            'go': ['main.go', 'app.go', 'go.mod']
        }
        
        patterns = entry_patterns.get(primary_language, [])
        
        for pattern in patterns:
            for file_path in repo_path.rglob(pattern):
                if file_path.is_file():
                    entry_points.append(str(file_path.relative_to(repo_path)))
        
        # Also look for files with main functions/entry points
        if primary_language in ['python', 'javascript', 'java', 'cpp', 'rust', 'go']:
            entry_points.extend(self._find_main_functions(repo_path, primary_language))
        
        return list(set(entry_points))  # Remove duplicates
    
    def _find_main_functions(self, repo_path: Path, language: str) -> List[str]:
        """Find files containing main functions or entry points."""
        entry_files = []
        
        # Language-specific main function patterns
        main_patterns = {
            'python': [r'if\s+__name__\s*==\s*["\']__main__["\']', r'def\s+main\s*\('],
            'javascript': [r'function\s+main\s*\(', r'module\.exports\s*=', r'export\s+default'],
            'java': [r'public\s+static\s+void\s+main\s*\('],
            'cpp': [r'int\s+main\s*\('],
            'rust': [r'fn\s+main\s*\('],
            'go': [r'func\s+main\s*\(']
        }
        
        patterns = main_patterns.get(language, [])
        if not patterns:
            return entry_files
        
        import re
        
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and not self._should_ignore(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1024)  # Read first 1KB
                        
                        for pattern in patterns:
                            if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
                                entry_files.append(str(file_path.relative_to(repo_path)))
                                break
                except:
                    continue
        
        return entry_files
    
    def cleanup(self, repo_url: str) -> bool:
        """Clean up cloned repository."""
        return self.git_manager.cleanup_repository(repo_url)
    
    def get_repo_path(self, repo_url: str) -> Optional[str]:
        """Get local path of cloned repository."""
        return self.git_manager.get_repo_path(repo_url)


def map_repository(repo_url: str, branch: Optional[str] = None) -> RepoMap:
    """
    Convenience function to map a repository.
    
    Args:
        repo_url: GitHub repository URL
        branch: Specific branch to analyze
        
    Returns:
        RepoMap object
    """
    mapper = RepoMapper()
    return mapper.map_repository(repo_url, branch)