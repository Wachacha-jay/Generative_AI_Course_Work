"""
FastAPI backend for Codebase Genius - Multi-language codebase analysis API.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, HttpUrl
import json

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from agents.code_genius import CodeGenius, AnalysisResult
from utils.language_detector import LanguageDetector


# Pydantic models
class AnalysisRequest(BaseModel):
    repo_url: HttpUrl
    branch: Optional[str] = None
    language: Optional[str] = None
    include_diagrams: bool = True
    include_api_ref: bool = True
    include_examples: bool = True


class AnalysisResponse(BaseModel):
    success: bool
    analysis_id: str
    repo_name: str
    analysis_time: float
    message: str
    error: Optional[str] = None


class AnalysisStatus(BaseModel):
    analysis_id: str
    status: str  # 'pending', 'running', 'completed', 'failed'
    progress: float  # 0.0 to 1.0
    message: str
    result: Optional[Dict[str, Any]] = None


class QueryRequest(BaseModel):
    repo_url: HttpUrl
    query: str


class QueryResponse(BaseModel):
    success: bool
    results: List[Dict[str, Any]]
    message: str


# Initialize FastAPI app
app = FastAPI(
    title="Codebase Genius API",
    description="Multi-language codebase analysis and documentation generation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
code_genius = CodeGenius()
language_detector = LanguageDetector()

# In-memory storage for analysis results (use database in production)
analysis_results: Dict[str, AnalysisResult] = {}
analysis_status: Dict[str, AnalysisStatus] = {}


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Codebase Genius API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_repository(request: AnalysisRequest):
    """
    Analyze a GitHub repository and generate documentation.
    
    Args:
        request: Analysis request with repository URL and options
        
    Returns:
        Analysis response with results
    """
    try:
        repo_url = str(request.repo_url)
        analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Update status
        analysis_status[analysis_id] = AnalysisStatus(
            analysis_id=analysis_id,
            status="running",
            progress=0.0,
            message="Starting analysis..."
        )
        
        # Perform analysis
        result = code_genius.analyze_repository(
            repo_url=repo_url,
            branch=request.branch,
            language=request.language
        )
        
        # Store result
        analysis_results[analysis_id] = result
        
        if result.success:
            analysis_status[analysis_id] = AnalysisStatus(
                analysis_id=analysis_id,
                status="completed",
                progress=1.0,
                message="Analysis completed successfully",
                result={
                    "repo_name": code_genius._extract_repo_name(repo_url),
                    "analysis_time": result.analysis_time,
                    "elements_count": len(result.ccg.elements),
                    "relationships_count": len(result.ccg.relationships),
                    "languages": result.repo_map.language_detection.get('detected_languages', []),
                    "primary_language": result.repo_map.language_detection.get('primary_language', 'unknown')
                }
            )
            
            return AnalysisResponse(
                success=True,
                analysis_id=analysis_id,
                repo_name=code_genius._extract_repo_name(repo_url),
                analysis_time=result.analysis_time,
                message="Analysis completed successfully"
            )
        else:
            analysis_status[analysis_id] = AnalysisStatus(
                analysis_id=analysis_id,
                status="failed",
                progress=0.0,
                message="Analysis failed",
                result={"error": result.error_message}
            )
            
            return AnalysisResponse(
                success=False,
                analysis_id=analysis_id,
                repo_name="",
                analysis_time=result.analysis_time,
                message="Analysis failed",
                error=result.error_message
            )
            
    except Exception as e:
        return AnalysisResponse(
            success=False,
            analysis_id="",
            repo_name="",
            analysis_time=0.0,
            message="Analysis failed",
            error=str(e)
        )


@app.get("/analyze/{analysis_id}/status", response_model=AnalysisStatus)
async def get_analysis_status(analysis_id: str):
    """Get the status of an analysis."""
    if analysis_id not in analysis_status:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analysis_status[analysis_id]


@app.get("/analyze/{analysis_id}/result")
async def get_analysis_result(analysis_id: str):
    """Get the full analysis result."""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    
    result = analysis_results[analysis_id]
    
    if not result.success:
        raise HTTPException(status_code=400, detail="Analysis failed")
    
    # Convert result to JSON-serializable format
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
    }


@app.get("/analyze/{analysis_id}/download")
async def download_documentation(analysis_id: str):
    """Download the generated documentation as a markdown file."""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis result not found")
    
    result = analysis_results[analysis_id]
    
    if not result.success:
        raise HTTPException(status_code=400, detail="Analysis failed")
    
    # Save documentation
    repo_name = code_genius._extract_repo_name(result.repo_map.repo_info.get('url', ''))
    output_path = code_genius.doc_genie.save_documentation(result.documentation, repo_name)
    
    if not os.path.exists(output_path):
        raise HTTPException(status_code=500, detail="Documentation file not found")
    
    return FileResponse(
        path=output_path,
        filename="docs.md",
        media_type="text/markdown"
    )


@app.post("/query", response_model=QueryResponse)
async def query_codebase(request: QueryRequest):
    """Query a previously analyzed codebase."""
    try:
        repo_url = str(request.repo_url)
        results = code_genius.query_codebase(repo_url, request.query)
        
        return QueryResponse(
            success=True,
            results=results,
            message=f"Found {len(results)} results"
        )
        
    except Exception as e:
        return QueryResponse(
            success=False,
            results=[],
            message=f"Query failed: {str(e)}"
        )


@app.get("/repositories")
async def list_repositories():
    """List all analyzed repositories."""
    repos = code_genius.list_analyzed_repositories()
    return {"repositories": repos}


@app.get("/repositories/{repo_url:path}")
async def get_repository_info(repo_url: str):
    """Get information about a specific repository."""
    info = code_genius.get_repository_info(repo_url)
    
    if not info:
        raise HTTPException(status_code=404, detail="Repository not found")
    
    return info


@app.get("/languages")
async def get_supported_languages():
    """Get information about supported programming languages."""
    languages = {}
    
    for lang in ['python', 'jac', 'javascript', 'java', 'cpp', 'rust', 'go']:
        info = language_detector.get_language_info(lang)
        languages[lang] = info
    
    return {"languages": languages}


@app.get("/stats")
async def get_analysis_stats():
    """Get analysis statistics."""
    stats = code_genius.get_analysis_summary()
    return stats


@app.delete("/analyze/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete an analysis result."""
    if analysis_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    del analysis_results[analysis_id]
    del analysis_status[analysis_id]
    
    return {"message": "Analysis deleted successfully"}


@app.post("/cleanup")
async def cleanup_repositories():
    """Clean up all cloned repositories."""
    code_genius.cleanup_all()
    return {"message": "Cleanup completed"}


@app.get("/export/history")
async def export_analysis_history():
    """Export analysis history as JSON."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"analysis_history_{timestamp}.json"
    
    # Create temporary file
    temp_path = f"/tmp/{filename}"
    code_genius.export_analysis_history(temp_path)
    
    return FileResponse(
        path=temp_path,
        filename=filename,
        media_type="application/json"
    )


# Background task for cleanup
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    code_genius.cleanup_all()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )