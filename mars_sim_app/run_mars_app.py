#!/usr/bin/env python3
"""
Mars Colony Application Launcher
Handles both JAC API server and Streamlit app startup
"""

import subprocess
import time
import sys
import os
import signal
import threading

def start_jac_server():
    """Start JAC API server in background"""
    try:
        print("🔴 Starting JAC API Server...")
        process = subprocess.Popen([
            'jac', 'serve', 'mars_api.jac', '--port', '8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server started successfully
        if process.poll() is None:
            print("✅ JAC API Server started on port 8000")
            return process
        else:
            print("❌ JAC API Server failed to start")
            return None
    except Exception as e:
        print(f"❌ Failed to start JAC server: {e}")
        return None

def start_streamlit():
    """Start Streamlit application"""
    try:
        print("🚀 Starting Streamlit Mars Colony App...")
        subprocess.run([
            'streamlit', 'run', 'mars_app.py', '--server.port', '8501'
        ])
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Mars Colony App...")
    except Exception as e:
        print(f"❌ Failed to start Streamlit: {e}")

def main():
    """Main launcher function"""
    print("🔴 Mars Colony Simulation Launcher")
    print("=" * 50)
    
    # Check if JAC is available
    try:
        result = subprocess.run(['jac', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ JAC language not found. Please install JAC first.")
            sys.exit(1)
        print(f"✅ JAC version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ JAC language not found. Please install JAC first.")
        sys.exit(1)
    
    # Check if Streamlit is available
    try:
        result = subprocess.run(['streamlit', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Streamlit not found. Please install Streamlit first.")
            sys.exit(1)
        print(f"✅ Streamlit version: {result.stdout.strip()}")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install Streamlit first.")
        sys.exit(1)
    
    print("\n🚀 Starting Mars Colony Application...")
    print("   - JAC API Server: http://localhost:8000")
    print("   - Streamlit App: http://localhost:8501")
    print("\nPress Ctrl+C to stop both services")
    print("=" * 50)
    
    # Start JAC server
    jac_process = start_jac_server()
    
    # Start Streamlit (this will block)
    try:
        start_streamlit()
    finally:
        # Cleanup
        if jac_process:
            print("🛑 Stopping JAC API Server...")
            jac_process.terminate()
            jac_process.wait()
        print("✅ Mars Colony Application stopped")

if __name__ == "__main__":
    main()