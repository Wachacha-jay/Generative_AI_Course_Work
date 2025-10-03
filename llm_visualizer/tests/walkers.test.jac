"""Unit tests for walker implementations"""

import pytest;
import from walkers {ArchitectureTraverser, TokenFlowWalker, AttentionVisualizer, StageNavigator}
import from nodes {Model, Layer, Token}
import from config {MODEL_CONFIGS}

test test_architecture_traverser {
    model = Model(
        name="GPT-2 (small)",
        config=MODEL_CONFIGS["GPT-2 (small)"],
        current_stage="Introduction"
    );
    
    traverser = ArchitectureTraverser();
    layers = traverser.traverse_forward(model);
    
    assert len(layers) > 0;
    assert len(layers) == model.config["layers"] * 2;  # attention + ffn
}

test test_token_flow_walker {
    model = Model(
        name="GPT-2",
        config={"embedding_dim": 768},
        input_text="Hello world"
    );
    
    walker = TokenFlowWalker();
    tokens = walker.tokenize_input(model);
    
    assert len(tokens) == 2;
    assert tokens[0].text == "Hello";
    assert tokens[1].text == "world";
}

test test_attention_visualizer {
    walker = AttentionVisualizer();
    head = AttentionHead(
        head_num=0,
        parent_layer=0,
        query_weight=[],
        key_weight=[],
        value_weight=[],
        attention_scores=[]
    );
    
    walker.compute_attention(head);
    
    assert len(walker.attention_matrices) > 0;
    assert head.attention_scores is not None;
}

test test_stage_navigator {
    model = Model(
        name="GPT-2",
        config={},
        current_stage="Introduction"
    );
    
    navigator = StageNavigator();
    
    # Test next stage
    next_stage = navigator.next_stage(model);
    assert next_stage == "Tokenization";
    
    # Test progress
    progress = navigator.get_progress(model);
    assert progress[0] == 2;  # Current is 2nd stage
    
    # Test prev stage
    prev_stage = navigator.prev_stage(model);
    assert prev_stage == "Introduction";
}
