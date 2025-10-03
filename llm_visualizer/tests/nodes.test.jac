"""Unit tests for node definitions"""
import from nodes { Token, Layer, AttentionHead, TransformerBlock, Model }

test test_token_creation {
    token = Token(
        text="hello",
        token_id=1234,
        embedding=[0.1, 0.2, 0.3],
        position=0
    );
    
    assert token.text == "hello";
    assert token.token_id == 1234;
    assert len(token.embedding) == 3;
    assert token.position == 0;
}

test test_layer_creation {
    layer = Layer(
        layer_num=1,
        layer_type="attention",
        input_dim=768,
        output_dim=768,
        num_heads=12,
        position=(0, 0, 2)
    );
    
    assert layer.layer_num == 1;
    assert layer.layer_type == "attention";
    assert layer.num_heads == 12;
    assert layer.is_active == False;
}

test test_attention_head_creation {
    head = AttentionHead(
        head_num=0,
        parent_layer=1,
        query_weight=[],
        key_weight=[],
        value_weight=[],
        attention_scores=[]
    );
    
    assert head.head_num == 0;
    assert head.parent_layer == 1;
}

test test_transformer_block {
    block = TransformerBlock(
        block_num=1,
        num_layers=12,
        has_attention=True,
        has_ffn=True,
        has_norm=True
    );
    
    assert block.block_num == 1;
    assert block.has_attention == True;
    assert block.has_ffn == True;
}

test test_model_initialization {
    model = Model(
        name="GPT-2",
        config={"layers": 12},
        current_stage="Introduction"
    );
    
    assert model.name == "GPT-2";
    assert model.current_stage == "Introduction";
    assert model.animation_speed == 1.0;
}
