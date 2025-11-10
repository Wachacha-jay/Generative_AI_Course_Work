#import python modules

import from agents.code_genius { CodeGenius, AnalysisResult };
import from utils.language_detector { LanguageDetector };

node AnalysisRequest {
    has repo_url: str;
    has branch: str = None;
    has language: str = None;
    has include_diagrams: bool = True;
    has include_api_ref: bool = True;
    has include_examples: bool = True;
}

node AnalysisResponse {
    has success: bool;
    has analysis_id: str;
    has repo_name: str;
    has analysis_time: float;
    has message: str;
    has error: str = None;
}

node AnalysisStatus {
    has analysis_id: str;
    has status: str;
    has progress: float;
    has message: str;
    has result: dict = None;
}

node QueryRequest {
    has repo_url: str;
    has query: str;
}

node QueryResponse {
    has success: bool;
    has results: list;
    has message: str;
}

node CodeGeniusAPI {
    has code_genius: CodeGenius;
    has language_detector: LanguageDetector;
    has analysis_results: dict;
    has analysis_status: dict;
}

walker APIHandler {
    has api_node: CodeGeniusAPI;

    can init with CodeGeniusAPI entry {
        self.api_node = here;
        here.code_genius = CodeGenius();
        here.language_detector = LanguageDetector();
        here.analysis_results = {};
        here.analysis_status = {};
    }

    can start with CodeGeniusAPI entry {
        return {
            "message": "Codebase Genius API",
            "version": "1.0.0",
            "docs": "/docs",
            "status": "running"
        };
    }

    can health_check with CodeGeniusAPI entry {
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0"
        };
    }

    can analyze_repository with AnalysisRequest entry {
        try {
            repo_url = here.repo_url;
            analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}";
            
            here.analysis_status[analysis_id] = AnalysisStatus(
                analysis_id=analysis_id,
                status="running",
                progress=0.0,
                message="Starting analysis..."
            );
            
            result = here.code_genius.analyze_repository(
                repo_url=repo_url,
                branch=request.branch,
                language=request.language
            );
            
            here.analysis_results[analysis_id] = result;
            
            if result.success {
                here.analysis_status[analysis_id] = AnalysisStatus(
                    analysis_id=analysis_id,
                    status="completed",
                    progress=1.0,
                    message="Analysis completed successfully",
                    result={
                        "repo_name": here.code_genius._extract_repo_name(repo_url),
                        "analysis_time": result.analysis_time,
                        "elements_count": len(result.ccg.elements),
                        "relationships_count": len(result.ccg.relationships),
                        "languages": result.repo_map.language_detection.get('detected_languages', []),
                        "primary_language": result.repo_map.language_detection.get('primary_language', 'unknown')
                    }
                );
                
                return AnalysisResponse(
                    success=True,
                    analysis_id=analysis_id,
                    repo_name=here.code_genius._extract_repo_name(repo_url),
                    analysis_time=result.analysis_time,
                    message="Analysis completed successfully"
                );
            } else {
                here.analysis_status[analysis_id] = AnalysisStatus(
                    analysis_id=analysis_id,
                    status="failed",
                    progress=0.0,
                    message="Analysis failed",
                    result={"error": result.error_message}
                );
                
                return AnalysisResponse(
                    success=False,
                    analysis_id=analysis_id,
                    repo_name="",
                    analysis_time=result.analysis_time,
                    message="Analysis failed",
                    error=result.error_message
                );
            }
        } except Exception as e {
            return AnalysisResponse(
                success=False,
                analysis_id="",
                repo_name="",
                analysis_time=0.0,
                message="Analysis failed",
                error=str(e)
            );
        }
    }

    can get_analysis_status(analysis_id: str) with CodeGeniusAPI entry {
        if analysis_id not in here.analysis_status {
            raise HTTPException(status_code=404, detail="Analysis not found");
        }
        
        return here.analysis_status[analysis_id];
    }

    can get_analysis_result(analysis_id: str) with CodeGeniusAPI entry {
        if analysis_id not in here.analysis_results {
            raise HTTPException(status_code=404, detail="Analysis result not found");
        }
        
        result = here.analysis_results[analysis_id];
        
        if not result.success {
            raise HTTPException(status_code=400, detail="Analysis failed");
        }
        
        return {
            "analysis_id": analysis_id,
            "success": result.success,
            "analysis_time": result.analysis_time,
            "repo_info": result.repo_map.repo_info,
            "language_detection": result.repo_map.language_detection,
            "entry_points": result.repo_map.entry_points,
            "readme_summary": result.repo_map.readme_summary,
            "elements": {k: v.to_dict() for k, v in result.ccg.elements.items()},
            "relationships": result.ccg.relationships,
            "documentation": {
                "title": result.documentation.title,
                "sections": [
                    {
                        "title": section.title,
                        "content": section.content,
                        "level": section.level
                    }
                    for section in result.documentation.sections
                ],
                "diagrams": result.documentation.diagrams,
                "metadata": result.documentation.metadata
            }
        };
    }

    can download_documentation(analysis_id: str) with CodeGeniusAPI entry {
        if analysis_id not in here.analysis_results {
            raise HTTPException(status_code=404, detail="Analysis result not found");
        }
        
        result = here.analysis_results[analysis_id];
        
        if not result.success {
            raise HTTPException(status_code=400, detail="Analysis failed");
        }
        
        repo_name = here.code_genius._extract_repo_name(result.repo_map.repo_info.get('url', ''));
        output_path = here.code_genius.doc_genie.save_documentation(result.documentation, repo_name);
        
        if not os.path.exists(output_path) {
            raise HTTPException(status_code=500, detail="Documentation file not found");
        }
        
        return FileResponse(
            path=output_path,
            filename="docs.md",
            media_type="text/markdown"
        );
    }

    can query_codebase(request: QueryRequest) with CodeGeniusAPI entry {
        try {
            repo_url = request.repo_url;
            results = here.code_genius.query_codebase(repo_url, request.query);
            
            return QueryResponse(
                success=True,
                results=results,
                message=f"Found {len(results)} results"
            );
        } except Exception as e {
            return QueryResponse(
                success=False,
                results=[],
                message=f"Query failed: {str(e)}"
            );
        }
    }

    can list_repositories with CodeGeniusAPI entry {
        repos = here.code_genius.list_analyzed_repositories();
        return {"repositories": repos};
    }

    can get_repository_info(repo_url: str) with CodeGeniusAPI entry {
        info = here.code_genius.get_repository_info(repo_url);
        
        if not info {
            raise HTTPException(status_code=404, detail="Repository not found");
        }
        
        return info;
    }

    can get_supported_languages with CodeGeniusAPI entry {
        languages = {};
        
        for lang in ['python', 'jac', 'javascript', 'java', 'cpp', 'rust', 'go'] {
            info = here.language_detector.get_language_info(lang);
            languages[lang] = info;
        }
        
        return {"languages": languages};
    }

    can get_analysis_stats with CodeGeniusAPI entry {
        stats = here.code_genius.get_analysis_summary();
        return stats;
    }

    can delete_analysis(analysis_id: str) with CodeGeniusAPI entry {
        if analysis_id not in here.analysis_results {
            raise HTTPException(status_code=404, detail="Analysis not found");
        }
        
        del here.analysis_results[analysis_id];
        del here.analysis_status[analysis_id];
        
        return {"message": "Analysis deleted successfully"};
    }

    can cleanup_repositories with CodeGeniusAPI entry {
        here.code_genius.cleanup_all();
        return {"message": "Cleanup completed"};
    }

    can export_analysis_history with CodeGeniusAPI entry {
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S');
        filename = f"analysis_history_{timestamp}.json";
        
        temp_path = f"/tmp/{filename}";
        here.code_genius.export_analysis_history(temp_path);
        
        return FileResponse(
            path=temp_path,
            filename=filename,
            media_type="application/json"
        );
    }

    can shutdown_cleanup with CodeGeniusAPI entry {
        here.code_genius.cleanup_all();
    }
}