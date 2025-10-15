"""Configuration and constants for LLM Visualization"""

import streamlit as st;
import numpy as np;


glob MODEL_CONFIGS: dict = {
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

glob STAGES: list = [
    "Introduction",
    "Tokenization",
    "Embedding",
    "Positional Encoding",
    "Layer Norm",
    "Self Attention",
    "Multi-Head Attention",
    "Projection",
    "MLP",
    "Residual Connection",
    "Transformer Block",
    "Decoder Stack",
    "Output Layer",
    "Softmax",
    "Prediction"
];

glob STAGE_INFO: dict = {
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
    "Self Attention": {
        "desc": "Learn how tokens attend to each other using Query, Key, Value matrices.",
        "key_concepts": ["Q-K-V", "Attention Scores", "Weighted Sum"],
        "difficulty": "Advanced"
    },
    "MLP": {
        "desc": "Feed-forward networks process each position independently.",
        "key_concepts": ["FFN", "GELU", "Hidden Layers"],
        "difficulty": "Intermediate"
    },
    "Prediction": {
        "desc": "Generate next token predictions and explore sampling strategies.",
        "key_concepts": ["Top-k", "Top-p", "Greedy Decoding"],
        "difficulty": "Advanced"
    }
};

glob COLOR_PALETTE: dict = {
    "attention": "#4A90E2",
    "ffn": "#50E3C2",
    "embedding": "#F5A623",
    "output": "#BD10E0",
    "residual": "#E74C3C",
    "norm": "#9B59B6",
    "token": "#1ABC9C"
};
