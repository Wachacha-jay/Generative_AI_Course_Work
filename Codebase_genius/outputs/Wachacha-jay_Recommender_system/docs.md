# Wachacha-jay_Recommender_system - Code Documentation

## Table of Contents

- [Project Overview](#project-overview)
- [Installation and Setup](#installation-and-setup)
- [Architecture Overview](#architecture-overview)
- [API Reference](#api-reference)
- [Usage Examples](#usage-examples)
- [Development Guide](#development-guide)

## Project Overview

**Repository:** https://github.com/Wachacha-jay/Recommender_system
**Branch:** main
**Commit:** 8bf35e4f

**Primary Language:** Python
**Detected Languages:** text, markdown, toml, python
**Total Files:** 18

## Project Description
> A comprehensive, modular framework for building and comparing recommendation algorithms from scratch to production-ready systems. --- This project implements a complete recommendation system pipeline, demonstrating mastery of: - **Classical Methods**: Popularity, Collaborative Filtering, Content-Based - **Matrix Factorization**: SVD, ALS

## Entry Points
The following files serve as entry points to the application:

- `main.py`
- `setup.py`


## Installation and Setup

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Wachacha-jay/Recommender_system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Architecture Overview

## System Architecture

The following diagram shows the high-level architecture and relationships between components:

![Architecture Diagram](architecture_diagram.png)

### Key Components

#### Functions

- **main** (`main.py`)
- **download_movielens** (`src/data_loader.py`)

#### Classs

- **DataSplitter** (`src/preprocess.py`)
- **DataPreprocessor** (`src/preprocess.py`)
- **RecommenderEvaluator** (`src/evaluation.py`)
- **MovieLensLoader** (`src/data_loader.py`)
- **ContentBasedRecommender** (`src/recommenders/content_based.py`)
- **HybridRecommender** (`src/recommenders/content_based.py`)
- **RandomRecommender** (`src/recommenders/popularity.py`)
- **PopularityRecommender** (`src/recommenders/popularity.py`)
- **TimeDecayPopularityRecommender** (`src/recommenders/popularity.py`)
- **TrendingRecommender** (`src/recommenders/popularity.py`)


## API Reference

## API Reference

### main.py

#### main

**Type:** Function
**Location:** Lines 1-1

### src/preprocess.py

#### DataSplitter

**Type:** Class
**Location:** Lines 12-12

#### DataPreprocessor

**Type:** Class
**Location:** Lines 155-155

### src/evaluation.py

#### RecommenderEvaluator

**Type:** Class
**Location:** Lines 14-14

### src/data_loader.py

#### download_movielens

**Type:** Function
**Location:** Lines 189-189

#### MovieLensLoader

**Type:** Class
**Location:** Lines 17-17

### src/recommenders/content_based.py

#### ContentBasedRecommender

**Type:** Class
**Location:** Lines 16-16

#### HybridRecommender

**Type:** Class
**Location:** Lines 212-212

### src/recommenders/popularity.py

#### RandomRecommender

**Type:** Class
**Location:** Lines 15-15

#### PopularityRecommender

**Type:** Class
**Location:** Lines 61-61

#### TimeDecayPopularityRecommender

**Type:** Class
**Location:** Lines 133-133

#### TrendingRecommender

**Type:** Class
**Location:** Lines 212-212

### src/recommenders/base.py

#### BaseRecommender

**Type:** Class
**Location:** Lines 12-12

### src/recommenders/collaborative.py

#### UserBasedCF

**Type:** Class
**Location:** Lines 17-17

#### ItemBasedCF

**Type:** Class
**Location:** Lines 146-146

#### MatrixFactorizationSVD

**Type:** Class
**Location:** Lines 275-275

#### AlternatingLeastSquares

**Type:** Class
**Location:** Lines 366-366


## Usage Examples

## Usage Examples

### Running the Application

To run the main function in `main.py`:

```bash
python main.py
```

### Code Examples

Here are some key code examples from the codebase:

#### main

```python
# Function definition in main.py
# Lines 1-1
...
```

#### download_movielens

```python
# Function definition in src/data_loader.py
# Lines 189-189
...
```


## Development Guide

## Development Guide

### Project Structure

The project follows the following structure:

```
📁 codebase_genius_Wachacha-jay_Recommender_system/
  📄 .python-version
  📄 README.md
  🐍 main.py
  📁 models/
    📄 content_based.pkl
    📄 hybrid_best.pkl
    📄 item_cf_best.pkl
    📄 popularity_weighted.pkl
    📄 svd_best.pkl
    📄 time_decay.pkl
  📁 notebooks/
    🐍 01-data_exploration.ipynb
    🐍 02_baseline_model.ipynb
    📄 03-colaborative_filtering.ipynb
    🐍 04_content_based.ipynb
  📄 pyproject.toml
  📄 requirements.txt
  🐍 setup.py
  📁 src/
    🐍 __init__.py
    🐍 data_loader.py
    🐍 evaluation.py
    🐍 preprocess.py
    📁 recommenders/
      🐍 __init__.py
      🐍 base.py
      🐍 collaborative.py
      🐍 content_based.py
      🐍 popularity.py
    🐍 utils.py
  📄 uv.lock
```

### Key Files

- **main.py** - Entry point to the application
- **setup.py** - Entry point to the application

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request


## Diagrams

### Class Relationships

![class_relationships](class_relationships.png)

### Call Graph

![call_graph](call_graph.png)
