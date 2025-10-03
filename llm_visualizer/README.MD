# 🧠 LLM Architecture Visualizer

An interactive educational platform for visualizing and understanding transformer-based Large Language Models (LLMs) built with Jaclang and Streamlit.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Jaclang](https://img.shields.io/badge/jaclang-latest-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

## 🌟 Features

### 🏗️ Interactive 3D Architecture
- Rotatable, zoomable 3D visualization of transformer layers
- Color-coded components (attention, FFN, embeddings)
- Hover tooltips with detailed layer information
- Real-time layer highlighting during traversal

### 📚 15 Learning Stages
Progressive learning path from beginner to advanced:
1. Introduction
2. Tokenization
3. Embedding
4. Positional Encoding
5. Layer Norm
6. Self Attention
7. Multi-Head Attention
8. Projection
9. MLP (Feed-Forward Network)
10. Residual Connection
11. Transformer Block
12. Decoder Stack
13. Output Layer
14. Softmax
15. Prediction

### 🤖 Multiple Model Support
- **GPT-2 (small)**: 124M parameters, 12 layers
- **nano-gpt**: 10M parameters, 6 layers
- **GPT-2 (XL)**: 1.5B parameters, 48 layers
- **GPT-3**: 175B parameters, 96 layers
- **BERT**: 340M parameters, 24 layers

### 🎨 Advanced Visualizations
- 3D mesh rendering of layer stacks
- Attention heatmaps with causal masking
- Token flow diagrams
- Residual connection paths
- Positional encoding patterns
- GELU activation function plots

### 🚀 Walker-Based Architecture
Utilizes Jac's walker pattern for:
- **ArchitectureTraverser**: Animated layer-by-layer traversal
- **TokenFlowWalker**: Track tokens through the network
- **AttentionVisualizer**: Compute and display attention patterns
- **StageNavigator**: Manage learning progression

## 📋 Requirements

```txt
jaclang>=0.5.0
streamlit>=1.28.0
plotly>=5.17.0
numpy>=1.24.0
```

## 🚀 Installation

### Method 1: Using pip

```bash
# Clone the repository
git clone https://github.com/Wachacha-jay/llm-visualizer.git
cd llm-visualizer

# Install dependencies
pip install -r requirements.txt

# Run the application
jac run main.jac
```

### Method 2: Using Poetry

```bash
# Install poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Run the application
poetry run jac run main.jac
```

### Method 3: Using Docker

```bash
# Build the Docker image
docker build -t llm-visualizer .

# Run the container
docker run -p 8501:8501 llm-visualizer
```

## 📁 Project Structure

```
llm-visualizer/
├── main.jac                 # Entry point and session management
├── config.jac              # Model configurations and constants
├── nodes.jac               # Node definitions (Token, Layer, Model, etc.)
├── walkers.jac             # Walker implementations for traversal
├── visualizations.jac      # 3D/2D visualization logic
├── impl.jac                # UI implementation and rendering
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Poetry configuration
├── Dockerfile             # Docker configuration
├── README.md              # This file
├── LICENSE                # MIT License
└── docs/                  # Additional documentation
    ├── architecture.md    # Architecture overview
    ├── walkers.md        # Walker pattern explanation
    └── contributing.md   # Contribution guidelines
```

## 🎯 Usage

### Basic Usage

1. **Launch the application**:
   ```bash
   jac run main.jac
   ```

2. **Select a model** from the sidebar (GPT-2, GPT-3, nano-gpt, BERT)

3. **Navigate through stages** using Previous/Next buttons or the stage selector

4. **Explore tabs**:
   - **3D Architecture**: Interactive 3D model visualization
   - **Learning Content**: Stage-specific educational material
   - **Deep Dive**: Advanced technical explanations

5. **Customize input text** to see real-time tokenization and predictions

### Advanced Usage

#### Custom Model Configuration

```python
# In config.jac, add your model:
glob MODEL_CONFIGS = {
    "MyModel": {
        "layers": 32,
        "heads": 20,
        "embedding_dim": 2048,
        "hidden_dim": 8192,
        "params": "5B",
        "color": "#FF6B6B",
        "vocab_size": 50257
    }
}
```

#### Create Custom Walker

```python
# In walkers.jac, define new walker:
walker CustomAnalyzer {
    has analysis_results: dict = {};
    
    can analyze with Layer entry {
        # Your analysis logic
        self.analysis_results[here.layer_num] = {
            "type": here.layer_type,
            "params": here.input_dim * here.output_dim
        };
    }
}
```

#### Add New Visualization

```python
# In visualizations.jac:
obj Visualization3D {
    can create_custom_viz(data: dict) -> go.Figure {
        fig = go.Figure();
        # Your visualization logic
        return fig;
    }
}
```

## 🔧 Configuration

### Animation Speed
Adjust in the sidebar: 0.5x - 3.0x speed

### Display Options
- Show/Hide layer labels
- Show/Hide connections
- Toggle attention patterns

### Color Themes
Modify `COLOR_PALETTE` in `config.jac`:
```python
glob COLOR_PALETTE = {
    "attention": "#4A90E2",
    "ffn": "#50E3C2",
    "embedding": "#F5A623",
    # Add your colors...
}
```

## 📊 Examples

### Example 1: Understanding Attention

```python
# Run attention visualization walker
attn_walker = AttentionVisualizer()
attention_head = AttentionHead(
    head_num=0,
    parent_layer=0,
    query_weight=[],
    key_weight=[],
    value_weight=[],
    attention_scores=[]
)
attn_walker.compute_attention(attention_head)
```

### Example 2: Token Flow Tracking

```python
# Track token flow through layers
token_walker = TokenFlowWalker()
tokens = token_walker.tokenize_input(model)

for layer in layers:
    token_walker.flow_through_layer(layer)

print(token_walker.flow_path)
```

### Example 3: Architecture Traversal

```python
# Traverse and animate architecture
traverser = ArchitectureTraverser()
layers = traverser.traverse_forward(model)

for layer in layers:
    traverser.animate_layer_activation(layer)

print(f"Visited {len(traverser.visited_layers)} layers")
```

## 🎓 Educational Resources

### Learning Path

**Beginner (Stages 1-5)**
- Introduction to transformers
- Tokenization concepts
- Embedding spaces
- Position encoding

**Intermediate (Stages 6-10)**
- Self-attention mechanism
- Multi-head attention
- Feed-forward networks
- Layer normalization

**Advanced (Stages 11-15)**
- Complete transformer blocks
- Deep architecture patterns
- Output generation
- Sampling strategies

### Mathematical Formulas

#### Self-Attention
```
Attention(Q, K, V) = softmax(QK^T / √d_k)V
```

#### Feed-Forward Network
```
FFN(x) = GELU(xW₁ + b₁)W₂ + b₂
```

#### Positional Encoding
```
PE(pos, 2i) = sin(pos / 10000^(2i/d))
PE(pos, 2i+1) = cos(pos / 10000^(2i/d))
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](docs/contributing.md) for guidelines.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/Wachacha-jay/llm-visualizer.git
cd llm-visualizer

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
flake8 .

# Format code
black .
```

### Contribution Areas

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🎨 UI/UX enhancements
- 🧪 Test coverage
- 🌍 Internationalization

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_walkers.jac

# Run with coverage
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Jaclang Team**: For the amazing graph-based programming language
- **Streamlit**: For the intuitive web framework
- **Plotly**: For powerful visualization capabilities
- **Hugging Face**: For transformer architecture inspiration
- **Attention is All You Need**: The seminal paper on transformers

## 📞 Support

- 📧 Email: support@llmvisualizer.com
- 💬 Discord: [Join our community](https://discord.gg/llmvisualizer)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/llm-visualizer/issues)
- 📖 Docs: [Full Documentation](https://llmvisualizer.readthedocs.io)

## 🗺️ Roadmap

### Version 1.1 (Q1 2025)
- [ ] Real model inference integration
- [ ] Export visualizations as images/videos
- [ ] Comparison mode for multiple models
- [ ] Interactive quiz system

### Version 1.2 (Q2 2025)
- [ ] Mobile-responsive design
- [ ] Dark/light theme toggle
- [ ] Multi-language support (Spanish, Chinese, French)
- [ ] Save/load learning progress

### Version 2.0 (Q3 2025)
- [ ] RLHF visualization
- [ ] Fine-tuning simulator
- [ ] Model editing tools
- [ ] API for external integrations

## 📈 Stats

- ⭐ GitHub Stars: 
- 🍴 Forks: 
- 👥 Contributors: 
- 📦 Downloads: 

## 🎬 Demo

Watch our demo video: [YouTube Link](https://youtube.com/llmvisualizer)

Try the live demo: [llmvisualizer.com](https://llmvisualizer.com)

---

Made with ❤️ by the LLM Visualizer Team

**Happy Learning! 🚀**