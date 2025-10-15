"""Main entry point for LLM Visualization Application"""
import from config { MODEL_CONFIGS, STAGES, STAGE_INFO }
import from render_ui { setup_streamlit, render_sidebar, render_tokenization_view, render_attention_view, render_prediction_view }
import streamlit as st;
import visualizations;

with entry {
    # Initialize
     ::py::
    setup_streamlit()
    
    # Initialize session state
    if 'model' not in st.session_state:
        st.session_state.model = spawn Model(
            name="GPT-2 (small)",
            config=MODEL_CONFIGS["GPT-2 (small)"],
            current_stage="Introduction",
            input_text="The future of AI is",
            animation_speed=1.0
        )
    
    if 'navigator' not in st.session_state:
        st.session_state.navigator = spawn StageNavigator()
    
    if 'token_walker' not in st.session_state:
        st.session_state.token_walker = spawn TokenFlowWalker()
    
    if 'attn_walker' not in st.session_state:
        st.session_state.attn_walker = spawn AttentionVisualizer()
    
    if 'arch_traverser' not in st.session_state:
        st.session_state.arch_traverser = spawn ArchitectureTraverser()
    
    model = st.session_state.model
    navigator = st.session_state.navigator
    token_walker = st.session_state.token_walker
    arch_traverser = st.session_state.arch_traverser
    
    # Header
    st.markdown("""
        <h1 style='text-align: center; background: linear-gradient(90deg, #4A90E2, #50E3C2, #F5A623); 
             -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
             font-size: 48px; font-weight: bold;'>
            🧠 LLM Architecture Visualizer
        </h1>
        <p style='text-align: center; color: #ECF0F1; font-size: 18px;'>
            Interactive Deep Learning Exploration Platform
        </p>
    """, unsafe_allow_html=True)
    
    # Render sidebar
    selected_model_name = render_sidebar(model, navigator)
    
    # Update model if changed
    if selected_model_name != model.name:
        model.name = selected_model_name
        model.config = MODEL_CONFIGS[selected_model_name]
        model.config["model_name"] = selected_model_name
    
    # Tokenize input
    token_walker.tokenize_input(model)
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["📐 3D Architecture", "📖 Learning Content", "🎯 Predictions"])
    
    with tab1:
        st.markdown("### 🏗️ Interactive 3D Model Architecture")
        
        # Get layers
        layers = arch_traverser.traverse_forward(model)
        
        # Create 3D visualization
        viz = visualizations.Visualization3D()
        fig_3d = viz.create_architecture_mesh(model.config, layers)
        st.plotly_chart(fig_3d, use_container_width=True)
        
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("🔷 Attention Layers", model.config['layers'])
        with col2:
            st.metric("🔶 FFN Layers", model.config['layers'])
        with col3:
            st.metric("⚡ Attention Heads", model.config['heads'])
        with col4:
            st.metric("📊 Parameters", model.config['params'])
    
    with tab2:
        current_stage = STAGES[navigator.current_index]
        stage_info = STAGE_INFO.get(current_stage, {"desc": "", "key_concepts": [], "difficulty": "Beginner"})
        
        st.markdown(f"## 📖 {current_stage}")
        st.markdown(f"**Difficulty:** {stage_info['difficulty']}")
        st.markdown(f"{stage_info['desc']}")
        
        st.markdown("---")
        
        # Stage-specific content
        if current_stage == "Tokenization":
            render_tokenization_view(model)
        elif current_stage == "Self Attention":
            render_attention_view(model.config)
        elif current_stage == "Prediction":
            render_prediction_view(model, model.config)
        else:
            st.info(f"Visualization for {current_stage} stage")
            viz = visualizations.Visualization3D()
            fig_flow = viz.create_flow_diagram(current_stage, model.config)
            st.plotly_chart(fig_flow, use_container_width=True)
        
        # Key concepts
        if stage_info['key_concepts']:
            st.markdown("### 🔑 Key Concepts")
            concepts_html = ""
            for concept in stage_info['key_concepts']:
                concepts_html += f"<span style='background: rgba(74,144,226,0.3); color: white; padding: 5px 12px; margin: 4px; border-radius: 15px; display: inline-block;'>{concept}</span>"
            st.markdown(concepts_html, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 🎯 Next Token Prediction")
        render_prediction_view(model, model.config)
    
    # Navigation
    st.markdown("---")
    col_prev, col_info, col_next = st.columns([1, 2, 1])
    
    with col_prev:
        if st.button("⬅️ Previous", use_container_width=True):
            navigator.prev_stage(model)
            st.rerun()
    
    with col_info:
        progress = navigator.get_progress(model)
        st.markdown(f"<div style='text-align: center; color: white;'>Stage {progress[0]} of {progress[1]}</div>", 
                   unsafe_allow_html=True)
    
    with col_next:
        if st.button("Next ➡️", use_container_width=True):
            navigator.next_stage(model)
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #95A5A6;'>
            <p>Built with Jaclang 🚀 | Powered by Streamlit & Plotly</p>
        </div>
    """, unsafe_allow_html=True)
    ::py::

}
