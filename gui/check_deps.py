#!/usr/bin/env python3
"""
GUI Dependencies Check Script
Verifies all required dependencies are properly installed before starting the GUI.
"""

import sys
import subprocess
import importlib
from pathlib import Path

def check_python_module(module_name):
    """Check if a Python module can be imported."""
    try:
        importlib.import_module(module_name)
        return True, None
    except ImportError as e:
        return False, str(e)

def check_npm_deps(directory):
    """Check if npm dependencies are installed in a directory."""
    node_modules = Path(directory) / "node_modules"
    return node_modules.exists()

def install_backend_deps():
    """Install backend Python dependencies."""
    print("📦 Installing backend Python dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"
        ], check=True, cwd=Path(__file__).parent)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install backend dependencies: {e}")
        return False

def install_frontend_deps():
    """Install frontend npm dependencies."""
    print("📦 Installing frontend npm dependencies...")
    try:
        subprocess.run(["npm", "install"], check=True, cwd=Path(__file__).parent / "frontend")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install frontend dependencies: {e}")
        return False

def build_frontend():
    """Build the frontend if not already built."""
    frontend_dist = Path(__file__).parent / "frontend" / "dist" / "index.html"
    if not frontend_dist.exists():
        print("🔨 Building frontend...")
        try:
            subprocess.run(["npm", "run", "build"], check=True, cwd=Path(__file__).parent / "frontend")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to build frontend: {e}")
            return False
    else:
        print("✅ Frontend already built")
        return True

def main():
    """Main dependency check function."""
    print("🔍 Checking MLX Fine-Tuning GUI dependencies...")
    print("=" * 50)
    
    issues = []
    
    # Check backend Python dependencies
    backend_modules = ["fastapi", "uvicorn", "websockets", "pydantic", "yaml"]
    
    for module in backend_modules:
        success, error = check_python_module(module)
        if success:
            print(f"✅ {module}")
        else:
            print(f"❌ {module}: {error}")
            issues.append(f"Backend module {module}")
    
    # Check frontend npm dependencies
    if check_npm_deps("frontend"):
        print("✅ Frontend npm dependencies")
    else:
        print("❌ Frontend npm dependencies not installed")
        issues.append("Frontend dependencies")
    
    # Check if frontend is built
    frontend_dist = Path(__file__).parent / "frontend" / "dist" / "index.html"
    if frontend_dist.exists():
        print("✅ Frontend built")
    else:
        print("❌ Frontend not built")
        issues.append("Frontend build")
    
    print("=" * 50)
    
    if issues:
        print(f"❌ Found {len(issues)} issue(s). Attempting to fix...")
        
        if "Backend module" in str(issues):
            if not install_backend_deps():
                return False
        
        if "Frontend dependencies" in str(issues):
            if not install_frontend_deps():
                return False
        
        if "Frontend build" in str(issues):
            if not build_frontend():
                return False
        
        print("✅ All issues resolved!")
    else:
        print("✅ All dependencies are properly installed!")
    
    print("\n🚀 GUI is ready to start!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)