"""Main entry point for LLM Visualization Application"""
# -*- coding: utf-8 -*-


with entry {
    # Initialize components
    ui_manager = UIManager();
    ui_manager.setup_streamlit();
    
    # Initialize session state
    if 'model' not in st.session_state {
        st.session_state.model = Model(
            name="GPT-2 (small)",
            config=MODEL_CONFIGS["GPT-2 (small)"],
            current_stage="Introduction",
            input_text="The future of AI is"
        );
    }
    
    if 'navigator' not in st.session_state {
        st.session_state.navigator = StageNavigator();
    }
    
    if 'token_walker' not in st.session_state {
        st.session_state.token_walker = TokenFlowWalker();
    }
    
    if 'attn_walker' not in st.session_state {
        st.session_state.attn_walker = AttentionVisualizer();
    }
    
    if 'arch_traverser' not in st.session_state {
        st.session_state.arch_traverser = ArchitectureTraverser();
    }
    
    model = st.session_state.model;
    navigator = st.session_state.navigator;
    token_walker = st.session_state.token_walker;
    attn_walker = st.session_state.attn_walker;
    arch_traverser = st.session_state.arch_traverser;
    
    # Header
    st.markdown("""
        <h1 style='text-align: center; background: linear-gradient(90deg, #4A90E2, #50E3C2, #F5A623); 
             -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
             font-size: 48px; font-weight: bold; margin-bottom: 10px;'>
            🧠 LLM Architecture Visualizer
        </h1>
        <p style='text-align: center; color: #ECF0F1; font-size: 18px; margin-bottom: 30px;'>
            Interactive Deep Learning Exploration Platform
        </p>
    """, unsafe_allow_html=True);
    
    # Render sidebar and get selected model
    selected_model_name = ui_manager.render_sidebar(model, navigator);
    
    # Update model if changed
    if selected_model_name != model.name {
        model.name = selected_model_name;
        model.config = MODEL_CONFIGS[selected_model_name];
        model.config["model_name"] = selected_model_name;
    }
    
    # Tokenize input
    token_walker.tokenize_input(model);
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📐 3D Architecture", "📖 Learning Content", "🔬 Deep Dive"]);
    
    with tab1 {
        st.markdown("### 🏗️ Interactive 3D Model Architecture");
        
        # Get layers from traverser
        layers = arch_traverser.traverse_forward(model);
        
        # Create and display 3D visualization
        fig_3d = ui_manager.viz3d.create_architecture_mesh(model.config, layers);
        st.plotly_chart(fig_3d, use_container_width=True);
        
        # Layer information
        col1, col2, col3, col4 = st.columns(4);
        with col1 {
            st.metric("🔷 Attention Layers", model.config['layers']);
        }
        with col2 {
            st.metric("🔶 FFN Layers", model.config['layers']);
        }
        with col3 {
            st.metric("⚡ Attention Heads", model.config['heads']);
        }
        with col4 {
            total_params = model.config['params'];
            st.metric("📊 Total Parameters", total_params);
        }
    }
    
    with tab2 {
        # Render stage-specific content
        ui_manager.render_stage_content(
            navigator.stage_sequence[navigator.current_index],
            model.config,
            model,
            token_walker,
            attn_walker
        );
        
        # Flow diagram
        st.markdown("---");
        st.markdown("### 🔄 Process Flow");
        fig_flow = ui_manager.viz3d.create_flow_diagram(
            navigator.stage_sequence[navigator.current_index],
            model.config
        );
        st.plotly_chart(fig_flow, use_container_width=True);
    }
    
    with tab3 {
        st.markdown("### 🔬 Technical Deep Dive");
        
        deep_dive_topic = st.selectbox(
            "Select Topic",
            ["Attention Mechanism", "Position Embeddings", "Layer Normalization", 
             "Gradient Flow", "Training Dynamics", "Tokenization Algorithms"]
        );
        
        if deep_dive_topic == "Attention Mechanism" {
            st.markdown("""
            #### Mathematical Foundation
            
            The attention mechanism computes a weighted sum of values based on the compatibility 
            between queries and keys:
            """);
            
            st.latex(r"\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V");
            
            st.markdown("""
            **Step-by-step breakdown:**
            
            1. **Compute Scores**: $S = QK^T$ measures similarity between queries and keys
            2. **Scale**: Divide by $\sqrt{d_k}$ to prevent vanishing gradients
            3. **Normalize**: Apply softmax to get probabilities
            4. **Weight Values**: Multiply probabilities with values
            """);
            
            # Generate sample attention pattern
            attn_head = AttentionHead(
                head_num=0,
                parent_layer=0,
                query_weight=[],
                key_weight=[],
                value_weight=[],
                attention_scores=[]
            );
            attn_walker.compute_attention(attn_head);
            
            if attn_head.attention_scores {
                fig_attn = ui_manager.viz3d.create_attention_heatmap(
                    attn_head.attention_scores,
                    "Attention Head 1"
                );
                st.plotly_chart(fig_attn, use_container_width=True);
            }
        } elif deep_dive_topic == "Position Embeddings" {
            st.markdown("""
            #### Positional Encoding
            
            Since transformers have no inherent notion of sequence order, we add positional 
            information to the embeddings:
            """);
            
            st.latex(r"PE_{(pos, 2i)} = \sin\left(\frac{pos}{10000^{2i/d}}\right)");
            st.latex(r"PE_{(pos, 2i+1)} = \cos\left(\frac{pos}{10000^{2i/d}}\right)");
            
            # Visualize positional encodings
            pos = np.arange(50);
            d_model = 128;
            pe = np.zeros((50, d_model));
            
            for p in range(50) {
                for i in range(0, d_model, 2) {
                    pe[p, i] = np.sin(p / (10000 ** (2 * i / d_model)));
                    if i + 1 < d_model {
                        pe[p, i + 1] = np.cos(p / (10000 ** (2 * i / d_model)));
                    }
                }
            }
            
            fig_pe = go.Figure(data=go.Heatmap(
                z=pe.T,
                colorscale='RdBu',
                zmid=0
            ));
            fig_pe.update_layout(
                title="Positional Encoding Pattern",
                xaxis_title="Position",
                yaxis_title="Dimension",
                height=400,
                paper_bgcolor='rgba(30,60,114,0.3)',
                font=dict(color='white')
            );
            st.plotly_chart(fig_pe, use_container_width=True);
        }
    }
    
    # Navigation buttons
    st.markdown("---");
    col_prev, col_info, col_next = st.columns([1, 2, 1]);
    
    with col_prev {
        if st.button("⬅️ Previous Stage", use_container_width=True) {
            navigator.prev_stage(model);
            st.rerun();
        }
    }
    
    with col_info {
        current_stage = navigator.stage_sequence[navigator.current_index];
        st.markdown(f"<div style='text-align: center; padding: 10px; color: white; font-size: 18px;'>Current: <b>{current_stage}</b></div>", 
                   unsafe_allow_html=True);
    }
    
    with col_next {
        if st.button("Next Stage ➡️", use_container_width=True) {
            navigator.next_stage(model);
            st.rerun();
        }
    }
    
    # Footer
    st.markdown("---");
    st.markdown("""
        <div style='text-align: center; color: #95A5A6; padding: 20px;'>
            <p>Built with Jaclang 🚀 | Powered by Streamlit & Plotly</p>
            <p style='font-size: 12px;'>Explore transformer architectures through interactive visualization</p>
        </div>
    """, unsafe_allow_html=True);
}