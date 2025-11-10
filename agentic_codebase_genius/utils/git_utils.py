"""
Git utilities for repository cloning and management.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
import git
from git import Repo, InvalidGitRepositoryError


class GitManager:
    """Manages Git repository operations."""
    
    def __init__(self, temp_dir: Optional[str] = None):
        """
        Initialize Git manager.
        
        Args:
            temp_dir: Temporary directory for cloning repos. If None, uses system temp.
        """
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.cloned_repos: Dict[str, str] = {}  # URL -> local path mapping
    
    def clone_repository(self, repo_url: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """
        Clone a repository to a temporary directory.
        
        Args:
            repo_url: GitHub repository URL
            branch: Specific branch to clone (default: main/master)
            
        Returns:
            Dictionary with clone information
        """
        try:
            # Validate URL
            if not self._is_valid_github_url(repo_url):
                raise ValueError(f"Invalid GitHub URL: {repo_url}")
            
            # Create unique directory name
            repo_name = self._extract_repo_name(repo_url)
            clone_dir = Path(self.temp_dir) / f"codebase_genius_{repo_name}"
            
            # Remove existing directory if it exists
            if clone_dir.exists():
                shutil.rmtree(clone_dir)
            
            # Clone repository
            print(f"Cloning repository: {repo_url}")
            repo = Repo.clone_from(repo_url, clone_dir)
            
            # Checkout specific branch if provided
            if branch:
                try:
                    repo.git.checkout(branch)
                except git.exc.GitCommandError:
                    print(f"Warning: Could not checkout branch '{branch}', using default")
            
            # Store mapping
            self.cloned_repos[repo_url] = str(clone_dir)
            
            # Get repository information
            repo_info = self._get_repo_info(repo, repo_url)
            
            return {
                'success': True,
                'local_path': str(clone_dir),
                'repo_name': repo_name,
                'repo_info': repo_info,
                'message': f"Successfully cloned {repo_url}"
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f"Failed to clone {repo_url}: {str(e)}"
            }
    
    def cleanup_repository(self, repo_url: str) -> bool:
        """
        Clean up a cloned repository.
        
        Args:
            repo_url: Repository URL to clean up
            
        Returns:
            True if cleanup was successful
        """
        if repo_url in self.cloned_repos:
            local_path = self.cloned_repos[repo_url]
            try:
                if Path(local_path).exists():
                    shutil.rmtree(local_path)
                del self.cloned_repos[repo_url]
                return True
            except Exception as e:
                print(f"Error cleaning up {local_path}: {e}")
                return False
        return False
    
    def cleanup_all(self) -> None:
        """Clean up all cloned repositories."""
        for repo_url in list(self.cloned_repos.keys()):
            self.cleanup_repository(repo_url)
    
    def _is_valid_github_url(self, url: str) -> bool:
        """Check if URL is a valid GitHub repository URL."""
        github_patterns = [
            r'https://github\.com/[^/]+/[^/]+/?$',
            r'git@github\.com:[^/]+/[^/]+\.git$'
        ]
        
        import re
        return any(re.match(pattern, url) for pattern in github_patterns)
    
    def _extract_repo_name(self, url: str) -> str:
        """Extract repository name from URL."""
        if url.endswith('.git'):
            url = url[:-4]
        
        if url.startswith('git@github.com:'):
            url = url.replace('git@github.com:', 'https://github.com/')
        
        parts = url.rstrip('/').split('/')
        if len(parts) >= 2:
            return f"{parts[-2]}_{parts[-1]}"
        
        return "unknown_repo"
    
    def _get_repo_info(self, repo: Repo, repo_url: str) -> Dict[str, Any]:
        """Get repository information."""
        try:
            # Get current branch
            current_branch = repo.active_branch.name if not repo.head.is_detached else "detached"
            
            # Get commit info
            commit = repo.head.commit
            commit_info = {
                'hash': commit.hexsha[:8],
                'message': commit.message.strip().split('\n')[0],
                'author': commit.author.name,
                'date': commit.committed_datetime.isoformat()
            }
            
            # Get remote info
            remote_info = {}
            for remote in repo.remotes:
                remote_info[remote.name] = remote.url
            
            # Get file count
            file_count = len([f for f in repo.tree().traverse() if f.type == 'blob'])
            
            return {
                'url': repo_url,
                'branch': current_branch,
                'commit': commit_info,
                'remotes': remote_info,
                'file_count': file_count,
                'is_dirty': repo.is_dirty()
            }
            
        except Exception as e:
            return {
                'url': repo_url,
                'error': f"Could not get repo info: {str(e)}"
            }
    
    def get_repo_path(self, repo_url: str) -> Optional[str]:
        """Get local path of a cloned repository."""
        return self.cloned_repos.get(repo_url)
    
    def is_repo_cloned(self, repo_url: str) -> bool:
        """Check if a repository is already cloned."""
        return repo_url in self.cloned_repos


def clone_repository(repo_url: str, branch: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to clone a repository.
    
    Args:
        repo_url: GitHub repository URL
        branch: Specific branch to clone
        
    Returns:
        Clone result dictionary
    """
    manager = GitManager()
    return manager.clone_repository(repo_url, branch)