"""
Python utilities for Jac language integration.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional
import base64
from io import BytesIO
from byllm.llm import Model 

# Import our existing modules
from utils.language_detector import LanguageDetector
from utils.git_utils import GitManager
from agents.repo_mapper import RepoMapper
from agents.code_analyzer import CodeAnalyzer
from agents.doc_genie import DocGenie

llm = Model(model_name="gemini/gemini-2.0-flash")

class JacCodebaseGenius:
    """Main class for Jac integration."""
    
    def __init__(self):
        self.git_manager = GitManager()
        self.repo_mapper = RepoMapper()
        self.code_analyzer = CodeAnalyzer()
        self.doc_genie = DocGenie()
        self.language_detector = LanguageDetector()
    
    def map_repository(self, repo_url: str, branch: Optional[str] = None) -> Dict[str, Any]:
        """Map repository structure."""
        try:
            # Clone repository
            clone_result = self.git_manager.clone_repository(repo_url, branch)
            if not clone_result['success']:
                return {
                    "success": False,
                    "error": clone_result['error'],
                    "message": f"Failed to clone repository: {clone_result['error']}"
                }
            
            local_path = clone_result['local_path']
            
            # Detect languages
            lang_detection = self.language_detector.detect_languages_in_repo(local_path)
            
            # Generate file tree
            file_tree = self.repo_mapper._generate_file_tree(local_path)

            # get repository name
            repo_name = clone_result['repo_name']
            
            # Find entry points
            entry_points = self.repo_mapper._find_entry_points(
                local_path, 
                lang_detection['primary_language']
            )
            
            # Extract README summary
            readme_summary = self.repo_mapper._extract_readme_summary(local_path)
            
            return {
                "success": True,
                "repo_name": repo_name,
                "repo_info": clone_result['repo_info'],
                "local_path": local_path,
                "language_detection": lang_detection,
                "file_tree": file_tree.to_dict() if hasattr(file_tree, 'to_dict') else str(file_tree),
                "entry_points": entry_points,
                "readme_summary": readme_summary,
                "message": "Repository mapping completed successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Repository mapping failed: {str(e)}"
            }
    
    def analyze_codebase(self, repo_path: str, language: str, entry_points: List[str]) -> Dict[str, Any]:
        """Analyze codebase structure."""
        try:
            ccg = self.code_analyzer.analyze_codebase(repo_path, language, entry_points)
            
            return {
                "ccg": ccg,
                "success": True,
                "elements": {k: v.to_dict() for k, v in ccg.elements.items()},
                "relationships": ccg.relationships,
                "graph_nodes": list(ccg.graph.nodes()),
                "graph_edges": list(ccg.graph.edges()),
                "message": "Code analysis completed successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Code analysis failed: {str(e)}"
            }
    
    def generate_documentation(self, repo_map: Dict[str, Any], ccg: Dict[str, Any], repo_name: str) -> Dict[str, Any]:
        """Generate documentation."""
        try:
            # Convert dict back to objects for DocGenie
            # This is a simplified approach - in practice, you'd need proper object reconstruction
            
            # Create mock objects for DocGenie
            class MockRepoMap:
                def __init__(self, data):
                    self.repo_info = data.get('repo_info', {})
                    self.language_detection = data.get('language_detection', {})
                    self.entry_points = data.get('entry_points', [])
                    self.readme_summary = data.get('readme_summary', '')
                    self.file_tree = data.get('file_tree', {})
            
            class MockCCG:
                def __init__(self, data):
                    self.elements = {k: MockElement(v) for k, v in data.get('elements', {}).items()}
                    self.relationships = data.get('relationships', [])
                    self.graph = None  # Simplified for now
            
            class MockElement:
                def __init__(self, data):
                    self.name = data.get('name', '')
                    self.type = data.get('type', '')
                    self.file_path = data.get('file_path', '')
                    self.line_start = data.get('line_start', 0)
                    self.line_end = data.get('line_end', 0)
                    self.docstring = data.get('docstring', '')
                    self.parameters = data.get('parameters', [])
                    self.return_type = data.get('return_type', '')
                    self.parent = data.get('parent', '')
            
            mock_repo_map = MockRepoMap(repo_map)
            mock_ccg = MockCCG(ccg)
            
            # Generate documentation
            documentation = self.doc_genie.generate_documentation(
                repo_map=mock_repo_map,
                ccg=mock_ccg,
                repo_name=repo_name
            )
            
            return {
                "success": True,
                "documentation": {
                    "title": documentation.title,
                    "sections": [
                        {
                            "title": section.title,
                            "content": section.content,
                            "level": section.level
                        }
                        for section in documentation.sections
                    ],
                    "diagrams": documentation.diagrams,
                    "metadata": documentation.metadata
                },
                "message": "Documentation generation completed successfully"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"Documentation generation failed: {str(e)}"
            }
    
    def enhance_documentation_with_llm(self, documentation: Dict[str, Any], repo_map: Dict[str, Any], ccg: Dict[str, Any]) -> Dict[str, Any]:
        """Enhance documentation using LLM."""
        try:
            # This would integrate with byLLM
            # For now, we'll return the original documentation
            return documentation
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": f"LLM enhancement failed: {str(e)}"
            }
    
    def save_documentation(self, documentation: Dict[str, Any], repo_name: str) -> str:
        """Save documentation to file."""
        try:
            # Create output directory
            output_dir = Path("outputs") / repo_name
            output_dir.mkdir(exist_ok=True)
            
            # Generate markdown content
            markdown_content = self._generate_markdown(documentation)
            
            # Save markdown file
            md_file = output_dir / "docs.md"
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            return str(md_file)
            
        except Exception as e:
            raise Exception(f"Failed to save documentation: {str(e)}")
    
    def _generate_markdown(self, documentation: Dict[str, Any]) -> str:
        """Generate markdown content from documentation."""
        content = []
        
        # Title
        content.append(f"# {documentation['title']}")
        content.append("")
        
        # Table of contents
        content.append("## Table of Contents")
        content.append("")
        for section in documentation['sections']:
            content.append(f"- [{section['title']}](#{section['title'].lower().replace(' ', '-')})")
        content.append("")
        
        # Sections
        for section in documentation['sections']:
            content.append(f"## {section['title']}")
            content.append("")
            content.append(section['content'])
            content.append("")
        
        # Diagrams
        if documentation['diagrams']:
            content.append("## Diagrams")
            content.append("")
            for diagram in documentation['diagrams']:
                content.append(f"### {diagram['name'].replace('_', ' ').title()}")
                content.append("")
                content.append(f"![{diagram['name']}]({diagram['name']}.png)")
                content.append("")
        
        return "\n".join(content)
    
    def cleanup(self, repo_url: str) -> bool:
        """Clean up cloned repository."""
        return self.git_manager.cleanup_repository(repo_url)
    
    def cleanup_all(self) -> None:
        """Clean up all cloned repositories."""
        self.git_manager.cleanup_all()


# Global instance for Jac to use
jac_genius = JacCodebaseGenius()


# Convenience functions for Jac
def map_repository(repo_url: str, branch: Optional[str] = None) -> Dict[str, Any]:
    """Map a repository."""
    return jac_genius.map_repository(repo_url, branch)


def analyze_codebase(repo_path: str, language: str, entry_points: List[str]) -> Dict[str, Any]:
    """Analyze a codebase."""
    return jac_genius.analyze_codebase(repo_path, language, entry_points)


def generate_documentation(repo_map: Dict[str, Any], ccg: Dict[str, Any], repo_name: str) -> Dict[str, Any]:
    """Generate documentation."""
    return jac_genius.generate_documentation(repo_map, ccg, repo_name)


def save_documentation(documentation: Dict[str, Any], repo_name: str) -> str:
    """Save documentation."""
    return jac_genius.save_documentation(documentation, repo_name)


def cleanup_repository(repo_url: str) -> bool:
    """Clean up repository."""
    return jac_genius.cleanup(repo_url)