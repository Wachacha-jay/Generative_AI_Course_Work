# 🧠 LLM Architecture Visualizer

An interactive web application built with Jaclang and Streamlit for visualizing Large Language Model architectures and learning about transformer components.

## Features

- **3D Architecture Visualization**: Interactive 3D models of transformer architectures
- **Educational Content**: Step-by-step learning modules covering:
  - Tokenization
  - Embedding layers
  - Self-attention mechanisms
  - Multi-head attention
  - Feed-forward networks
  - Prediction layers
- **Model Comparison**: Support for different model architectures (GPT-2, BERT, etc.)
- **Interactive UI**: Modern, responsive interface with real-time visualizations

## Prerequisites

- Python 3.8+
- Jaclang 0.8.0+
- Streamlit 1.28.0+
- Plotly 5.17.0+
- NumPy 1.24.0+

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd llm_visualizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Method 1: Using the run script (Recommended)
```bash
python run_app.py
```

### Method 2: Manual steps
```bash
# Build the Jaclang application
jac build main.jac

# Run with Streamlit
streamlit run main.py
```

### Method 3: Direct Jaclang execution
```bash
jac run main.jac
```

## Project Structure

```
llm_visualizer/
├── main.jac              # Main application entry point
├── config.jac            # Configuration and constants
├── nodes.jac             # Node definitions for architecture components
├── walkers.jac           # Walker definitions for traversing architecture
├── render_ui.jac         # UI rendering functions
├── visualizations.py     # Python visualization implementations
├── requirements.txt      # Python dependencies
├── run_app.py           # Application runner script
└── README.md            # This file
```

## Architecture

The application uses a hybrid approach:
- **Jaclang**: For the main application logic, node definitions, and walkers
- **Python**: For visualization implementations and Streamlit integration
- **Streamlit**: For the web interface and user interactions

## Key Components

### Nodes (nodes.jac)
- `Token`: Represents individual tokens with embeddings
- `Layer`: Represents transformer layers (attention, FFN)
- `AttentionHead`: Represents individual attention heads
- `TransformerBlock`: Represents complete transformer blocks
- `Model`: Represents the complete model configuration

### Walkers (walkers.jac)
- `ArchitectureTraverser`: Traverses and visualizes the architecture
- `TokenFlowWalker`: Handles token processing and flow
- `AttentionVisualizer`: Computes and visualizes attention patterns
- `StageNavigator`: Manages navigation between learning stages

### Visualizations (visualizations.py)
- `Visualization3D`: Creates 3D interactive visualizations using Plotly
- Architecture mesh generation
- Attention heatmaps
- Process flow diagrams

## Usage

1. **Select a Model**: Choose from different model architectures in the sidebar
2. **Navigate Stages**: Use the Previous/Next buttons to explore different learning stages
3. **Explore Visualizations**: 
   - View 3D architecture in the "3D Architecture" tab
   - Learn concepts in the "Learning Content" tab
   - See predictions in the "Predictions" tab
4. **Interactive Features**: Modify input text and see real-time updates

## Troubleshooting

### Common Issues

1. **Build Errors**: Ensure Jaclang is properly installed and up to date
2. **Import Errors**: Check that all Python dependencies are installed
3. **Streamlit Issues**: Make sure Streamlit is running on the correct port (8501)

### Getting Help

If you encounter issues:
1. Check the console output for error messages
2. Ensure all dependencies are installed correctly
3. Verify that Jaclang is properly configured

## Development

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.