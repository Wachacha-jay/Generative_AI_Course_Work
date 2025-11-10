# Codebase Genius 

An intelligent multi-agent system that autonomously analyzes codebases and generates comprehensive documentation with explanatory diagrams using both Jac and Python components.

##  Features

- **Dual Architecture**
  - **Jac Backend**: Powerful agent-based analysis with native API exposure
  - **Python Frontend**: Intuitive Streamlit interface for user interaction
- **Multi-language Support**: Analyzes Python, Jac, JavaScript, Java, C++, Rust, and Go codebases
- **Intelligent Analysis**: Tree-sitter parsing + Code Context Graphs (CCG)
- **API Integration**: RESTful endpoints for each analysis component
- **Visual Documentation**: Auto-generated diagrams of code relationships
- **Real-time Processing**: Live analysis updates and progress tracking

##  Architecture

The system combines two powerful architectures:

### Jac Backend (API Server)
1. **Repository Node**: Base entity storing repository information
2. **repo_mapper Walker**: Maps repository structure (Port 8000)
3. **code_analyzer Walker**: Deep code analysis (Port 8001)
4. **doc_generator Walker**: Documentation generation (Port 8002)
5. **doc_saver Walker**: Documentation persistence (Port 8003)

### Python Frontend
1. **Streamlit UI**: User-friendly web interface
2. **API Client**: Communicates with Jac backend services
3. **Visualization Engine**: Renders code relationships
4. **Documentation Renderer**: Displays and formats documentation

##  Quick Start

The project offers two implementation paths:

### Method 1: Pure Jac Implementation
Run the application using pure Jac implementation:
```bash
# Install dependencies
pip install -r requirements.txt

# Launch Jac version
cd jac_version
jac run genius.jac
```
This runs a self-contained Jac implementation with its own UI and processing logic.

### Method 2: Python-Jac Hybrid Implementation
Run the application using the Python frontend with Jac backend:

1. Start the FastAPI backend:
```bash
# Terminal 1
python main.py
```

2. Start the Jac services:
```bash
# Terminal 2
cd agentic_codebase_genius
jac run genius.jac
```

3. Launch the Streamlit frontend:
```bash
# Terminal 3
cd frontend
streamlit run app.py
```

##  Usage

### Via Web Interface
1. Open http://localhost:8501 in your browser
2. Enter a GitHub repository URL
3. Configure analysis options:
   - Select programming language (or auto-detect)
   - Choose documentation features
   - Enable/disable diagram generation
4. Click "Analyze Repository"
5. View and download the generated documentation

### Via API
Each component exposes a RESTful API:

```bash
# Map repository structure
curl -X POST "http://localhost:8000/repo_mapper" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/user/repo"}'

# Analyze code
curl -X POST "http://localhost:8001/code_analyzer" \
  -H "Content-Type: application/json" \
  -d '{"repo_path": "/path/to/repo"}'

# Generate documentation
curl -X POST "http://localhost:8002/doc_generator" \
  -H "Content-Type: application/json" \
  -d '{"repo_map": {...}, "ccg": {...}}'

# Save documentation
curl -X POST "http://localhost:8003/doc_saver" \
  -H "Content-Type: application/json" \
  -d '{"documentation": {...}, "repo_name": "repo-name"}'
```

##  Sample Outputs

You can find example documentation outputs in the [outputs directory](./outputs/). Here are some notable examples:

- [Recommender System Analysis](./outputs/Wachacha-jay_Recommender_system/docs.md)
  - Full codebase documentation
  - Architecture diagrams
  - API reference

## 🔧 Configuration

### Environment Variables
```bash
GITHUB_TOKEN=your_github_token  # For private repos
PORT=8000                       # API server port
DEBUG=True                      # Enable debug mode
```

### Language Detection
The system supports automatic language detection or manual selection of:
- Python (*.py)
- Jac (*.jac)
- JavaScript (*.js)
- Java (*.java)
- C++ (*.cpp, *.hpp)
- Rust (*.rs)
- Go (*.go)

##  Development

### Project Structure
```
codebase_genius/
├── README.md
├── requirements.txt
├── main.py                    # FastAPI backend server
├── agents/                    # Python implementation
│   ├── code_analyzer.py
│   ├── code_genius.py
│   ├── doc_genie.py
│   └── repo_mapper.py
├── jac_version/              # Pure Jac implementation
│   ├── app.py               # Jac app runner
│   ├── genius.jac          # Main Jac implementation
│   └── jac_utils.py        # Jac utilities
├── frontend/                 # Python-Jac hybrid frontend
│   └── app.py              # Streamlit UI
├── utils/                    # Shared utilities
│   ├── git_utils.py
│   └── language_detector.py
└── outputs/                  # Generated documentation
    └── Wachacha-jay_Recommender_system/
        └── docs.md
```

### Adding New Features
1. Implement new walker in `genius.jac`
2. Add corresponding API endpoint
3. Update frontend to utilize new functionality
4. Add tests and documentation

## Documentation

Generated documentation includes:
- Project overview and setup instructions
- API reference with function/class relationships
- Visual diagrams showing code structure
- Usage examples and best practices
- Code quality metrics and insights

##  Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [Project Repository](https://github.com/Wachacha-jay/Generative_AI_Course_Work/Codebase_genius/)
- [Sample Outputs](./outputs/)
- [API Documentation](./docs/api.md)