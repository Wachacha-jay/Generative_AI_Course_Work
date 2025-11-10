# Codebase Genius

An autonomous multi-agent system that generates high-quality markdown documentation for GitHub repositories with clear prose and explanatory diagrams.

## Features

- **Multi-language Support**: Detects and analyzes Python, Jac, JavaScript, Java, C++, Rust, and Go codebases
- **Intelligent Analysis**: Uses Tree-sitter for accurate code parsing and builds Code Context Graphs (CCG)
- **Interactive UI**: Streamlit-based web interface for easy repository analysis
- **REST API**: HTTP interface for programmatic access
- **Visual Documentation**: Generates diagrams showing code relationships

## Architecture

The system consists of four main agents:

1. **Code Genius (Supervisor)** - Orchestrates the workflow and coordinates other agents
2. **Repo Mapper** - Clones repositories and generates file-tree representations
3. **Code Analyzer** - Performs deep code analysis and builds relationship graphs
4. **DocGenie** - Synthesizes final markdown documentation with diagrams

## Quick Start

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit UI:
```bash
streamlit run frontend/app.py
```

3. Or run the API server:
```bash
python -m uvicorn main:app --reload --port 8000
```

## Usage

1. Open the Streamlit UI in your browser
2. Enter a GitHub repository URL
3. Select the target language (auto-detection available)
4. Click "Analyze Repository"
5. Download the generated documentation

## API Usage

```bash
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"repo_url": "https://github.com/user/repo", "language": "python"}'
```

## Output

Generated documentation includes:
- Project overview and installation instructions
- API reference with function/class relationships
- Visual diagrams showing code structure
- Usage examples and best practices