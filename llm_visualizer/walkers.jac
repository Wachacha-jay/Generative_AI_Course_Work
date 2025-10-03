"""Walker definitions for traversing and animating the architecture"""

walker ArchitectureTraverser {
    has visited_layers: list = [];
    has animation_frames: list = [];
    has current_position: tuple = (0, 0, 0);
    
    can traverse_forward with Model entry {
        # Build the architecture graph
        layers = [];
        config = here.config;
        
        for i in range(config["layers"]) {
            # Create attention layer
            attn_layer = Layer(
                layer_num=i,
                layer_type="attention",
                input_dim=config["embedding_dim"],
                output_dim=config["embedding_dim"],
                num_heads=config["heads"],
                position=(0, 0, i * 2)
            );
            layers.append(attn_layer);
            
            # Create FFN layer
            ffn_layer = Layer(
                layer_num=i,
                layer_type="ffn",
                input_dim=config["embedding_dim"],
                output_dim=config["embedding_dim"],
                position=(5, 0, i * 2 + 0.5)
            );
            layers.append(ffn_layer);
        }
        
        return layers;
    }
    
    can animate_layer_activation with Layer entry {
        # Activate current layer
        here.is_active = True;
        self.visited_layers.append(here.layer_num);
        
        # Create animation frame
        frame_data = {
            "layer": here.layer_num,
            "type": here.layer_type,
            "position": here.position,
            "timestamp": len(self.animation_frames)
        };
        self.animation_frames.append(frame_data);
        
        # Deactivate after animation
        here.is_active = False;
    }
}

walker TokenFlowWalker {
    has tokens: list[Token] = [];
    has current_token_idx: int = 0;
    has flow_path: list = [];
    
    can tokenize_input with Model entry {
        words = here.input_text.split();
        for i, word in enumerate(words) {
            token = Token(
                text=word,
                token_id=1000 + i,
                embedding=[np.random.randn() for _ in range(8)],
                position=i
            );
            self.tokens.append(token);
        }
        return self.tokens;
    }
    
    can flow_through_layer with Layer entry {
        # Record token flow through this layer
        for token in self.tokens {
            self.flow_path.append({
                "token": token.text,
                "layer": here.layer_num,
                "layer_type": here.layer_type,
                "position": here.position
            });
        }
    }
}

walker AttentionVisualizer {
    has attention_matrices: list = [];
    has head_activations: list = [];
    
    can compute_attention with AttentionHead entry {
        # Simulate attention computation
        seq_len = 5;  # Example sequence length
        attention_pattern = np.random.rand(seq_len, seq_len);
        
        # Apply causal mask for GPT-style models
        for i in range(seq_len) {
            for j in range(seq_len) {
                if j > i {
                    attention_pattern[i][j] = 0;
                }
            }
        }
        
        # Normalize
        row_sums = attention_pattern.sum(axis=1, keepdims=True);
        attention_pattern = attention_pattern / row_sums;
        
        here.attention_scores = attention_pattern.tolist();
        self.attention_matrices.append({
            "head": here.head_num,
            "layer": here.parent_layer,
            "matrix": attention_pattern.tolist()
        });
    }
    
    can visualize_attention_pattern with Model entry {
        # Create attention heatmaps
        return self.attention_matrices;
    }
}

walker StageNavigator {
    has stage_sequence: list = list(STAGE_INFO.keys());
    has current_index: int = 0;
    has visited_stages: list = [];
    
    can next_stage with Model entry {
        if self.current_index < len(self.stage_sequence) - 1 {
            self.current_index += 1;
            here.current_stage = self.stage_sequence[self.current_index];
            self.visited_stages.append(here.current_stage);
        }
        return here.current_stage;
    }
    
    can prev_stage with Model entry {
        if self.current_index > 0 {
            self.current_index -= 1;
            here.current_stage = self.stage_sequence[self.current_index];
        }
        return here.current_stage;
    }
    
    can get_progress with Model entry {
        return (self.current_index + 1, len(self.stage_sequence));
    }
}
