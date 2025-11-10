"""
DocGenie Agent - Synthesizes final markdown documentation with diagrams.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import io
import base64


@dataclass
class DocumentationSection:
    """Represents a section of the documentation."""
    title: str
    content: str
    level: int = 1
    subsections: Optional[List['DocumentationSection']] = None


@dataclass
class GeneratedDocumentation:
    """Generated documentation structure."""
    title: str
    sections: List[DocumentationSection]
    diagrams: List[Dict[str, str]]  # List of {name: base64_image}
    metadata: Dict[str, Any]


class DocGenie:
    """Generates comprehensive markdown documentation."""
    
    def __init__(self):
        self.output_dir = Path("outputs")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_documentation(
        self,
        repo_map: Any,
        ccg: Any,
        repo_name: str
    ) -> GeneratedDocumentation:
        """
        Generate comprehensive documentation for a repository.
        
        Args:
            repo_map: Repository mapping from RepoMapper
            ccg: Code Context Graph from CodeAnalyzer
            repo_name: Name of the repository
            
        Returns:
            GeneratedDocumentation object
        """
        sections = []
        
        # 1. Project Overview
        overview_section = self._generate_overview_section(repo_map)
        sections.append(overview_section)
        
        # 2. Installation and Setup
        setup_section = self._generate_setup_section(repo_map)
        sections.append(setup_section)
        
        # 3. Architecture Overview
        architecture_section = self._generate_architecture_section(ccg)
        sections.append(architecture_section)
        
        # 4. API Reference
        api_section = self._generate_api_section(ccg)
        sections.append(api_section)
        
        # 5. Usage Examples
        usage_section = self._generate_usage_section(repo_map, ccg)
        sections.append(usage_section)
        
        # 6. Development Guide
        dev_section = self._generate_development_section(repo_map, ccg)
        sections.append(dev_section)
        
        # Generate diagrams
        diagrams = self._generate_diagrams(ccg, repo_name)
        
        # Create metadata
        metadata = {
            'repo_name': repo_name,
            'total_files': repo_map.language_detection.get('total_files', 0),
            'languages': repo_map.language_detection.get('detected_languages', []),
            'primary_language': repo_map.language_detection.get('primary_language', 'unknown'),
            'generated_at': self._get_current_timestamp()
        }
        
        return GeneratedDocumentation(
            title=f"{repo_name} - Code Documentation",
            sections=sections,
            diagrams=diagrams,
            metadata=metadata
        )
    
    def _generate_overview_section(self, repo_map: Any) -> DocumentationSection:
        """Generate project overview section."""
        content = []
        
        # Repository information
        repo_info = repo_map.repo_info
        content.append(f"**Repository:** {repo_info.get('url', 'Unknown')}")
        content.append(f"**Branch:** {repo_info.get('branch', 'Unknown')}")
        content.append(f"**Commit:** {repo_info.get('commit', {}).get('hash', 'Unknown')}")
        content.append("")
        
        # Language information
        lang_info = repo_map.language_detection
        if lang_info:
            content.append(f"**Primary Language:** {lang_info.get('primary_language', 'Unknown').title()}")
            content.append(f"**Detected Languages:** {', '.join(lang_info.get('detected_languages', []))}")
            content.append(f"**Total Files:** {lang_info.get('total_files', 0)}")
            content.append("")
        
        # README summary
        if repo_map.readme_summary:
            content.append("## Project Description")
            content.append(repo_map.readme_summary)
            content.append("")
        
        # Entry points
        if repo_map.entry_points:
            content.append("## Entry Points")
            content.append("The following files serve as entry points to the application:")
            content.append("")
            for entry_point in repo_map.entry_points:
                content.append(f"- `{entry_point}`")
            content.append("")
        
        return DocumentationSection(
            title="Project Overview",
            content="\n".join(content),
            level=1
        )
    
    def _generate_setup_section(self, repo_map: Any) -> DocumentationSection:
        """Generate installation and setup section."""
        content = []
        
        content.append("## Prerequisites")
        content.append("")
        
        # Language-specific prerequisites
        primary_lang = repo_map.language_detection.get('primary_language', 'unknown')
        if primary_lang == 'python':
            content.append("- Python 3.7 or higher")
            content.append("- pip (Python package manager)")
        elif primary_lang == 'jac':
            content.append("- Jac language runtime")
            content.append("- Python 3.7 or higher")
        elif primary_lang == 'javascript':
            content.append("- Node.js 14 or higher")
            content.append("- npm or yarn")
        elif primary_lang == 'java':
            content.append("- Java 8 or higher")
            content.append("- Maven or Gradle")
        elif primary_lang == 'rust':
            content.append("- Rust 1.50 or higher")
            content.append("- Cargo")
        elif primary_lang == 'go':
            content.append("- Go 1.16 or higher")
        
        content.append("")
        content.append("## Installation")
        content.append("")
        content.append("1. Clone the repository:")
        content.append("```bash")
        content.append(f"git clone {repo_map.repo_info.get('url', 'REPO_URL')}")
        content.append("```")
        content.append("")
        
        # Language-specific installation steps
        if primary_lang == 'python':
            content.append("2. Create a virtual environment:")
            content.append("```bash")
            content.append("python -m venv venv")
            content.append("source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
            content.append("```")
            content.append("")
            content.append("3. Install dependencies:")
            content.append("```bash")
            content.append("pip install -r requirements.txt")
            content.append("```")
        elif primary_lang == 'javascript':
            content.append("2. Install dependencies:")
            content.append("```bash")
            content.append("npm install")
            content.append("```")
        elif primary_lang == 'java':
            content.append("2. Build the project:")
            content.append("```bash")
            content.append("mvn clean install")
            content.append("```")
        elif primary_lang == 'rust':
            content.append("2. Build the project:")
            content.append("```bash")
            content.append("cargo build")
            content.append("```")
        elif primary_lang == 'go':
            content.append("2. Build the project:")
            content.append("```bash")
            content.append("go build")
            content.append("```")
        
        return DocumentationSection(
            title="Installation and Setup",
            content="\n".join(content),
            level=1
        )
    
    def _generate_architecture_section(self, ccg: Any) -> DocumentationSection:
        """Generate architecture overview section."""
        content = []
        
        content.append("## System Architecture")
        content.append("")
        content.append("The following diagram shows the high-level architecture and relationships between components:")
        content.append("")
        
        # Add architecture diagram placeholder
        content.append("![Architecture Diagram](architecture_diagram.png)")
        content.append("")
        
        # Component overview
        content.append("### Key Components")
        content.append("")
        
        # Group elements by type
        components = {}
        for element_id, element in ccg.elements.items():
            comp_type = element.type
            if comp_type not in components:
                components[comp_type] = []
            components[comp_type].append(element)
        
        for comp_type, elements in components.items():
            content.append(f"#### {comp_type.title()}s")
            content.append("")
            for element in elements[:10]:  # Limit to first 10
                content.append(f"- **{element.name}** (`{element.file_path}`)")
                if element.docstring:
                    content.append(f"  - {element.docstring[:100]}...")
            content.append("")
        
        return DocumentationSection(
            title="Architecture Overview",
            content="\n".join(content),
            level=1
        )
    
    def _generate_api_section(self, ccg: Any) -> DocumentationSection:
        """Generate API reference section."""
        content = []
        
        content.append("## API Reference")
        content.append("")
        
        # Group by file
        files = {}
        for element_id, element in ccg.elements.items():
            if element.type in ['function', 'class']:
                file_path = element.file_path
                if file_path not in files:
                    files[file_path] = []
                files[file_path].append(element)
        
        for file_path, elements in files.items():
            content.append(f"### {file_path}")
            content.append("")
            
            for element in elements:
                content.append(f"#### {element.name}")
                content.append("")
                
                if element.type == 'function':
                    content.append("**Type:** Function")
                    if element.parameters:
                        content.append(f"**Parameters:** {', '.join(element.parameters)}")
                    if element.return_type:
                        content.append(f"**Returns:** {element.return_type}")
                elif element.type == 'class':
                    content.append("**Type:** Class")
                
                content.append(f"**Location:** Lines {element.line_start}-{element.line_end}")
                content.append("")
                
                if element.docstring:
                    content.append("**Description:**")
                    content.append(element.docstring)
                    content.append("")
        
        return DocumentationSection(
            title="API Reference",
            content="\n".join(content),
            level=1
        )
    
    def _generate_usage_section(self, repo_map: Any, ccg: Any) -> DocumentationSection:
        """Generate usage examples section."""
        content = []
        
        content.append("## Usage Examples")
        content.append("")
        
        # Find main functions or entry points
        main_functions = []
        for element_id, element in ccg.elements.items():
            if element.type == 'function' and 'main' in element.name.lower():
                main_functions.append(element)
        
        if main_functions:
            content.append("### Running the Application")
            content.append("")
            for func in main_functions:
                content.append(f"To run the main function in `{func.file_path}`:")
                content.append("")
                content.append("```bash")
                if repo_map.language_detection.get('primary_language') == 'python':
                    content.append(f"python {func.file_path}")
                elif repo_map.language_detection.get('primary_language') == 'jac':
                    content.append(f"jac run {func.file_path}")
                elif repo_map.language_detection.get('primary_language') == 'javascript':
                    content.append(f"node {func.file_path}")
                content.append("```")
                content.append("")
        
        # Add example code snippets
        content.append("### Code Examples")
        content.append("")
        content.append("Here are some key code examples from the codebase:")
        content.append("")
        
        # Find interesting functions to showcase
        interesting_functions = []
        for element_id, element in ccg.elements.items():
            if element.type == 'function' and len(element.name) > 3:
                interesting_functions.append(element)
        
        for func in interesting_functions[:3]:  # Show first 3
            content.append(f"#### {func.name}")
            content.append("")
            content.append(f"```{repo_map.language_detection.get('primary_language', 'text')}")
            content.append(f"# Function definition in {func.file_path}")
            content.append(f"# Lines {func.line_start}-{func.line_end}")
            content.append("...")
            content.append("```")
            content.append("")
        
        return DocumentationSection(
            title="Usage Examples",
            content="\n".join(content),
            level=1
        )
    
    def _generate_development_section(self, repo_map: Any, ccg: Any) -> DocumentationSection:
        """Generate development guide section."""
        content = []
        
        content.append("## Development Guide")
        content.append("")
        
        content.append("### Project Structure")
        content.append("")
        content.append("The project follows the following structure:")
        content.append("")
        
        # Generate file tree representation
        tree_content = self._generate_file_tree_text(repo_map.file_tree, 0)
        content.append("```")
        content.append(tree_content)
        content.append("```")
        content.append("")
        
        content.append("### Key Files")
        content.append("")
        for entry_point in repo_map.entry_points:
            content.append(f"- **{entry_point}** - Entry point to the application")
        content.append("")
        
        content.append("### Contributing")
        content.append("")
        content.append("1. Fork the repository")
        content.append("2. Create a feature branch")
        content.append("3. Make your changes")
        content.append("4. Add tests if applicable")
        content.append("5. Submit a pull request")
        content.append("")
        
        return DocumentationSection(
            title="Development Guide",
            content="\n".join(content),
            level=1
        )
    
    def _generate_file_tree_text(self, node: Any, depth: int) -> str:
        """Generate text representation of file tree."""
        lines = []
        indent = "  " * depth
        
        if node.type == 'directory':
            lines.append(f"{indent}📁 {node.name}/")
            if node.children:
                for child in node.children[:10]:  # Limit depth
                    lines.append(self._generate_file_tree_text(child, depth + 1))
        else:
            icon = "🐍" if node.language == 'python' else "📄"
            lines.append(f"{indent}{icon} {node.name}")
        
        return "\n".join(lines)
    
    def _generate_diagrams(self, ccg: Any, repo_name: str) -> List[Dict[str, str]]:
        """Generate visual diagrams."""
        diagrams = []
        
        # 1. Class/Function relationship diagram
        try:
            class_diagram = self._create_class_diagram(ccg)
            diagrams.append({
                'name': 'class_relationships',
                'data': class_diagram
            })
        except Exception as e:
            print(f"Error creating class diagram: {e}")
        
        # 2. Call graph diagram
        try:
            call_graph = self._create_call_graph(ccg)
            diagrams.append({
                'name': 'call_graph',
                'data': call_graph
            })
        except Exception as e:
            print(f"Error creating call graph: {e}")
        
        return diagrams
    
    def _create_class_diagram(self, ccg: Any) -> str:
        """Create a class relationship diagram."""
        plt.figure(figsize=(12, 8))
        
        # Create a new graph for visualization
        G = nx.DiGraph()
        
        # Add nodes for classes and functions
        for element_id, element in ccg.elements.items():
            if element.type in ['class', 'function']:
                G.add_node(element_id, label=element.name, type=element.type)
        
        # Add edges for relationships
        for from_id, to_id, rel_type in ccg.relationships:
            if from_id in G.nodes and to_id in G.nodes:
                G.add_edge(from_id, to_id, relationship=rel_type)
        
        # Layout
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Draw nodes
        classes = [n for n in G.nodes() if G.nodes[n].get('type') == 'class']
        functions = [n for n in G.nodes() if G.nodes[n].get('type') == 'function']
        
        nx.draw_networkx_nodes(G, pos, nodelist=classes, node_color='lightblue', 
                              node_size=1000, alpha=0.8)
        nx.draw_networkx_nodes(G, pos, nodelist=functions, node_color='lightgreen', 
                              node_size=800, alpha=0.8)
        
        # Draw edges
        nx.draw_networkx_edges(G, pos, alpha=0.5, arrows=True, arrowsize=20)
        
        # Draw labels
        labels = {n: G.nodes[n]['label'] for n in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title("Class and Function Relationships")
        plt.axis('off')
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def _create_call_graph(self, ccg: Any) -> str:
        """Create a function call graph."""
        plt.figure(figsize=(10, 8))
        
        # Create a new graph for visualization
        G = nx.DiGraph()
        
        # Add nodes for functions only
        for element_id, element in ccg.elements.items():
            if element.type == 'function':
                G.add_node(element_id, label=element.name)
        
        # Add edges for call relationships
        for from_id, to_id, rel_type in ccg.relationships:
            if rel_type == 'calls' and from_id in G.nodes and to_id in G.nodes:
                G.add_edge(from_id, to_id)
        
        if len(G.nodes()) == 0:
            plt.text(0.5, 0.5, 'No function call relationships found', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.axis('off')
        else:
            # Layout
            pos = nx.spring_layout(G, k=2, iterations=50)
            
            # Draw nodes
            nx.draw_networkx_nodes(G, pos, node_color='lightcoral', 
                                  node_size=1000, alpha=0.8)
            
            # Draw edges
            nx.draw_networkx_edges(G, pos, alpha=0.6, arrows=True, arrowsize=20)
            
            # Draw labels
            labels = {n: G.nodes[n]['label'] for n in G.nodes()}
            nx.draw_networkx_labels(G, pos, labels, font_size=8)
        
        plt.title("Function Call Graph")
        plt.axis('off')
        
        # Convert to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp as string."""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def save_documentation(self, doc: GeneratedDocumentation, repo_name: str) -> str:
        """Save documentation to file."""
        # Create output directory
        output_dir = self.output_dir / repo_name
        output_dir.mkdir(exist_ok=True)
        
        # Generate markdown content
        markdown_content = self._generate_markdown(doc)
        
        # Save markdown file
        md_file = output_dir / "docs.md"
        with open(md_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Save diagrams
        for i, diagram in enumerate(doc.diagrams):
            diagram_file = output_dir / f"{diagram['name']}.png"
            with open(diagram_file, 'wb') as f:
                f.write(base64.b64decode(diagram['data']))
        
        # Save metadata
        metadata_file = output_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(doc.metadata, f, indent=2)
        
        return str(md_file)
    
    def _generate_markdown(self, doc: GeneratedDocumentation) -> str:
        """Generate markdown content from documentation."""
        content = []
        
        # Title
        content.append(f"# {doc.title}")
        content.append("")
        
        # Table of contents
        content.append("## Table of Contents")
        content.append("")
        for section in doc.sections:
            content.append(f"- [{section.title}](#{section.title.lower().replace(' ', '-')})")
        content.append("")
        
        # Sections
        for section in doc.sections:
            content.append(f"## {section.title}")
            content.append("")
            content.append(section.content)
            content.append("")
        
        # Diagrams
        if doc.diagrams:
            content.append("## Diagrams")
            content.append("")
            for diagram in doc.diagrams:
                content.append(f"### {diagram['name'].replace('_', ' ').title()}")
                content.append("")
                content.append(f"![{diagram['name']}]({diagram['name']}.png)")
                content.append("")
        
        return "\n".join(content)


def generate_documentation(repo_map: Any, ccg: Any, repo_name: str) -> GeneratedDocumentation:
    """
    Convenience function to generate documentation.
    
    Args:
        repo_map: Repository mapping
        ccg: Code Context Graph
        repo_name: Repository name
        
    Returns:
        GeneratedDocumentation object
    """
    doc_genie = DocGenie()
    return doc_genie.generate_documentation(repo_map, ccg, repo_name)