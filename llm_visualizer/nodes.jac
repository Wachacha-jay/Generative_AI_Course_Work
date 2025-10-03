"""Node definitions for LLM architecture components"""

node Token {
    has text: str;
    has token_id: int;
    has embedding: list[float];
    has position: int;
}

node Layer {
    has layer_num: int;
    has layer_type: str;  # "attention" or "ffn" or "norm"
    has input_dim: int;
    has output_dim: int;
    has num_heads: int = 0;
    has position: tuple = (0, 0, 0);
    has is_active: bool = False;
}

node AttentionHead {
    has head_num: int;
    has parent_layer: int;
    has query_weight: list[list[float]];
    has key_weight: list[list[float]];
    has value_weight: list[list[float]];
    has attention_scores: list[list[float]];
}

node TransformerBlock {
    has block_num: int;
    has num_layers: int;
    has has_attention: bool = True;
    has has_ffn: bool = True;
    has has_norm: bool = True;
}

node Model {
    has name: str;
    has config: dict;
    has current_stage: str = "Introduction";
    has input_text: str = "The future of AI is";
    has animation_speed: float = 1.0;
}

node StageNode {
    has stage_name: str;
    has description: str;
    has complexity_level: str;
    has is_completed: bool = False;
}
