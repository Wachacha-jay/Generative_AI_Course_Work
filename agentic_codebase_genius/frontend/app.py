"""
Streamlit UI for Codebase Genius - Multi-language codebase analysis tool.
"""

import streamlit as st
import os
import sys
from pathlib import Path
import time
import json
import requests
from typing import Dict, Any, Optional

# API endpoints
API_ENDPOINTS = {
    'repo_mapper': 'http://localhost:8000',
    'code_analyzer': 'http://localhost:8001',
    'doc_generator': 'http://localhost:8002',
    'doc_saver': 'http://localhost:8003'
}


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Codebase Genius",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
    }
    .info-message {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #bee5eb;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'current_repo' not in st.session_state:
        st.session_state.current_repo = None
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'documentation' not in st.session_state:
        st.session_state.documentation = None
    
    # Header
    st.markdown('<h1 class="main-header">🧠 Codebase Genius</h1>', unsafe_allow_html=True)
    st.markdown("### Multi-language codebase analysis and documentation generator")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Repository URL input
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/user/repo",
            help="Enter the full GitHub repository URL"
        )
        
        # Branch selection
        branch = st.text_input(
            "Branch (optional)",
            placeholder="main",
            help="Leave empty to use default branch"
        )
        
        # Language selection
        language_options = [
            "Auto-detect",
            "Python",
            "Jac",
            "JavaScript",
            "Java",
            "C++",
            "Rust",
            "Go"
        ]
        
        selected_language = st.selectbox(
            "Programming Language",
            language_options,
            help="Select the primary programming language or use auto-detection"
        )
        
        language = None if selected_language == "Auto-detect" else selected_language.lower()
        
        # Analysis options
        st.subheader("Analysis Options")
        include_diagrams = st.checkbox("Generate diagrams", value=True)
        include_api_ref = st.checkbox("Generate API reference", value=True)
        include_examples = st.checkbox("Include usage examples", value=True)
        
        # Analyze button
        analyze_button = st.button(
            "🚀 Analyze Repository",
            type="primary",
            use_container_width=True
        )
    
    # Main content area
    if analyze_button and repo_url:
        with st.spinner("Analyzing repository..."):
            try:
                # Step 1: Map Repository
                start_time = time.time()
                
                map_response = requests.post(
                    f"{API_ENDPOINTS['repo_mapper']}/repo_mapper",
                    json={"url": repo_url}
                ).json()
                
                if not map_response.get("success"):
                    st.error(f"❌ Repository mapping failed: {map_response.get('error')}")
                    return
                
                st.session_state.current_repo = map_response
                
                # Step 2: Analyze Code
                analysis_response = requests.post(
                    f"{API_ENDPOINTS['code_analyzer']}/code_analyzer",
                    json={"repo_path": map_response.get("local_path")}
                ).json()
                
                if not analysis_response.get("success"):
                    st.error(f"❌ Code analysis failed: {analysis_response.get('error')}")
                    return
                
                st.session_state.analysis_result = analysis_response
                
                # Step 3: Generate Documentation
                doc_response = requests.post(
                    f"{API_ENDPOINTS['doc_generator']}/doc_generator",
                    json={
                        "repo_map": map_response,
                        "ccg": analysis_response.get("ccg", {})
                    }
                ).json()
                
                if not doc_response.get("success"):
                    st.error(f"❌ Documentation generation failed: {doc_response.get('error')}")
                    return
                
                st.session_state.documentation = doc_response.get("documentation")
                
                # Record successful analysis
                analysis_time = time.time() - start_time
                st.session_state.analysis_history.append({
                    'repo_url': repo_url,
                    'timestamp': time.time(),
                    'success': True,
                    'analysis_time': analysis_time
                })
                
                st.success("✅ Analysis completed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {str(e)}")
    
    # Display results
    if st.session_state.analysis_result and st.session_state.analysis_result.success:
        display_analysis_results(st.session_state.analysis_result)
    
    # Analysis history
    if st.session_state.analysis_history:
        display_analysis_history()
    
    # Repository information
    if repo_url and not analyze_button:
        display_repo_preview(repo_url)


def display_analysis_results(result):
    """Display analysis results."""
    st.header("📊 Analysis Results")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Analysis Time",
            f"{result.analysis_time:.2f}s",
            help="Time taken to complete the analysis"
        )
    
    with col2:
        st.metric(
            "Files Analyzed",
            result.repo_map.language_detection.get('total_files', 0),
            help="Total number of files in the repository"
        )
    
    with col3:
        st.metric(
            "Code Elements",
            len(result.ccg.elements),
            help="Functions, classes, and other code elements found"
        )
    
    with col4:
        st.metric(
            "Relationships",
            len(result.ccg.relationships),
            help="Relationships between code elements"
        )
    
    # Repository information
    st.subheader("📁 Repository Information")
    
    repo_info = result.repo_map.repo_info
    lang_info = result.repo_map.language_detection
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Repository:** {repo_info.get('url', 'Unknown')}")
        st.markdown(f"**Branch:** {repo_info.get('branch', 'Unknown')}")
        st.markdown(f"**Commit:** {repo_info.get('commit', {}).get('hash', 'Unknown')}")
    
    with col2:
        st.markdown(f"**Primary Language:** {lang_info.get('primary_language', 'Unknown').title()}")
        st.markdown(f"**Detected Languages:** {', '.join(lang_info.get('detected_languages', []))}")
        st.markdown(f"**Entry Points:** {len(result.repo_map.entry_points)}")
    
    # Language detection details
    if lang_info:
        st.subheader("🔍 Language Detection")
        
        detected_langs = lang_info.get('detected_languages', [])
        file_counts = lang_info.get('file_counts', {})
        
        if detected_langs:
            lang_data = []
            for lang in detected_langs:
                count = file_counts.get(lang, 0)
                percentage = (count / lang_info.get('total_files', 1)) * 100
                lang_data.append({
                    'Language': lang.title(),
                    'Files': count,
                    'Percentage': f"{percentage:.1f}%"
                })
            
            st.dataframe(lang_data, use_container_width=True)
    
    # Entry points
    if result.repo_map.entry_points:
        st.subheader("🚪 Entry Points")
        for entry_point in result.repo_map.entry_points:
            st.code(entry_point)
    
    # Code structure overview
    st.subheader("🏗️ Code Structure")
    
    # Group elements by type
    element_types = {}
    for element_id, element in result.ccg.elements.items():
        element_type = element.type
        if element_type not in element_types:
            element_types[element_type] = []
        element_types[element_type].append(element)
    
    for element_type, elements in element_types.items():
        with st.expander(f"{element_type.title()}s ({len(elements)})"):
            for element in elements[:10]:  # Show first 10
                st.markdown(f"**{element.name}** (`{element.file_path}`)")
                if element.docstring:
                    st.markdown(f"*{element.docstring[:100]}...*")
                st.markdown("---")
    
    # Relationships
    if result.ccg.relationships:
        st.subheader("🔗 Code Relationships")
        
        rel_data = []
        for from_id, to_id, rel_type in result.ccg.relationships[:20]:  # Show first 20
            from_element = result.ccg.elements.get(from_id)
            to_element = result.ccg.elements.get(to_id)
            
            if from_element and to_element:
                rel_data.append({
                    'From': f"{from_element.name} ({from_element.type})",
                    'To': f"{to_element.name} ({to_element.type})",
                    'Relationship': rel_type
                })
        
        if rel_data:
            st.dataframe(rel_data, use_container_width=True)
    
    # Documentation preview
    st.subheader("📝 Generated Documentation")
    
    doc = result.documentation
    
    st.markdown(f"**Title:** {doc.title}")
    st.markdown(f"**Sections:** {len(doc.sections)}")
    st.markdown(f"**Diagrams:** {len(doc.diagrams)}")
    
    # Show section previews
    for section in doc.sections:
        with st.expander(f"📄 {section.title}"):
            st.markdown(section.content[:500] + "..." if len(section.content) > 500 else section.content)
    
    # Download documentation
    st.subheader("💾 Download Documentation")
    
    if st.button("📥 Download Markdown Documentation"):
        try:
            # Save documentation using the doc_saver API
            save_response = requests.post(
                f"{API_ENDPOINTS['doc_saver']}/doc_saver",
                json={
                    "documentation": st.session_state.documentation,
                    "repo_name": st.session_state.current_repo.get("name", "unknown")
                }
            ).json()
            
            if save_response.get("success"):
                doc_path = save_response.get("path")
                with open(doc_path, 'r', encoding='utf-8') as f:
                    doc_content = f.read()
                
                st.download_button(
                    label="Download docs.md",
                    data=doc_content,
                    file_name="docs.md",
                    mime="text/markdown"
                )
            else:
                st.error(f"❌ Failed to save documentation: {save_response.get('error')}")
        except Exception as e:
            st.error(f"❌ Error saving documentation: {str(e)}")
    
    # Show diagrams
    if doc.diagrams:
        st.subheader("📊 Generated Diagrams")
        
        for diagram in doc.diagrams:
            st.markdown(f"### {diagram['name'].replace('_', ' ').title()}")
            
            # Decode and display diagram
            import base64
            from io import BytesIO
            from PIL import Image
            
            try:
                diagram_data = base64.b64decode(diagram['data'])
                image = Image.open(BytesIO(diagram_data))
                st.image(image, use_column_width=True)
            except Exception as e:
                st.error(f"Could not display diagram: {e}")


def display_analysis_history():
    """Display analysis history."""
    st.header("📈 Analysis History")
    
    if st.session_state.analysis_history:
        history_data = []
        for i, analysis in enumerate(st.session_state.analysis_history):
            history_data.append({
                'Repository': analysis['repo_url'],
                'Timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(analysis['timestamp'])),
                'Success': '✅' if analysis['success'] else '❌',
                'Time (s)': f"{analysis['analysis_time']:.2f}"
            })
        
        st.dataframe(history_data, use_container_width=True)
    else:
        st.info("No analysis history available.")


def display_repo_preview(repo_url):
    """Display repository preview before analysis."""
    st.header("🔍 Repository Preview")
    
    try:
        # Basic URL validation
        if not repo_url.startswith(('https://github.com/', 'git@github.com:')):
            st.warning("⚠️ Please enter a valid GitHub repository URL")
            return
        
        st.info(f"Ready to analyze: {repo_url}")
        
        # Show what will be analyzed
        st.markdown("**What will be analyzed:**")
        st.markdown("- Repository structure and file tree")
        st.markdown("- Code elements (functions, classes, variables)")
        st.markdown("- Relationships between code elements")
        st.markdown("- Language detection and classification")
        st.markdown("- Entry points and main functions")
        st.markdown("- README and documentation files")
        
    except Exception as e:
        st.error(f"Error previewing repository: {e}")


def check_api_health():
    """Check if all API endpoints are accessible."""
    all_healthy = True
    unhealthy_endpoints = []
    
    for name, url in API_ENDPOINTS.items():
        try:
            response = requests.get(f"{url}/status")
            if response.status_code != 200:
                all_healthy = False
                unhealthy_endpoints.append(name)
        except:
            all_healthy = False
            unhealthy_endpoints.append(name)
    
    if not all_healthy:
        st.error(f"❌ Some API endpoints are not accessible: {', '.join(unhealthy_endpoints)}")
        st.error("Please make sure the Jac server is running: jac run genius.jac")
        return False
    
    return True


def display_language_detection_info():
    """Display information about supported languages."""
    st.header("🌐 Supported Languages")
    
    languages = [
        {'name': 'Python', 'extensions': ['.py'], 'description': 'General-purpose programming language'},
        {'name': 'Jac', 'extensions': ['.jac'], 'description': 'Jaseci agent language'},
        {'name': 'JavaScript', 'extensions': ['.js'], 'description': 'Web programming language'},
        {'name': 'Java', 'extensions': ['.java'], 'description': 'Object-oriented programming language'},
        {'name': 'C++', 'extensions': ['.cpp', '.hpp'], 'description': 'Systems programming language'},
        {'name': 'Rust', 'extensions': ['.rs'], 'description': 'Systems programming language'},
        {'name': 'Go', 'extensions': ['.go'], 'description': 'Concurrent programming language'}
    ]
    
    for lang in languages:
        with st.expander(f"🔤 {lang['name']}"):
            st.markdown(f"**Description:** {lang['description']}")
            st.markdown(f"**Extensions:** {', '.join(lang['extensions'])}")


if __name__ == "__main__":
    main()