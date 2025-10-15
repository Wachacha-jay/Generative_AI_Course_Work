#!/usr/bin/env python3
"""
Simple script to run the LLM Visualizer application
This script compiles the Jaclang code and runs it with Streamlit
"""

import subprocess
import sys
import os

def main():
    # Change to the application directory
    os.chdir('/home/jay/Generative_AI_Course_Work/llm_visualizer')
    
    print("🧠 LLM Architecture Visualizer")
    print("=" * 50)
    
    # Build the Jaclang application
    print("📦 Building Jaclang application...")
    try:
        result = subprocess.run(['jac', 'build', 'main.jac'], 
                              capture_output=True, text=True, check=True)
        print("✅ Build successful!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return 1
    
    # Run the application with Streamlit
    print("🚀 Starting Streamlit application...")
    print("📱 Open your browser to http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("=" * 50)
    
    try:
        # Run the compiled Python file with Streamlit
        subprocess.run(['streamlit', 'run', 'main.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Application failed to start: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())