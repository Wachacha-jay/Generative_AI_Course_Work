"""Unit tests for visualization components"""

import from visualizations {Visualization3D }
import from config { MODEL_CONFIGS }

test test_create_architecture_mesh {
    viz = Visualization3D();
    config = MODEL_CONFIGS["GPT-2 (small)"];
    config["model_name"] = "GPT-2 (small)";
    
    fig = viz.create_architecture_mesh(config, []);
    
    assert fig is not None;
    assert "scene" in fig.layout;
}

test test_create_attention_heatmap {
    viz = Visualization3D();
    attention_matrix = [[0.5, 0.3, 0.2], [0.2, 0.6, 0.2], [0.1, 0.3, 0.6]];
    
    fig = viz.create_attention_heatmap(attention_matrix, "Test Stage");
    
    assert fig is not None;
    assert len(fig.data) > 0;
}

test test_create_flow_diagram {
    viz = Visualization3D();
    config = {"embedding_dim": 768, "hidden_dim": 3072};
    
    fig = viz.create_flow_diagram("Embedding", config);
    
    assert fig is not None;
    assert len(fig.data) > 0;
}