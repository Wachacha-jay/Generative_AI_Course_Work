"""Implementation of UI and interaction logic"""

obj UIManager {
    has viz3d: Visualization3D;
    
    can init {
        self.viz3d = Visualization3D();
    }
    
    can setup_streamlit {
        st.set_page_config(
            page_title="LLM Architecture Visualizer",
            layout="wide",
            initial_sidebar_state="expanded",
            page_icon="🧠"
        );
        
        st.markdown("""
            <style>
            .main {
                background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
            }
            .stButton>button {
                width: 100%;
                border-radius: 12px;
                height: 50px;
                font-weight: bold;
                transition: all 0.3s;
            }
            .stButton>button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .metric-card {
                background: rgba(255,255,255,0.1);
                padding: 15px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            .stage-progress {
                background: linear-gradient(90deg, #4A90E2 0%, #50E3C2 100%);
                height: 8px;
                border-radius: 4px;
                margin: 10px 0;
            }
            </style>
        """, unsafe_allow_html=True);
    }
    
    can render_sidebar(model: Model, navigator: StageNavigator) -> str {
        with st.sidebar {
            st.markdown("# ⚙️ Configuration");
            
            selected_model = st.selectbox(
                "Select Model Architecture",
                list(MODEL_CONFIGS.keys()),
                index=0
            );
            
            config = MODEL_CONFIGS[selected_model];
            
            st.markdown("### 📊 Model Specifications");
            
            col1, col2 = st.columns(2);
            with col1 {
                st.markdown(f"""
                    <div class='metric-card'>
                        <div style='font-size: 24px; font-weight: bold; color: #4A90E2;'>{config['params']}</div>
                        <div style='font-size: 12px; color: #ECF0F1;'>Parameters</div>
                    </div>
                """, unsafe_allow_html=True);
            }
            with col2 {
                st.markdown(f"""
                    <div class='metric-card'>
                        <div style='font-size: 24px; font-weight: bold; color: #50E3C2;'>{config['layers']}</div>
                        <div style='font-size: 12px; color: #ECF0F1;'>Layers</div>
                    </div>
                """, unsafe_allow_html=True);
            }
            
            col3, col4 = st.columns(2);
            with col3 {
                st.markdown(f"""
                    <div class='metric-card'>
                        <div style='font-size: 24px; font-weight: bold; color: #F5A623;'>{config['heads']}</div>
                        <div style='font-size: 12px; color: #ECF0F1;'>Heads</div>
                    </div>
                """, unsafe_allow_html=True);
            }
            with col4 {
                st.markdown(f"""
                    <div class='metric-card'>
                        <div style='font-size: 24px; font-weight: bold; color: #BD10E0;'>{config['embedding_dim']}</div>
                        <div style='font-size: 12px; color: #ECF0F1;'>Embed Dim</div>
                    </div>
                """, unsafe_allow_html=True);
            }
            
            st.markdown("---");
            
            st.markdown("### 📚 Learning Path");
            
            progress_curr, progress_total = navigator.get_progress(model);
            progress_pct = (progress_curr / progress_total) * 100;
            
            st.markdown(f"""
                <div style='color: white; margin-bottom: 5px;'>
                    Progress: {progress_curr}/{progress_total} ({progress_pct:.0f}%)
                </div>
                <div class='stage-progress' style='width: {progress_pct}%;'></div>
            """, unsafe_allow_html=True);
            
            stage_names = list(STAGE_INFO.keys());
            current_stage = st.radio(
                "Select Stage",
                stage_names,
                index=navigator.current_index,
                label_visibility="collapsed"
            );
            
            st.markdown("---");
            
            st.markdown("### 🎨 Visualization Settings");
            
            animation_speed = st.slider(
                "Animation Speed",
                min_value=0.5,
                max_value=3.0,
                value=1.0,
                step=0.5
            );
            model.animation_speed = animation_speed;
            
            show_labels = st.checkbox("Show Layer Labels", value=True);
            show_connections = st.checkbox("Show Connections", value=True);
            
            st.markdown("---");
            
            st.markdown("### ✍️ Input Text");
            input_text = st.text_area(
                "Enter text to analyze",
                value=model.input_text,
                height=100,
                placeholder="Type your text here..."
            );
            model.input_text = input_text;
        }
        
        return selected_model;
    }
    
    can render_stage_content(stage: str, config: dict, model: Model, 
                            token_walker: TokenFlowWalker, 
                            attn_walker: AttentionVisualizer) {
        stage_info = STAGE_INFO[stage];
        
        st.markdown(f"## 📖 {stage}");
        
        # Difficulty badge
        difficulty_colors = {
            "Beginner": "#2ECC71",
            "Intermediate": "#F39C12",
            "Advanced": "#E74C3C"
        };
        
        col1, col2, col3 = st.columns([2, 1, 1]);
        with col1 {
            st.markdown(f"<p style='color: #ECF0F1; font-size: 16px;'>{stage_info['desc']}</p>", 
                       unsafe_allow_html=True);
        }
        with col2 {
            difficulty_color = difficulty_colors[stage_info['difficulty']];
            st.markdown(f"""
                <div style='background: {difficulty_color}; color: white; padding: 8px; 
                     border-radius: 8px; text-align: center; font-weight: bold;'>
                    {stage_info['difficulty']}
                </div>
            """, unsafe_allow_html=True);
        }
        
        st.markdown("---");
        
        # Stage-specific visualizations
        if stage == "Tokenization" {
            self.render_tokenization_view(model, token_walker);
        } elif stage == "Embedding" {
            self.render_embedding_view(config, token_walker);
        } elif stage == "Self Attention" or stage == "Multi-Head Attention" {
            self.render_attention_view(config, attn_walker);
        } elif stage == "MLP" {
            self.render_mlp_view(config);
        } elif stage == "Residual Connection" {
            self.render_residual_view(config);
        } elif stage == "Transformer Block" {
            self.render_transformer_block_view(config);
        } elif stage == "Prediction" {
            self.render_prediction_view(model, config);
        } else {
            self.render_default_view(stage, config);
        }
        
        # Key concepts
        st.markdown("### 🔑 Key Concepts");
        concepts_html = "";
        for concept in stage_info['key_concepts'] {
            concepts_html += f"<span style='background: rgba(74,144,226,0.3); color: white; padding: 5px 12px; margin: 4px; border-radius: 15px; display: inline-block;'>{concept}</span>";
        }
        st.markdown(concepts_html, unsafe_allow_html=True);
    }
    
    can render_tokenization_view(model: Model, walker: TokenFlowWalker) {
        col1, col2 = st.columns([1, 1]);
        
        with col1 {
            st.markdown("#### 📝 Input Text");
            st.markdown(f"<div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; font-size: 18px; color: white;'>{model.input_text}</div>", 
                       unsafe_allow_html=True);
        }
        
        with col2 {
            st.markdown("#### 🔤 Tokens");
            tokens = model.input_text.split();
            token_html = "<div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>";
            colors = ['#4A90E2', '#50E3C2', '#F5A623', '#BD10E0', '#E74C3C', '#9B59B6'];
            for i, token in enumerate(tokens) {
                color = colors[i % len(colors)];
                token_html += f"<div style='background: {color}; color: white; padding: 10px; margin: 5px 0; border-radius: 8px; display: flex; justify-content: space-between;'><span>{token}</span><span style='opacity: 0.7;'>ID: {1000+i}</span></div>";
            }
            token_html += "</div>";
            st.markdown(token_html, unsafe_allow_html=True);
        }
        
        st.markdown("#### 📊 Tokenization Process");
        st.code("""
# Byte-Pair Encoding (BPE) Process
1. Start with vocabulary of all characters
2. Find most frequent pair of adjacent tokens
3. Merge this pair into a new token
4. Repeat until desired vocabulary size

Example:
"learning" -> ["learn", "ing"]
"transformer" -> ["transform", "er"]
        """, language="python");
    }
    
    can render_embedding_view(config: dict, walker: TokenFlowWalker) {
        st.markdown("#### 🎯 Embedding Transformation");
        
        tokens = walker.tokens if walker.tokens else [];
        if not tokens {
            st.info("Enter text in the sidebar to see embeddings");
            return;
        }
        
        for i, token in enumerate(tokens[:3]) {  # Show first 3 tokens
            with st.expander(f"Token: {token.text} (ID: {token.token_id})", expanded=(i==0)) {
                # Show embedding vector
                embedding_sample = token.embedding[:16] if len(token.embedding) >= 16 else token.embedding;
                
                col1, col2 = st.columns([2, 1]);
                with col1 {
                    st.markdown("**Embedding Vector (first 16 dims)**");
                    embed_html = "<div style='display: flex; flex-wrap: wrap; gap: 5px;'>";
                    for val in embedding_sample {
                        opacity = min(abs(val), 1.0);
                        color = '#4A90E2' if val > 0 else '#E74C3C';
                        embed_html += f"<div style='background: {color}; opacity: {opacity}; color: white; padding: 8px; border-radius: 5px; font-family: monospace; font-size: 11px;'>{val:.3f}</div>";
                    }
                    embed_html += "</div>";
                    st.markdown(embed_html, unsafe_allow_html=True);
                }
                with col2 {
                    st.metric("Dimension", config['embedding_dim']);
                    st.metric("Position", token.position);
                }
        }
        
        st.markdown("#### 📐 Mathematical Formula");
        st.latex(r"E = \text{Embedding}(\text{token\_id}) + \text{PositionalEncoding}(\text{position})");
    }
    
    can render_attention_view(config: dict, walker: AttentionVisualizer) {
        st.markdown("#### 🎯 Multi-Head Attention Mechanism");
        
        col1, col2 = st.columns([1, 1]);
        
        with col1 {
            st.markdown("**Attention Components**");
            
            components = [
                ("Query (Q)", "What am I looking for?", "#4A90E2"),
                ("Key (K)", "What do I contain?", "#50E3C2"),
                ("Value (V)", "What do I actually represent?", "#F5A623")
            ];
            
            for name, desc, color in components {
                st.markdown(f"""
                    <div style='background: {color}; padding: 15px; margin: 8px 0; border-radius: 8px;'>
                        <div style='font-weight: bold; font-size: 16px; margin-bottom: 5px;'>{name}</div>
                        <div style='font-size: 13px; opacity: 0.9;'>{desc}</div>
                    </div>
                """, unsafe_allow_html=True);
            }
        }
        
        with col2 {
            st.markdown("**Attention Formula**");
            st.latex(r"\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V");
            
            st.markdown("**Parameters**");
            st.markdown(f"- Number of heads: **{config['heads']}**");
            st.markdown(f"- Head dimension: **{config['embedding_dim'] // config['heads']}**");
            st.markdown(f"- Total dimension: **{config['embedding_dim']}**");
        }
        
        # Attention pattern visualization
        st.markdown("#### 🔥 Attention Pattern Example");
        attention_matrix = np.random.rand(8, 8);
        # Apply causal mask
        for i in range(8) {
            for j in range(8) {
                if j > i {
                    attention_matrix[i][j] = 0;
                }
            }
        }
        attention_matrix = attention_matrix / attention_matrix.sum(axis=1, keepdims=True);
        
        fig = self.viz3d.create_attention_heatmap(attention_matrix.tolist(), "Self Attention");
        st.plotly_chart(fig, use_container_width=True);
    }
    
    can render_mlp_view(config: dict) {
        st.markdown("#### 🔄 Feed-Forward Network Structure");
        
        layers_info = [
            ("Input Layer", config['embedding_dim'], "#4A90E2"),
            ("Hidden Layer", config['hidden_dim'], "#50E3C2"),
            ("Output Layer", config['embedding_dim'], "#BD10E0")
        ];
        
        cols = st.columns(len(layers_info));
        for i, (name, dim, color) in enumerate(layers_info) {
            with cols[i] {
                st.markdown(f"""
                    <div style='background: {color}; padding: 30px 20px; border-radius: 12px; text-align: center;'>
                        <div style='font-size: 32px; font-weight: bold; margin-bottom: 10px;'>{dim}</div>
                        <div style='font-size: 14px;'>{name}</div>
                    </div>
                """, unsafe_allow_html=True);
        }
        
        st.markdown("#### 📊 Network Flow");
        st.latex(r"\text{FFN}(x) = \text{GELU}(xW_1 + b_1)W_2 + b_2");
        
        st.markdown("**GELU Activation Function:**");
        x = np.linspace(-3, 3, 100);
        y = 0.5 * x * (1 + np.tanh(np.sqrt(2/np.pi) * (x + 0.044715 * x**3)));
        
        fig = go.Figure();
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='#50E3C2', width=3)));
        fig.update_layout(
            paper_bgcolor='rgba(30,60,114,0.3)',
            plot_bgcolor='rgba(30,60,114,0.3)',
            font=dict(color='white'),
            height=300,
            xaxis_title="Input",
            yaxis_title="Output",
            title="GELU(x) = x * Φ(x)"
        );
        st.plotly_chart(fig, use_container_width=True);
    }
    
    can render_residual_view(config: dict) {
        st.markdown("#### 🔁 Residual Connections");
        
        col1, col2 = st.columns([1, 1]);
        
        with col1 {
            st.markdown("**Why Residual Connections?**");
            st.markdown("""
            - 🎯 Prevent vanishing gradients
            - 🚀 Enable training of very deep networks
            - 📈 Improve gradient flow
            - 🔄 Allow identity mapping
            """);
            
            st.markdown("**Formula:**");
            st.latex(r"\text{Output} = \text{LayerNorm}(x + \text{Sublayer}(x))");
        }
        
        with col2 {
            # Create simple residual visualization
            fig = go.Figure();
            
            # Main path
            fig.add_trace(go.Scatter(
                x=[0, 1, 2, 3],
                y=[0, 0, 0, 0],
                mode='lines+markers+text',
                line=dict(color='#4A90E2', width=4),
                marker=dict(size=20, color='#4A90E2'),
                text=["Input", "Transform", "", "Add"],
                textposition="top center",
                name="Main Path"
            ));
            
            # Skip connection
            fig.add_trace(go.Scatter(
                x=[0, 0.5, 2.5, 3],
                y=[0, -1, -1, 0],
                mode='lines+text',
                line=dict(color='#E74C3C', width=4, dash='dash'),
                text=["", "Skip", "Connection", ""],
                textposition="bottom center",
                name="Skip Connection"
            ));
            
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(30,60,114,0.3)',
                height=300,
                showlegend=True,
                xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
                font=dict(color='white')
            );
            st.plotly_chart(fig, use_container_width=True);
        }
    }
    
    can render_transformer_block_view(config: dict) {
        st.markdown("#### 🏗️ Complete Transformer Block");
        
        block_components = [
            ("1. Layer Norm", "#9B59B6"),
            ("2. Multi-Head Attention", "#4A90E2"),
            ("3. Residual Add", "#E74C3C"),
            ("4. Layer Norm", "#9B59B6"),
            ("5. Feed-Forward", "#50E3C2"),
            ("6. Residual Add", "#E74C3C")
        ];
        
        for name, color in block_components {
            st.markdown(f"""
                <div style='background: {color}; padding: 12px; margin: 8px 0; border-radius: 8px; font-weight: bold;'>
                    {name}
                </div>
            """, unsafe_allow_html=True);
        }
        
        st.markdown(f"**Total Blocks in Model:** {config['layers']}");
    }
    
    can render_prediction_view(model: Model, config: dict) {
        st.markdown("#### 🎲 Next Token Prediction");
        
        col1, col2 = st.columns([2, 1]);
        
        with col1 {
            st.markdown("**Input Context:**");
            st.markdown(f"<div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; font-size: 18px;'>{model.input_text} <span style='color: #4A90E2;'>|</span></div>", 
                       unsafe_allow_html=True);
            
            st.markdown("**Top Predictions:**");
            
            predictions = [
                ("bright", 0.28),
                ("promising", 0.22),
                ("revolutionary", 0.18),
                ("transformative", 0.15),
                ("uncertain", 0.08),
                ("exciting", 0.09)
            ];
            
            for word, prob in predictions {
                st.markdown(f"""
                    <div style='margin: 10px 0;'>
                        <div style='display: flex; justify-content: space-between; margin-bottom: 5px;'>
                            <span style='font-weight: bold;'>{word}</span>
                            <span style='color: #4A90E2;'>{prob*100:.1f}%</span>
                        </div>
                        <div style='background: rgba(255,255,255,0.1); border-radius: 10px; height: 8px;'>
                            <div style='background: linear-gradient(90deg, #4A90E2, #50E3C2); width: {prob*100}%; height: 100%; border-radius: 10px;'></div>
                        </div>
                    </div>
                """, unsafe_allow_html=True);
            }
        }
        
        with col2 {
            st.markdown("**Sampling Strategy:**");
            
            sampling_method = st.radio(
                "Method",
                ["Greedy", "Top-k", "Top-p (Nucleus)", "Temperature"],
                label_visibility="collapsed"
            );
            
            if sampling_method == "Temperature" {
                temp = st.slider("Temperature", 0.1, 2.0, 1.0, 0.1);
                st.info(f"Higher temperature ({temp}) = more random");
            } elif sampling_method == "Top-k" {
                k = st.slider("k value", 1, 50, 10);
                st.info(f"Sample from top {k} tokens");
            } elif sampling_method == "Top-p (Nucleus)" {
                p = st.slider("p value", 0.1, 1.0, 0.9, 0.05);
                st.info(f"Sample from top {p*100}% cumulative probability");
            }
            
            st.markdown("**Model Info:**");
            st.metric("Vocabulary Size", f"{config['vocab_size']:,}");
    }
    
    can render_default_view(stage: str, config: dict) {
        st.info(f"Visualization for {stage} is being prepared...");
        
        # Show flow diagram
        fig = self.viz3d.create_flow_diagram(stage, config);
        st.plotly_chart(fig, use_container_width=True);
    }
}
