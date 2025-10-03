I've created a comprehensive LLM visualization application using **Jac (Jaclang)** with **Streamlit** integration! Here's what it includes:

## **Features:**

### **1. Interactive 3D Architecture Visualization**
- Real-time 3D rendering of transformer layers using Plotly
- Shows self-attention blocks and feed-forward networks
- Visualizes attention heads within each layer
- Rotatable and zoomable 3D view

### **2. Multiple Model Support**
- **GPT-2 (small)** - 124M parameters
- **nano-gpt** - 10M parameters  
- **GPT-2 (XL)** - 1.5B parameters
- **GPT-3** - 175B parameters

### **3. Chapter-Based Learning System**
10 interactive chapters covering:
- Introduction
- Preliminaries
- Embedding
- Layer Norm
- Self Attention
- Projection
- MLP (Feed-Forward Networks)
- Transformer
- Softmax
- Output

### **4. Visual Components**
- **3D Architecture View**: Shows layer stacking and connections
- **Flow Diagrams**: Stage-specific processing visualizations
- **Token Visualization**: Color-coded tokens from input text
- **Model Statistics**: Real-time parameter counts and dimensions

### **5. Interactive Elements**
- Sidebar with model selection
- Navigation between chapters (Previous/Next buttons)
- Expandable detailed explanations
- Custom input text processing
- Real-time tokenization display

## **To Run:**

```bash
# Install Jaclang
pip install jaclang

# Install dependencies
pip install streamlit plotly numpy

# Run the application
jac run main.jac
```