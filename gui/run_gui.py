#!/usr/bin/env python3
"""
MLX Fine-Tuning GUI Launcher
Starts both backend and frontend, then launches the Electron GUI.
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path

def check_dependencies():
    """Check if all dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    # Run the dependency checker
    try:
        result = subprocess.run([sys.executable, "check_deps.py"], 
                              cwd=Path(__file__).parent,
                              capture_output=True, 
                              text=True)
        print(result.stdout)
        if result.returncode != 0:
            print(f"❌ Dependency check failed: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"❌ Error checking dependencies: {e}")
        return False

def start_backend():
    """Start the FastAPI backend server."""
    print("🚀 Starting backend server...")
    backend_dir = Path(__file__).parent / "backend"
    
    try:
        # Start backend server
        backend_process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], cwd=backend_dir)
        
        # Give it time to start
        time.sleep(3)
        
        # Check if it's still running
        if backend_process.poll() is None:
            print("✅ Backend server started successfully")
            return backend_process
        else:
            print("❌ Backend server failed to start")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def build_electron():
    """Build the Electron main process."""
    print("🔨 Building Electron main process...")
    gui_dir = Path(__file__).parent
    
    try:
        result = subprocess.run(["npm", "run", "build:main"], 
                              cwd=gui_dir,
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print("✅ Electron main process built successfully")
            return True
        else:
            print(f"❌ Electron build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error building Electron: {e}")
        return False

def start_electron():
    """Start the Electron GUI."""
    print("🖥️  Starting Electron GUI...")
    gui_dir = Path(__file__).parent
    
    try:
        # Start Electron
        electron_process = subprocess.Popen(["npm", "start"], cwd=gui_dir)
        return electron_process
    except Exception as e:
        print(f"❌ Error starting Electron: {e}")
        return None

def cleanup_processes(backend_process, electron_process):
    """Clean up background processes."""
    print("\n🧹 Cleaning up processes...")
    
    if electron_process and electron_process.poll() is None:
        electron_process.terminate()
        try:
            electron_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            electron_process.kill()
    
    if backend_process and backend_process.poll() is None:
        backend_process.terminate()
        try:
            backend_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            backend_process.kill()

def main():
    """Main launcher function."""
    print("🚀 MLX Fine-Tuning GUI Launcher")
    print("=" * 40)
    
    backend_process = None
    electron_process = None
    
    def signal_handler(sig, frame):
        cleanup_processes(backend_process, electron_process)
        sys.exit(0)
    
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Check dependencies
        if not check_dependencies():
            print("❌ Dependencies not ready. Please fix the issues above.")
            return 1
        
        # Start backend
        backend_process = start_backend()
        if not backend_process:
            print("❌ Could not start backend server")
            return 1
        
        # Build Electron
        if not build_electron():
            print("❌ Could not build Electron main process")
            cleanup_processes(backend_process, None)
            return 1
        
        # Start Electron GUI
        electron_process = start_electron()
        if not electron_process:
            print("❌ Could not start Electron GUI")
            cleanup_processes(backend_process, None)
            return 1
        
        print("✅ GUI launched successfully!")
        print("🌐 Backend running at: http://localhost:8000")
        print("🖥️  GUI running in Electron window")
        print("\nPress Ctrl+C to stop all processes")
        
        # Wait for Electron to finish
        electron_process.wait()
        
    except KeyboardInterrupt:
        print("\n⏹️  Stopping GUI...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return 1
    finally:
        cleanup_processes(backend_process, electron_process)
    
    print("👋 GUI stopped successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main())