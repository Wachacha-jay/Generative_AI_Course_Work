"""Configuration and constants for LLM Visualization"""

import:py streamlit as st;
import:py plotly.graph_objects as go;
import:py numpy as np;

glob MODEL_CONFIGS = {
    "GPT-2 (small)": {
        "layers": 12,
        "heads": 12,
        "embedding_dim": 768,
        "hidden_dim": 3072,
        "params": "124M",
        "color": "#4A90E2",
        "vocab_size": 50257
    },
    "nano-gpt": {
        "layers": 6,
        "heads": 6,
        "embedding_dim": 384,
        "hidden_dim": 1536,
        "params": "10M",
        "color": "#50E3C2",
        "vocab_size": 50257
    },
    "GPT-2 (XL)": {
        "layers": 48,
        "heads": 25,
        "embedding_dim": 1600,
        "hidden_dim": 6400,
        "params": "1.5B",
        "color": "#F5A623",
        "vocab_size": 50257
    },
    "GPT-3": {
        "layers": 96,
        "heads": 96,
        "embedding_dim": 12288,
        "hidden_dim": 49152,
        "params": "175B",
        "color": "#BD10E0",
        "vocab_size": 50257
    },
    "BERT": {
        "layers": 24,
        "heads": 16,
        "embedding_dim": 1024,
        "hidden_dim": 4096,
        "params": "340M",
        "color": "#E74C3C",
        "vocab_size": 30522
    }
};

glob STAGE_INFO = {
    "Introduction": {
        "desc": "Learn about transformer architectures and how LLMs process text.",
        "key_concepts": ["Transformers", "Self-Attention", "Neural Networks"],
        "difficulty": "Beginner"
    },
    "Tokenization": {
        "desc": "Break text into subword tokens using BPE or WordPiece encoding.",
        "key_concepts": ["BPE", "Subwords", "Vocabulary"],
        "difficulty": "Beginner"
    },
    "Embedding": {
        "desc": "Convert tokens into continuous vector representations.",
        "key_concepts": ["Embeddings", "Vectors", "Dimensions"],
        "difficulty": "Beginner"
    },
    "Positional Encoding": {
        "desc": "Add position information to embeddings since transformers have no inherent sequence order.",
        "key_concepts": ["Sinusoidal", "Learned Positions", "Sequence Order"],
        "difficulty": "Intermediate"
    },
    "Layer Norm": {
        "desc": "Normalize activations to stabilize training and improve convergence.",
        "key_concepts": ["Normalization", "Mean", "Variance"],
        "difficulty": "Intermediate"
    },
    "Self Attention": {
        "desc": "Learn how tokens attend to each other using Query, Key, Value matrices.",
        "key_concepts": ["Q-K-V", "Attention Scores", "Weighted Sum"],
        "difficulty": "Advanced"
    },
    "Multi-Head Attention": {
        "desc": "Run multiple attention mechanisms in parallel to capture different relationships.",
        "key_concepts": ["Parallel Heads", "Concatenation", "Projections"],
        "difficulty": "Advanced"
    },
    "Projection": {
        "desc": "Project attention outputs back to the embedding space.",
        "key_concepts": ["Linear Transformation", "Matrix Multiplication"],
        "difficulty": "Intermediate"
    },
    "MLP": {
        "desc": "Feed-forward networks process each position independently.",
        "key_concepts": ["FFN", "GELU", "Hidden Layers"],
        "difficulty": "Intermediate"
    },
    "Residual Connection": {
        "desc": "Add skip connections to prevent vanishing gradients in deep networks.",
        "key_concepts": ["Skip Connection", "Gradient Flow", "Deep Networks"],
        "difficulty": "Intermediate"
    },
    "Transformer Block": {
        "desc": "Combine attention, MLP, normalization, and residuals into a single block.",
        "key_concepts": ["Block Structure", "Layer Composition"],
        "difficulty": "Advanced"
    },
    "Decoder Stack": {
        "desc": "Stack multiple transformer blocks to create the full model.",
        "key_concepts": ["Layer Stacking", "Deep Architecture"],
        "difficulty": "Advanced"
    },
    "Output Layer": {
        "desc": "Convert final hidden states to vocabulary logits.",
        "key_concepts": ["Linear Layer", "Logits", "Vocabulary"],
        "difficulty": "Intermediate"
    },
    "Softmax": {
        "desc": "Convert logits to probability distributions over the vocabulary.",
        "key_concepts": ["Probabilities", "Temperature", "Sampling"],
        "difficulty": "Intermediate"
    },
    "Prediction": {
        "desc": "Generate next token predictions and explore sampling strategies.",
        "key_concepts": ["Top-k", "Top-p", "Greedy Decoding"],
        "difficulty": "Advanced"
    }
};

glob COLOR_PALETTE = {
    "attention": "#4A90E2",
    "ffn": "#50E3C2",
    "embedding": "#F5A623",
    "output": "#BD10E0",
    "residual": "#E74C3C",
    "norm": "#9B59B6",
    "token": "#1ABC9C"
};
