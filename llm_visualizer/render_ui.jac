"""Implementation of UI and interaction logic"""

import streamlit as st;
# Visualization3D will be imported in Python code blocks


def setup_streamlit() {
    ::py::
    st.set_page_config(
        page_title="LLM Architecture Visualizer",
        layout="wide",
        initial_sidebar_state="expanded",
        page_icon="🧠"
    )
    
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
        }
        </style>
    """, unsafe_allow_html=True)
    ::py::

}


def render_sidebar(model: Model, navigator: StageNavigator) -> str {
    ::py::
    from config import MODEL_CONFIGS, STAGES
    
    with st.sidebar:
        st.markdown("# ⚙️ Configuration")
        
        selected_model = st.selectbox(
            "Select Model Architecture",
            list(MODEL_CONFIGS.keys()),
            index=0
        )
        
        config = MODEL_CONFIGS[selected_model]
        
        st.markdown("### 📊 Model Specifications")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Parameters", config['params'])
            st.metric("Layers", config['layers'])
        with col2:
            st.metric("Heads", config['heads'])
            st.metric("Embed Dim", config['embedding_dim'])
        
        st.markdown("---")
        st.markdown("### 📚 Learning Path")
        
        current_stage = st.radio(
            "Select Stage",
            STAGES,
            index=navigator["current_index"]
        )
        
        st.markdown("---")
        st.markdown("### ✍️ Input Text")
        input_text = st.text_area(
            "Enter text to analyze",
            value=model["input_text"],
            height=100
        )
        model["input_text"] = input_text
    
    return selected_model
    ::py::
}


def render_tokenization_view(model: Model) {
    ::py::
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📝 Input Text")
        st.markdown(f"<div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; font-size: 18px; color: white;'>{model['input_text']}</div>", 
                   unsafe_allow_html=True)
    
    with col2:
        st.markdown("#### 🔤 Tokens")
        tokens = model['input_text'].split()
        colors = ['#4A90E2', '#50E3C2', '#F5A623', '#BD10E0', '#E74C3C']
        token_html = "<div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;'>"
        for i, token in enumerate(tokens):
            color = colors[i % len(colors)]
            token_html += f"<div style='background: {color}; color: white; padding: 10px; margin: 5px 0; border-radius: 8px;'>{token} (ID: {1000+i})</div>"
        token_html += "</div>"
        st.markdown(token_html, unsafe_allow_html=True)
    ::py::
}


def render_attention_view(config: dict) {
    ::py::
    import numpy as np
    from visualizations import Visualization3D
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Attention Components**")
        components = [
            ("Query (Q)", "What am I looking for?", "#4A90E2"),
            ("Key (K)", "What do I contain?", "#50E3C2"),
            ("Value (V)", "What do I represent?", "#F5A623")
        ]
        
        for name, desc, color in components:
            st.markdown(f"""
                <div style='background: {color}; padding: 15px; margin: 8px 0; border-radius: 8px;'>
                    <div style='font-weight: bold; font-size: 16px;'>{name}</div>
                    <div style='font-size: 13px;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Attention Formula**")
        st.latex(r"\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V")
        st.markdown(f"- Number of heads: **{config['heads']}**")
        st.markdown(f"- Head dimension: **{config['embedding_dim'] // config['heads']}**")
    
    # Attention heatmap
    st.markdown("#### 🔥 Attention Pattern")
    attention_matrix = np.random.rand(8, 8)
    for i in range(8):
        for j in range(8):
            if j > i:
                attention_matrix[i][j] = 0
    attention_matrix = attention_matrix / attention_matrix.sum(axis=1, keepdims=True)
    
    viz = Visualization3D()
    fig = viz.create_attention_heatmap(attention_matrix.tolist(), "Self Attention")
    st.plotly_chart(fig, use_container_width=True)
    ::py::
}


def render_prediction_view(model: Model, config: dict) {
    ::py::
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("**Input Context:**")
        st.markdown(f"<div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; font-size: 18px;'>{model['input_text']} <span style='color: #4A90E2;'>|</span></div>", 
                   unsafe_allow_html=True)
        
        st.markdown("**Top Predictions:**")
        predictions = [
            ("bright", 0.28),
            ("promising", 0.22),
            ("revolutionary", 0.18),
            ("transformative", 0.15),
            ("uncertain", 0.08)
        ]
        
        for word, prob in predictions:
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
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Model Info:**")
        st.metric("Vocabulary Size", f"{config['vocab_size']:,}")
    ::py::
}
