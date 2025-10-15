"""Node definitions for LLM architecture components"""

node Token {
    has text: str;
    has token_id: int;
    has embedding: list;
    has position: int;
}


node Layer {
    has layer_num: int;
    has layer_type: str;
    has input_dim: int;
    has output_dim: int;
    has num_heads: int;
    has position: tuple;
    has is_active: bool;
}


node AttentionHead {
    has head_num: int;
    has parent_layer: int;
    has attention_scores: list;
}


node TransformerBlock {
    has block_num: int;
    has num_layers: int;
    has has_attention: bool;
    has has_ffn: bool;
}


node Model {
    has name: str;
    has config: dict;
    has current_stage: str;
    has input_text: str;
    has animation_speed: float;
}
