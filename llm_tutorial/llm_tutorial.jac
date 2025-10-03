"""
LLM Visualization Application using Jac and Streamlit
This creates an interactive 3D visualization of transformer architectures
"""

# main.jac
import streamlit as st;
import plotly.graph_objects as go;
import numpy as np;
import from typing {Dict, List, Tuple}

# Model configurations
glob model_configs = {
    "GPT-2 (small)": {
        "layers": 12,
        "heads": 12,
        "embedding_dim": 768,
        "hidden_dim": 3072,
        "params": "124M",
        "color": "#4A90E2"
    },
    "nano-gpt": {
        "layers": 6,
        "heads": 6,
        "embedding_dim": 384,
        "hidden_dim": 1536,
        "params": "10M",
        "color": "#50E3C2"
    },
    "GPT-2 (XL)": {
        "layers": 48,
        "heads": 25,
        "embedding_dim": 1600,
        "hidden_dim": 6400,
        "params": "1.5B",
        "color": "#F5A623"
    },
    "GPT-3": {
        "layers": 96,
        "heads": 96,
        "embedding_dim": 12288,
        "hidden_dim": 49152,
        "params": "175B",
        "color": "#BD10E0"
    }
};

# Visualization stages
glob stages = [
    "Introduction",
    "Preliminaries",
    "Embedding",
    "Layer Norm",
    "Self Attention",
    "Projection",
    "MLP",
    "Transformer",
    "Softmax",
    "Output"
];

node LLMVisualizer {
    has selected_model: str = "GPT-2 (small)";
    has current_stage: str = "Introduction";
    has input_text: str = "The future of AI is";
    
    can init_streamlit {
        st.set_page_config(
            page_title="LLM Visualization",
            layout="wide",
            initial_sidebar_state="expanded"
        );
        
        # Custom CSS
        st.markdown("""
            <style>
            .main {
                background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            }
            .stButton>button {
                width: 100%;
                border-radius: 10px;
                height: 60px;
                font-weight: bold;
            }
            .stage-button {
                background-color: #2C3E50;
                color: white;
                padding: 15px;
                margin: 5px 0;
                border-radius: 8px;
                cursor: pointer;
            }
            .stage-button:hover {
                background-color: #34495E;
            }
            </style>
        """, unsafe_allow_html=True);
    }
    
    can create_3d_architecture(model_name: str) -> go.Figure {
        config = model_configs[model_name];
        layers = config["layers"];
        heads = config["heads"];
        
        fig = go.Figure();
        
        # Create layer blocks
        for i in range(min(layers, 10)) {
            z_pos = i * 2;
            
            # Self-attention blocks
            fig.add_trace(go.Mesh3d(
                x=[0, 4, 4, 0, 0, 4, 4, 0],
                y=[0, 0, 3, 3, 0, 0, 3, 3],
                z=[z_pos, z_pos, z_pos, z_pos, z_pos+1, z_pos+1, z_pos+1, z_pos+1],
                i=[0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 2, 3],
                j=[1, 2, 3, 4, 5, 6, 7, 5, 1, 2, 3, 0],
                k=[2, 3, 0, 5, 6, 7, 4, 6, 5, 6, 7, 4],
                color=config["color"],
                opacity=0.7,
                name=f"Layer {i+1}",
                hovertext=f"Self-Attention Layer {i+1}"
            ));
            
            # FFN blocks
            fig.add_trace(go.Mesh3d(
                x=[5, 9, 9, 5, 5, 9, 9, 5],
                y=[0, 0, 3, 3, 0, 0, 3, 3],
                z=[z_pos, z_pos, z_pos, z_pos, z_pos+1, z_pos+1, z_pos+1, z_pos+1],
                i=[0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 2, 3],
                j=[1, 2, 3, 4, 5, 6, 7, 5, 1, 2, 3, 0],
                k=[2, 3, 0, 5, 6, 7, 4, 6, 5, 6, 7, 4],
                color="#50E3C2",
                opacity=0.6,
                name=f"FFN {i+1}",
                hovertext=f"Feed-Forward Network {i+1}"
            ));
            
            # Attention heads visualization
            head_positions = np.linspace(0.5, 3.5, min(heads, 8));
            for j, hpos in enumerate(head_positions) {
                fig.add_trace(go.Scatter3d(
                    x=[2],
                    y=[hpos],
                    z=[z_pos + 0.5],
                    mode='markers',
                    marker=dict(size=3, color='yellow'),
                    name=f"Head {j+1}",
                    showlegend=False
                ));
            }
        }
        
        # Add connections between layers
        for i in range(min(layers-1, 9)) {
            z_pos = i * 2;
            fig.add_trace(go.Scatter3d(
                x=[2, 2],
                y=[1.5, 1.5],
                z=[z_pos+1, z_pos+2],
                mode='lines',
                line=dict(color='white', width=2),
                showlegend=False
            ));
        }
        
        fig.update_layout(
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, title=''),
                yaxis=dict(showbackground=False, showticklabels=False, title=''),
                zaxis=dict(showbackground=False, showticklabels=False, title='Layers'),
                camera=dict(
                    eye=dict(x=1.5, y=1.5, z=1.2)
                ),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=700,
            showlegend=False,
            title=dict(
                text=f"{model_name} Architecture",
                font=dict(size=24, color='white')
            )
        );
        
        return fig;
    }
    
    can create_flow_diagram(stage: str) -> go.Figure {
        fig = go.Figure();
        
        if stage == "Embedding" {
            # Token embedding visualization
            nodes = ["Input Text", "Tokenization", "Token IDs", "Embedding Layer", "Vector Representations"];
            x_pos = [0, 1, 2, 3, 4];
            y_pos = [0, 0, 0, 0, 0];
            
            for i, (node, x, y) in enumerate(zip(nodes, x_pos, y_pos)) {
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers+text',
                    marker=dict(size=60, color=['#4A90E2', '#50E3C2', '#F5A623', '#BD10E0', '#E74C3C'][i]),
                    text=[node],
                    textposition="bottom center",
                    textfont=dict(size=12, color='white'),
                    showlegend=False
                ));
                
                if i < len(nodes) - 1 {
                    fig.add_annotation(
                        x=x+0.5,
                        y=y,
                        ax=x,
                        ay=y,
                        xref='x',
                        yref='y',
                        axref='x',
                        ayref='y',
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=3,
                        arrowcolor='white'
                    );
                }
            }
        } elif stage == "Self Attention" {
            # Multi-head attention visualization
            components = ["Query (Q)", "Key (K)", "Value (V)", "Attention Scores", "Weighted Sum"];
            x_pos = [0, 0, 0, 1.5, 3];
            y_pos = [2, 0, -2, 0, 0];
            
            for comp, x, y in zip(components, x_pos, y_pos) {
                color = '#4A90E2' if 'Q' in comp or 'K' in comp or 'V' in comp else '#BD10E0';
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers+text',
                    marker=dict(size=70, color=color),
                    text=[comp],
                    textposition="middle center",
                    textfont=dict(size=10, color='white'),
                    showlegend=False
                ));
            }
            
            # Add attention connections
            for i in range(3) {
                fig.add_annotation(
                    x=1.5,
                    y=0,
                    ax=0,
                    ay=y_pos[i],
                    xref='x',
                    yref='y',
                    axref='x',
                    ayref='y',
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor='white'
                );
            }
            
            fig.add_annotation(
                x=3,
                y=0,
                ax=1.5,
                ay=0,
                xref='x',
                yref='y',
                axref='x',
                ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=3,
                arrowcolor='#50E3C2'
            );
        } elif stage == "MLP" {
            # Feed-forward network
            layers_viz = ["Input", "Linear 1", "Activation (GELU)", "Linear 2", "Output"];
            x_pos = list(range(len(layers_viz)));
            y_pos = [0] * len(layers_viz);
            
            for layer, x, y in zip(layers_viz, x_pos, y_pos) {
                fig.add_trace(go.Scatter(
                    x=[x],
                    y=[y],
                    mode='markers+text',
                    marker=dict(size=70, color='#50E3C2'),
                    text=[layer],
                    textposition="bottom center",
                    textfont=dict(size=11, color='white'),
                    showlegend=False
                ));
                
                if x < len(layers_viz) - 1 {
                    fig.add_annotation(
                        x=x+0.5,
                        y=y,
                        ax=x,
                        ay=y,
                        xref='x',
                        yref='y',
                        axref='x',
                        ayref='y',
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=3,
                        arrowcolor='white'
                    );
                }
            }
        } else {
            # Default flow
            fig.add_annotation(
                text=f"Visualizing: {stage}",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=24, color='white')
            );
        }
        
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(30,60,114,0.3)',
            height=400,
            showlegend=False
        );
        
        return fig;
    }
    
    can render_ui {
        self.init_streamlit();
        
        # Header
        st.markdown("<h1 style='text-align: center; color: white;'>🧠 LLM Visualization</h1>", 
                   unsafe_allow_html=True);
        st.markdown("<p style='text-align: center; color: #ECF0F1;'>Interactive Transformer Architecture Explorer</p>",
                   unsafe_allow_html=True);
        
        # Sidebar
        with st.sidebar {
            st.markdown("## ⚙️ Configuration");
            
            # Model selection
            self.selected_model = st.selectbox(
                "Select Model",
                list(model_configs.keys()),
                index=0
            );
            
            config = model_configs[self.selected_model];
            
            # Model info
            st.markdown("### 📊 Model Stats");
            st.metric("Parameters", config["params"]);
            st.metric("Layers", config["layers"]);
            st.metric("Attention Heads", config["heads"]);
            st.metric("Embedding Dim", config["embedding_dim"]);
            
            st.markdown("---");
            
            # Stage navigation
            st.markdown("### 📚 Chapters");
            self.current_stage = st.radio(
                "Select Stage",
                stages,
                index=0
            );
            
            st.markdown("---");
            
            # Input text
            st.markdown("### ✍️ Input Text");
            self.input_text = st.text_input(
                "Enter text",
                value=self.input_text,
                placeholder="Type your text here..."
            );
        }
        
        # Main content area
        col1, col2 = st.columns([2, 1]);
        
        with col1 {
            st.markdown("### 🏗️ 3D Architecture View");
            fig_3d = self.create_3d_architecture(self.selected_model);
            st.plotly_chart(fig_3d, use_container_width=True);
        }
        
        with col2 {
            st.markdown(f"### 📖 Chapter: {self.current_stage}");
            
            # Stage description
            stage_descriptions = {
                "Introduction": "Learn about transformer architectures and how LLMs process text.",
                "Preliminaries": "Understand the basic components: tokens, embeddings, and attention.",
                "Embedding": "Convert tokens into continuous vector representations.",
                "Layer Norm": "Normalize activations to stabilize training.",
                "Self Attention": "Learn how tokens attend to each other using Q, K, V matrices.",
                "Projection": "Project attention outputs back to the embedding space.",
                "MLP": "Feed-forward networks process each position independently.",
                "Transformer": "Combine attention and MLP layers with residual connections.",
                "Softmax": "Convert logits to probability distributions.",
                "Output": "Generate next token predictions from the final layer."
            };
            
            st.info(stage_descriptions.get(self.current_stage, "Exploring transformer architecture..."));
            
            # Token visualization
            if self.input_text {
                st.markdown("#### 🔤 Tokenization");
                tokens = self.input_text.split();
                token_html = "";
                for i, token in enumerate(tokens) {
                    color = ['#4A90E2', '#50E3C2', '#F5A623', '#BD10E0', '#E74C3C'][i % 5];
                    token_html += f"<span style='background-color: {color}; color: white; padding: 5px 10px; margin: 3px; border-radius: 5px; display: inline-block;'>{token}</span>";
                }
                st.markdown(token_html, unsafe_allow_html=True);
            }
        }
        
        # Flow diagram
        st.markdown("---");
        st.markdown("### 🔄 Processing Flow");
        fig_flow = self.create_flow_diagram(self.current_stage);
        st.plotly_chart(fig_flow, use_container_width=True);
        
        # Detailed explanation
        with st.expander(f"📝 Detailed Explanation: {self.current_stage}") {
            if self.current_stage == "Self Attention" {
                st.markdown("""
                **Multi-Head Self-Attention Mechanism:**
                
                The attention mechanism allows the model to focus on different parts of the input sequence:
                
                1. **Query (Q), Key (K), Value (V)**: Linear projections of the input
                2. **Attention Scores**: Calculate similarity between queries and keys
                3. **Softmax**: Normalize scores to probabilities
                4. **Weighted Sum**: Multiply values by attention weights
                
                Formula: `Attention(Q, K, V) = softmax(QK^T / √d_k)V`
                
                With multiple heads, the model can attend to different aspects simultaneously.
                """);
            } elif self.current_stage == "MLP" {
                st.markdown("""
                **Feed-Forward Network (FFN):**
                
                After attention, each position goes through a 2-layer MLP:
                
                1. **Linear Projection**: Expand to hidden dimension (4x embedding size)
                2. **Activation**: Apply GELU non-linearity
                3. **Linear Projection**: Project back to embedding dimension
                
                Formula: `FFN(x) = GELU(xW₁ + b₁)W₂ + b₂`
                
                This allows the model to learn complex transformations.
                """);
            } elif self.current_stage == "Embedding" {
                st.markdown("""
                **Token Embeddings:**
                
                Text is converted into numerical representations:
                
                1. **Tokenization**: Split text into subwords (BPE/WordPiece)
                2. **Token IDs**: Map tokens to vocabulary indices
                3. **Embedding Lookup**: Convert IDs to dense vectors
                4. **Position Encoding**: Add positional information
                
                Each token becomes a {}-dimensional vector.
                """.format(config["embedding_dim"]));
            } else {
                st.markdown(f"Learn more about **{self.current_stage}** in the transformer architecture.");
            }
        }
        
        # Navigation buttons
        st.markdown("---");
        col_prev, col_next = st.columns([1, 1]);
        
        with col_prev {
            current_idx = stages.index(self.current_stage);
            if current_idx > 0 and st.button("⬅️ Previous", use_container_width=True) {
                self.current_stage = stages[current_idx - 1];
                st.rerun();
            }
        }
        
        with col_next {
            current_idx = stages.index(self.current_stage);
            if current_idx < len(stages) - 1 and st.button("Next ➡️", use_container_width=True) {
                self.current_stage = stages[current_idx + 1];
                st.rerun();
            }
        }
    }
}

with entry {
    visualizer = LLMVisualizer();
    visualizer.render_ui();
}