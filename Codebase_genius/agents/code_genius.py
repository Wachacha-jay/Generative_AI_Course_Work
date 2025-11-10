"""
Code Genius Supervisor Agent - Orchestrates the workflow and coordinates other agents.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import time

from agents.repo_mapper import RepoMapper, RepoMap
from agents.code_analyzer import CodeAnalyzer, CodeContextGraph
from agents.doc_genie import DocGenie, GeneratedDocumentation


@dataclass
class AnalysisResult:
    """Result of codebase analysis."""
    repo_map: RepoMap
    ccg: CodeContextGraph
    documentation: GeneratedDocumentation
    analysis_time: float
    success: bool
    error_message: Optional[str] = None


class CodeGenius:
    """Supervisor agent that orchestrates the codebase analysis workflow."""
    
    def __init__(self):
        self.repo_mapper = RepoMapper()
        self.code_analyzer = CodeAnalyzer()
        self.doc_genie = DocGenie()
        self.analysis_history: List[AnalysisResult] = []
    
    def analyze_repository(
        self,
        repo_url: str,
        branch: Optional[str] = None,
        language: Optional[str] = None
    ) -> AnalysisResult:
        """
        Analyze a repository and generate documentation.
        
        Args:
            repo_url: GitHub repository URL
            branch: Specific branch to analyze
            language: Force specific language (if None, auto-detect)
            
        Returns:
            AnalysisResult object
        """
        start_time = time.time()
        
        try:
            print(f"🚀 Starting analysis of {repo_url}")
            
            # Step 1: Map repository
            print("📁 Mapping repository structure...")
            repo_map = self.repo_mapper.map_repository(repo_url, branch)
            print(f"✅ Repository mapped successfully")
            print(f"   - Primary language: {repo_map.language_detection.get('primary_language', 'Unknown')}")
            print(f"   - Total files: {repo_map.language_detection.get('total_files', 0)}")
            print(f"   - Entry points: {len(repo_map.entry_points)}")
            
            # Step 2: Analyze code
            print("🔍 Analyzing code structure...")
            detected_language = language or repo_map.language_detection.get('primary_language', 'python')
            ccg = self.code_analyzer.analyze_codebase(
                repo_path=self.repo_mapper.get_repo_path(repo_url),
                language=detected_language,
                entry_points=repo_map.entry_points
            )
            print(f"✅ Code analysis completed")
            print(f"   - Elements found: {len(ccg.elements)}")
            print(f"   - Relationships: {len(ccg.relationships)}")
            
            # Step 3: Generate documentation
            print("📝 Generating documentation...")
            repo_name = self._extract_repo_name(repo_url)
            documentation = self.doc_genie.generate_documentation(
                repo_map=repo_map,
                ccg=ccg,
                repo_name=repo_name
            )
            print(f"✅ Documentation generated")
            print(f"   - Sections: {len(documentation.sections)}")
            print(f"   - Diagrams: {len(documentation.diagrams)}")
            
            # Step 4: Save results
            print("💾 Saving documentation...")
            output_path = self.doc_genie.save_documentation(documentation, repo_name)
            print(f"✅ Documentation saved to: {output_path}")
            
            analysis_time = time.time() - start_time
            
            result = AnalysisResult(
                repo_map=repo_map,
                ccg=ccg,
                documentation=documentation,
                analysis_time=analysis_time,
                success=True
            )
            
            self.analysis_history.append(result)
            print(f"🎉 Analysis completed in {analysis_time:.2f} seconds")
            
            return result
            
        except Exception as e:
            analysis_time = time.time() - start_time
            error_msg = f"Analysis failed: {str(e)}"
            print(f"❌ {error_msg}")
            
            result = AnalysisResult(
                repo_map=None,
                ccg=None,
                documentation=None,
                analysis_time=analysis_time,
                success=False,
                error_message=error_msg
            )
            
            self.analysis_history.append(result)
            return result
        
        finally:
            # Cleanup
            try:
                self.repo_mapper.cleanup(repo_url)
            except:
                pass
    
    def get_analysis_summary(self) -> Dict[str, Any]:
        """Get summary of all analyses performed."""
        total_analyses = len(self.analysis_history)
        successful_analyses = sum(1 for r in self.analysis_history if r.success)
        failed_analyses = total_analyses - successful_analyses
        
        total_time = sum(r.analysis_time for r in self.analysis_history)
        avg_time = total_time / total_analyses if total_analyses > 0 else 0
        
        return {
            'total_analyses': total_analyses,
            'successful_analyses': successful_analyses,
            'failed_analyses': failed_analyses,
            'success_rate': successful_analyses / total_analyses if total_analyses > 0 else 0,
            'total_time': total_time,
            'average_time': avg_time,
            'recent_analyses': [
                {
                    'timestamp': time.time() - r.analysis_time,
                    'success': r.success,
                    'time_taken': r.analysis_time,
                    'error': r.error_message
                }
                for r in self.analysis_history[-5:]  # Last 5 analyses
            ]
        }
    
    def query_codebase(self, repo_url: str, query: str) -> List[Dict[str, Any]]:
        """
        Query a previously analyzed codebase.
        
        Args:
            repo_url: Repository URL
            query: Query string
            
        Returns:
            List of matching results
        """
        # Find the most recent successful analysis for this repo
        repo_analyses = [
            r for r in self.analysis_history
            if r.success and r.repo_map and r.repo_map.repo_info.get('url') == repo_url
        ]
        
        if not repo_analyses:
            return []
        
        latest_analysis = repo_analyses[-1]
        ccg = latest_analysis.ccg
        
        # Query the Code Context Graph
        return self.code_analyzer.query_relationships(ccg, query)
    
    def get_repository_info(self, repo_url: str) -> Optional[Dict[str, Any]]:
        """Get information about a previously analyzed repository."""
        repo_analyses = [
            r for r in self.analysis_history
            if r.success and r.repo_map and r.repo_map.repo_info.get('url') == repo_url
        ]
        
        if not repo_analyses:
            return None
        
        latest_analysis = repo_analyses[-1]
        repo_map = latest_analysis.repo_map
        
        return {
            'url': repo_url,
            'repo_info': repo_map.repo_info,
            'language_detection': repo_map.language_detection,
            'entry_points': repo_map.entry_points,
            'readme_summary': repo_map.readme_summary,
            'analysis_time': latest_analysis.analysis_time,
            'elements_count': len(latest_analysis.ccg.elements),
            'relationships_count': len(latest_analysis.ccg.relationships)
        }
    
    def list_analyzed_repositories(self) -> List[Dict[str, Any]]:
        """List all previously analyzed repositories."""
        repos = {}
        
        for analysis in self.analysis_history:
            if analysis.success and analysis.repo_map:
                url = analysis.repo_map.repo_info.get('url')
                if url and url not in repos:
                    repos[url] = {
                        'url': url,
                        'name': self._extract_repo_name(url),
                        'language': analysis.repo_map.language_detection.get('primary_language', 'Unknown'),
                        'files_count': analysis.repo_map.language_detection.get('total_files', 0),
                        'analysis_time': analysis.analysis_time,
                        'elements_count': len(analysis.ccg.elements) if analysis.ccg else 0
                    }
        
        return list(repos.values())
    
    def _extract_repo_name(self, repo_url: str) -> str:
        """Extract repository name from URL."""
        if repo_url.endswith('.git'):
            repo_url = repo_url[:-4]
        
        if repo_url.startswith('git@github.com:'):
            repo_url = repo_url.replace('git@github.com:', 'https://github.com/')
        
        parts = repo_url.rstrip('/').split('/')
        if len(parts) >= 2:
            return f"{parts[-2]}_{parts[-1]}"
        
        return "unknown_repo"
    
    def cleanup_all(self) -> None:
        """Clean up all cloned repositories."""
        self.repo_mapper.git_manager.cleanup_all()
    
    def export_analysis_history(self, file_path: str) -> None:
        """Export analysis history to JSON file."""
        history_data = []
        
        for analysis in self.analysis_history:
            analysis_data = {
                'success': analysis.success,
                'analysis_time': analysis.analysis_time,
                'error_message': analysis.error_message,
                'timestamp': time.time() - analysis.analysis_time
            }
            
            if analysis.success and analysis.repo_map:
                analysis_data.update({
                    'repo_url': analysis.repo_map.repo_info.get('url'),
                    'repo_name': self._extract_repo_name(analysis.repo_map.repo_info.get('url', '')),
                    'language': analysis.repo_map.language_detection.get('primary_language'),
                    'files_count': analysis.repo_map.language_detection.get('total_files', 0),
                    'elements_count': len(analysis.ccg.elements) if analysis.ccg else 0,
                    'relationships_count': len(analysis.ccg.relationships) if analysis.ccg else 0
                })
            
            history_data.append(analysis_data)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2)
    
    def import_analysis_history(self, file_path: str) -> None:
        """Import analysis history from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
            
            # Note: This is a simplified import that only restores metadata
            # Full restoration would require re-analyzing repositories
            for data in history_data:
                if data.get('success'):
                    print(f"Found analysis record for {data.get('repo_name', 'Unknown')}")
            
            print(f"Imported {len(history_data)} analysis records")
            
        except Exception as e:
            print(f"Error importing analysis history: {e}")


def analyze_repository(repo_url: str, branch: Optional[str] = None, language: Optional[str] = None) -> AnalysisResult:
    """
    Convenience function to analyze a repository.
    
    Args:
        repo_url: GitHub repository URL
        branch: Specific branch to analyze
        language: Force specific language
        
    Returns:
        AnalysisResult object
    """
    genius = CodeGenius()
    return genius.analyze_repository(repo_url, branch, language)