"""3D and 2D visualization implementations"""

obj Visualization3D {
    can create_architecture_mesh(config: dict, layers_data: list) -> go.Figure {
        fig = go.Figure();
        
        num_layers = min(config["layers"], 12);
        
        for i in range(num_layers) {
            z_pos = i * 2.5;
            
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
            ));
            
            # Add text annotation
            fig.add_trace(go.Scatter3d(
                x=[2],
                y=[1.5],
                z=[z_pos + 0.75],
                mode='text',
                text=[f"L{i+1}"],
                textfont=dict(size=10, color='white'),
                showlegend=False
            ));
            
            # FFN block
            fig.add_trace(go.Mesh3d(
                x=[5, 9, 9, 5, 5, 9, 9, 5],
                y=[0, 0, 3, 3, 0, 0, 3, 3],
                z=[z_pos, z_pos, z_pos, z_pos, z_pos+1.5, z_pos+1.5, z_pos+1.5, z_pos+1.5],
                i=[0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 2, 3],
                j=[1, 2, 3, 4, 5, 6, 7, 5, 1, 2, 3, 0],
                k=[2, 3, 0, 5, 6, 7, 4, 6, 5, 6, 7, 4],
                color=COLOR_PALETTE["ffn"],
                opacity=0.6,
                name=f"FFN {i+1}",
                hovertemplate=f"<b>Layer {i+1}</b><br>Feed-Forward<br>Hidden: {config['hidden_dim']}<extra></extra>"
            ));
            
            # Attention heads visualization
            head_positions = np.linspace(0.5, 2.5, min(config["heads"], 8));
            for j, hpos in enumerate(head_positions) {
                fig.add_trace(go.Scatter3d(
                    x=[2],
                    y=[hpos],
                    z=[z_pos + 0.75],
                    mode='markers',
                    marker=dict(
                        size=4,
                        color='yellow',
                        symbol='diamond'
                    ),
                    name=f"Head {j+1}",
                    showlegend=False,
                    hovertext=f"Attention Head {j+1}"
                ));
            }
            
            # Residual connections
            if i < num_layers - 1 {
                fig.add_trace(go.Scatter3d(
                    x=[2, 2, 7, 7, 2],
                    y=[1.5, 1.5, 1.5, 1.5, 1.5],
                    z=[z_pos+1.5, z_pos+2, z_pos+2, z_pos+2.5, z_pos+4],
                    mode='lines',
                    line=dict(color='rgba(255,255,255,0.3)', width=3, dash='dash'),
                    showlegend=False,
                    hovertext="Residual Connection"
                ));
            }
        }
        
        # Add embedding layer at bottom
        fig.add_trace(go.Mesh3d(
            x=[-2, 11, 11, -2, -2, 11, 11, -2],
            y=[0, 0, 3, 3, 0, 0, 3, 3],
            z=[-2, -2, -2, -2, -1, -1, -1, -1],
            i=[0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 2, 3],
            j=[1, 2, 3, 4, 5, 6, 7, 5, 1, 2, 3, 0],
            k=[2, 3, 0, 5, 6, 7, 4, 6, 5, 6, 7, 4],
            color=COLOR_PALETTE["embedding"],
            opacity=0.8,
            name="Embedding Layer",
            hovertemplate=f"<b>Embedding Layer</b><br>Dimension: {config['embedding_dim']}<extra></extra>"
        ));
        
        # Add output layer at top
        top_z = num_layers * 2.5;
        fig.add_trace(go.Mesh3d(
            x=[-2, 11, 11, -2, -2, 11, 11, -2],
            y=[0, 0, 3, 3, 0, 0, 3, 3],
            z=[top_z, top_z, top_z, top_z, top_z+1, top_z+1, top_z+1, top_z+1],
            i=[0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 2, 3],
            j=[1, 2, 3, 4, 5, 6, 7, 5, 1, 2, 3, 0],
            k=[2, 3, 0, 5, 6, 7, 4, 6, 5, 6, 7, 4],
            color=COLOR_PALETTE["output"],
            opacity=0.8,
            name="Output Layer",
            hovertemplate=f"<b>Output Layer</b><br>Vocabulary: {config['vocab_size']}<extra></extra>"
        ));
        
        fig.update_layout(
            scene=dict(
                xaxis=dict(showbackground=False, showticklabels=False, title='', showgrid=False),
                yaxis=dict(showbackground=False, showticklabels=False, title='', showgrid=False),
                zaxis=dict(showbackground=False, showticklabels=True, title='Layer Depth', showgrid=True),
                camera=dict(
                    eye=dict(x=1.8, y=1.8, z=1.0),
                    center=dict(x=0, y=0, z=0)
                ),
                bgcolor='rgba(0,0,0,0)',
                aspectmode='manual',
                aspectratio=dict(x=1, y=0.8, z=2)
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=800,
            showlegend=True,
            legend=dict(
                x=0.02,
                y=0.98,
                bgcolor='rgba(0,0,0,0.5)',
                font=dict(color='white')
            ),
            title=dict(
                text=f"<b>{config.get('model_name', 'Model')} Architecture</b>",
                font=dict(size=24, color='white'),
                x=0.5,
                xanchor='center'
            ),
            hovermode='closest'
        );
        
        return fig;
    }
    
    can create_attention_heatmap(attention_matrix: list, stage: str) -> go.Figure {
        fig = go.Figure();
        
        matrix = np.array(attention_matrix);
        
        fig.add_trace(go.Heatmap(
            z=matrix,
            colorscale='Blues',
            showscale=True,
            hovertemplate='Query: %{y}<br>Key: %{x}<br>Attention: %{z:.3f}<extra></extra>'
        ));
        
        fig.update_layout(
            title=f"Attention Pattern - {stage}",
            xaxis_title="Key Position",
            yaxis_title="Query Position",
            paper_bgcolor='rgba(30,60,114,0.3)',
            plot_bgcolor='rgba(30,60,114,0.3)',
            font=dict(color='white'),
            height=400
        );
        
        return fig;
    }
    
    can create_flow_diagram(stage: str, config: dict) -> go.Figure {
        fig = go.Figure();
        
        if stage == "Tokenization" {
            nodes = ["Input Text", "Byte-Pair Encoding", "Token IDs", "Vocabulary Lookup"];
            colors = [COLOR_PALETTE["token"]] * len(nodes);
        } elif stage == "Embedding" {
            nodes = ["Token IDs", "Embedding Matrix", "Position Encoding", "Input Vectors"];
            colors = [COLOR_PALETTE["embedding"]] * len(nodes);
        } elif stage == "Self Attention" {
            nodes = ["Input", "Q/K/V Projection", "Attention Scores", "Softmax", "Weighted Sum", "Output"];
            colors = [COLOR_PALETTE["attention"]] * len(nodes);
        } elif stage == "MLP" {
            nodes = ["Input", f"Linear ({config['embedding_dim']}→{config['hidden_dim']})", 
                    "GELU", f"Linear ({config['hidden_dim']}→{config['embedding_dim']})", "Output"];
            colors = [COLOR_PALETTE["ffn"]] * len(nodes);
        } elif stage == "Residual Connection" {
            nodes = ["Input", "Sublayer", "Output", "Add & Norm"];
            colors = [COLOR_PALETTE["residual"]] * len(nodes);
        } else {
            nodes = [stage];
            colors = ['#4A90E2'];
        }
        
        x_pos = list(range(len(nodes)));
        y_pos = [0] * len(nodes);
        
        for i, (node, x, y, color) in enumerate(zip(nodes, x_pos, y_pos, colors)) {
            fig.add_trace(go.Scatter(
                x=[x],
                y=[y],
                mode='markers+text',
                marker=dict(size=80, color=color, line=dict(color='white', width=2)),
                text=[node],
                textposition="bottom center",
                textfont=dict(size=10, color='white', family='monospace'),
                showlegend=False,
                hovertext=node
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
                    arrowsize=1.5,
                    arrowwidth=4,
                    arrowcolor='white'
                );
            }
        }
        
        fig.update_layout(
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.5, len(nodes)-0.5]),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-1, 1]),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(30,60,114,0.3)',
            height=300,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=100)
        );
        
        return fig;
    }
}
