"""
3D and 2D visualization implementations using pure Python
This file is imported by the Jac code
"""

import plotly.graph_objects as go
import numpy as np
from typing import Dict, List, Tuple

class Visualization3D:
    """Handle all visualization logic in Python"""
    
    def __init__(self):
        self.color_palette = {
            "attention": "#4A90E2",
            "ffn": "#50E3C2",
            "embedding": "#F5A623",
            "output": "#BD10E0",
            "residual": "#E74C3C"
        }
    
    def create_architecture_mesh(self, config: Dict, layers_data: List) -> go.Figure:
        """Create 3D mesh visualization of architecture"""
        fig = go.Figure()
        
        num_layers = min(config["layers"], 12)
        
        for i in range(num_layers):
            z_pos = i * 2.5
            
            # Self-attention block
            fig.add_trace(go.Mesh3d(
                x=[0, 4, 4, 0, 0, 4, 4, 0],
                y=[0, 0, 3, 3, 0, 0, 3, 3],
                z=[z_pos, z_pos, z_pos, z_pos, z_pos+1.5, z_pos+1.5, z_pos+1.5, z_pos+1.5],
                i=[0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 2, 3],
                j=[1, 2, 3, 4, 5, 6, 7, 5, 1, 2, 3, 0],
                k=[2, 3, 0, 5, 6, 7, 4, 6, 5, 6, 7, 4],
                color=config["color"],
                opacity=0.7,
                name=f"Attention {i+1}",
                hovertemplate=f"<b>Layer {i+1}</b><br>Self-Attention<br>Heads: {config['heads']}<extra></extra>"
            ))
            
            # FFN block
            fig.add_trace(go.Mesh3d(
                x=[5, 9, 9, 5, 5, 9, 9, 5],
                y=[0, 0, 3, 3, 0, 0, 3, 3],
                z=[z_pos, z_pos, z_pos, z_pos, z_pos+1.5, z_pos+1.5, z_pos+1.5, z_pos+1.5],
                i=[0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 2, 3],
                j=[1, 2, 3, 4, 5, 6, 7, 5, 1, 2, 3, 0],
                k=[2, 3, 0, 5, 6, 7, 4, 6, 5, 6, 7, 4],
                color=self.color_palette["ffn"],
                opacity=0.6,
                name=f"FFN {i+1}",
                hovertemplate=f"<b>Layer {i+1}</b><br>Feed-Forward<extra></extra>"
            ))
            
            # Attention heads
            head_positions = np.linspace(0.5, 2.5, min(config["heads"], 8))
            for j, hpos in enumerate(head_positions):
                fig.add_trace(go.Scatter3d(
                    x=[2],
                    y=[hpos],
                    z=[z_pos + 0.75],
                    mode='markers',
                    marker=dict(size=4, color='yellow', symbol='diamond'),
                    showlegend=False,
                    hovertext=f"Attention Head {j+1}"
                ))
        
        # Add embedding layer
        fig.add_trace(go.Mesh3d(
            x=[-2, 11, 11, -2, -2, 11, 11, -2],
            y=[0, 0, 3, 3, 0, 0, 3, 3],
            z=[-2, -2, -2, -2, -1, -1, -1, -1],
            i=[0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 2, 3],
            j=[1, 2, 3, 4, 5, 6, 7, 5, 1, 2, 3, 0],
            k=[2, 3, 0, 5, 6, 7, 4, 6, 5, 6, 7, 4],
            color=self.color_palette["embedding"],
            opacity=0.8,
            name="Embedding Layer",
            hovertemplate=f"<b>Embedding Layer</b><br>Dim: {config['embedding_dim']}<extra></extra>"
        ))
        
        fig.update_layout(
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, title=''),
                yaxis=dict(showbackground=False, showticklabels=False, title=''),
                zaxis=dict(showbackground=False, title='Layer Depth'),
                camera=dict(eye=dict(x=1.8, y=1.8, z=1.0)),
                bgcolor='rgba(0,0,0,0)'
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=700,
            showlegend=True,
            title=dict(
                text=f"<b>{config.get('model_name', 'Model')} Architecture</b>",
                font=dict(size=24, color='white'),
                x=0.5
            )
        )
        
        return fig
    
    def create_attention_heatmap(self, attention_matrix: List, stage: str) -> go.Figure:
        """Create attention pattern heatmap"""
        fig = go.Figure()
        
        matrix = np.array(attention_matrix)
        
        fig.add_trace(go.Heatmap(
            z=matrix,
            colorscale='Blues',
            showscale=True,
            hovertemplate='Query: %{y}<br>Key: %{x}<br>Attention: %{z:.3f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"Attention Pattern - {stage}",
            xaxis_title="Key Position",
            yaxis_title="Query Position",
            paper_bgcolor='rgba(30,60,114,0.3)',
            plot_bgcolor='rgba(30,60,114,0.3)',
            font=dict(color='white'),
            height=400
        )
        
        return fig
    
    def create_flow_diagram(self, stage: str, config: Dict) -> go.Figure:
        """Create process flow diagram"""
        fig = go.Figure()
        
        if stage == "Tokenization":
            nodes = ["Input Text", "Byte-Pair Encoding", "Token IDs", "Vocabulary Lookup"]
            colors = [self.color_palette["attention"]] * len(nodes)
        elif stage == "Embedding":
            nodes = ["Token IDs", "Embedding Matrix", "Position Encoding", "Input Vectors"]
            colors = [self.color_palette["embedding"]] * len(nodes)
        elif stage == "Self Attention":
            nodes = ["Input", "Q/K/V Projection", "Attention Scores", "Softmax", "Output"]
            colors = [self.color_palette["attention"]] * len(nodes)
        elif stage == "MLP":
            nodes = ["Input", f"Linear ({config['embedding_dim']}→{config['hidden_dim']})", 
                    "GELU", f"Linear ({config['hidden_dim']}→{config['embedding_dim']})", "Output"]
            colors = [self.color_palette["ffn"]] * len(nodes)
        else:
            nodes = [stage]
            colors = ['#4A90E2']
        
        x_pos = list(range(len(nodes)))
        y_pos = [0] * len(nodes)
        
        for i, (node, x, y, color) in enumerate(zip(nodes, x_pos, y_pos, colors)):
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers+text',
                marker=dict(size=80, color=color, line=dict(color='white', width=2)),
                text=[node],
                textposition="bottom center",
                textfont=dict(size=10, color='white'),
                showlegend=False
            ))
            
            if i < len(nodes) - 1:
                fig.add_annotation(
                    x=x+0.5, y=y,
                    ax=x, ay=y,
                    xref='x', yref='y',
                    axref='x', ayref='y',
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1.5,
                    arrowwidth=4,
                    arrowcolor='white'
                )
        
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(30,60,114,0.3)',
            height=300,
            showlegend=False
        )
        
        return fig