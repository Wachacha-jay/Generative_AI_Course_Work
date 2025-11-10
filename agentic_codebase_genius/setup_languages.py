"""
Setup script for Tree-sitter language bindings.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(command, cwd=None):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None, e.stderr


def setup_tree_sitter_languages():
    """Setup Tree-sitter language bindings."""
    print("Setting up Tree-sitter language bindings...")
    
    # Create build directory
    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)
    
    # Languages to build
    languages = {
        'python': 'https://github.com/tree-sitter/tree-sitter-python.git',
        'javascript': 'https://github.com/tree-sitter/tree-sitter-javascript.git',
        'java': 'https://github.com/tree-sitter/tree-sitter-java.git',
        'cpp': 'https://github.com/tree-sitter/tree-sitter-cpp.git',
        'rust': 'https://github.com/tree-sitter/tree-sitter-rust.git',
        'go': 'https://github.com/tree-sitter/tree-sitter-go.git'
    }
    
    # Clone language repositories
    for lang, repo_url in languages.items():
        lang_dir = build_dir / f"tree-sitter-{lang}"
        
        if lang_dir.exists():
            print(f"Language {lang} already exists, skipping...")
            continue
        
        print(f"Cloning {lang} language binding...")
        stdout, stderr = run_command(f"git clone {repo_url} {lang_dir}")
        
        if stderr and "fatal" in stderr:
            print(f"Error cloning {lang}: {stderr}")
            continue
        
        print(f"Successfully cloned {lang}")
    
    # Build language bindings
    print("Building language bindings...")
    
    # Create grammars directory
    grammars_dir = build_dir / "grammars"
    grammars_dir.mkdir(exist_ok=True)
    
    for lang in languages.keys():
        lang_dir = build_dir / f"tree-sitter-{lang}"
        
        if not lang_dir.exists():
            continue
        
        print(f"Building {lang} grammar...")
        
        # Copy grammar files
        grammar_files = list(lang_dir.glob("grammar.js")) + list(lang_dir.glob("grammar.json"))
        if grammar_files:
            for grammar_file in grammar_files:
                dest_file = grammars_dir / f"{lang}.js"
                dest_file.write_text(grammar_file.read_text())
                print(f"Copied grammar for {lang}")
        else:
            print(f"No grammar file found for {lang}")
    
    print("Tree-sitter language bindings setup completed!")


def install_dependencies():
    """Install required Python dependencies."""
    print("Installing Python dependencies...")
    
    requirements = [
        "tree-sitter",
        "tree-sitter-python",
        "tree-sitter-javascript", 
        "tree-sitter-java",
        "tree-sitter-cpp",
        "tree-sitter-rust",
        "tree-sitter-go"
    ]
    
    for package in requirements:
        print(f"Installing {package}...")
        stdout, stderr = run_command(f"pip install {package}")
        
        if stderr and "error" in stderr.lower():
            print(f"Error installing {package}: {stderr}")
        else:
            print(f"Successfully installed {package}")


def main():
    """Main setup function."""
    print("🚀 Setting up Codebase Genius...")
    
    # Install dependencies
    install_dependencies()
    
    # Setup Tree-sitter languages
    setup_tree_sitter_languages()
    
    print("✅ Setup completed successfully!")
    print("\nTo run the application:")
    print("1. Streamlit UI: streamlit run frontend/app.py")
    print("2. API Server: python main.py")
    print("3. Or: uvicorn main:app --reload --port 8000")


if __name__ == "__main__":
    main()