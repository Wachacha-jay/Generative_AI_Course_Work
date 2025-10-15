"""Walker definitions for traversing and animating the architecture"""

walker ArchitectureTraverser {
    has visited_layers: list = [];
    has animation_frames: list = [];

    can traverse_forward with Model entry {
        layers = [];
        config = here.config;
        for i in range(config["layers"]) {
            attn_layer =
                spawn Layer(
                    layer_num=i,
                    layer_type="attention",
                    input_dim=config["embedding_dim"],
                    output_dim=config["embedding_dim"],
                    num_heads=config["heads"],
                    position=(0, 0, i * 2),
                    is_active=False
                );
            layers.append(attn_layer);
            ffn_layer =
                spawn Layer(
                    layer_num=i,
                    layer_type="ffn",
                    input_dim=config["embedding_dim"],
                    output_dim=config["embedding_dim"],
                    num_heads=0,
                    position=(5, 0, i * 2 + 0.5),
                    is_active=False
                );
            layers.append(ffn_layer);
        }
        return layers;
    }

    can animate_layer with Layer entry {
        here.is_active = True;
        self.visited_layers.append(here.layer_num);
        frame_data = {
            "layer": here.layer_num,
            "type": here.layer_type,
            "position": here.position
        };
        self.animation_frames.append(frame_data);
        here.is_active = False;
    }
}


walker TokenFlowWalker {
    has tokens: list = [];
    has flow_path: list = [];

    can tokenize_input with Model entry {
        ::py::
        import numpy as np
        words = here.input_text.split()
        for i, word in enumerate(words):
            token = spawn Token(
                text=word,
                token_id=1000 + i,
                embedding=[float(np.random.randn()) for _ in range(8)],
                position=i
            )
            self.tokens.append(token)
        ::py::

        return self.tokens;
    }

    can flow_through with Layer entry {
        for token in self.tokens {
            self.flow_path.append({
                "token": token.text,
                "layer": here.layer_num,
                "layer_type": here.layer_type
            });
        }
    }
}


walker AttentionVisualizer {
    has attention_matrices: list = [];

    can compute_attention with AttentionHead entry {
        ::py::
        import numpy as np
        seq_len = 5
        attention_pattern = np.random.rand(seq_len, seq_len)
        
        # Apply causal mask
        for i in range(seq_len):
            for j in range(seq_len):
                if j > i:
                    attention_pattern[i][j] = 0
        
        # Normalize
        row_sums = attention_pattern.sum(axis=1, keepdims=True)
        attention_pattern = attention_pattern / row_sums
        
        here.attention_scores = attention_pattern.tolist()
        self.attention_matrices.append({
            "head": here.head_num,
            "layer": here.parent_layer,
            "matrix": attention_pattern.tolist()
        })
        ::py::

    }
}


walker StageNavigator {
    has current_index: int = 0;
    has visited_stages: list = [];

    can next_stage with Model entry {
        ::py::
        from config import STAGES
        if self.current_index < len(STAGES) - 1:
            self.current_index += 1
            here.current_stage = STAGES[self.current_index]
            self.visited_stages.append(here.current_stage)
        ::py::

        return here.current_stage;
    }

    can prev_stage with Model entry {
        ::py::
        from config import STAGES
        if self.current_index > 0:
            self.current_index -= 1
            here.current_stage = STAGES[self.current_index]
        ::py::

        return here.current_stage;
    }

    can get_progress with Model entry {
        ::py::
        from config import STAGES
        progress = (self.current_index + 1, len(STAGES))
        ::py::

        return progress;
    }
}
