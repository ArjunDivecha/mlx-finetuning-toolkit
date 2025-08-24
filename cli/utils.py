"""
MLX Fine-Tuning Toolkit - Utility Functions

Shared utilities for system checking and hardware detection.
"""

import platform
import subprocess
import logging
from typing import Tuple, List, Dict, Any

logger = logging.getLogger(__name__)

def check_system_requirements() -> Tuple[bool, List[str]]:
    """
    Check if system meets minimum requirements for MLX fine-tuning.
    
    Returns:
        Tuple of (requirements_met: bool, issues: List[str])
    """
    issues = []
    
    # Check operating system
    if platform.system() != "Darwin":
        issues.append("MLX requires macOS (Darwin)")
    
    # Check Python version
    python_version = platform.python_version_tuple()
    major, minor = int(python_version[0]), int(python_version[1])
    if major < 3 or (major == 3 and minor < 9):
        issues.append("Python 3.9+ required")
    
    # Check for required packages
    required_packages = ["mlx", "transformers", "click", "rich", "yaml"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            issues.append(f"Missing required package: {package}")
    
    # Check for Apple Silicon (recommended)
    try:
        result = subprocess.run(
            ["sysctl", "-n", "hw.optional.arm64"], 
            capture_output=True, text=True, check=False
        )
        if result.returncode != 0 or result.stdout.strip() != "1":
            issues.append("Apple Silicon recommended for optimal performance")
    except Exception:
        issues.append("Could not detect processor type")
    
    return len(issues) == 0, issues

def get_hardware_info() -> Dict[str, Any]:
    """
    Get detailed hardware information for optimization.
    
    Returns:
        Dictionary with hardware details
    """
    info = {}
    
    try:
        # Basic system info
        info["platform"] = platform.system()
        info["python_version"] = platform.python_version()
        
        # macOS specific info
        if platform.system() == "Darwin":
            # Apple Silicon check
            result = subprocess.run(
                ["sysctl", "-n", "hw.optional.arm64"], 
                capture_output=True, text=True, check=False
            )
            info["apple_silicon"] = result.returncode == 0 and result.stdout.strip() == "1"
            
            # Memory info
            result = subprocess.run(
                ["sysctl", "-n", "hw.memsize"], 
                capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                memory_bytes = int(result.stdout.strip())
                info["memory_gb"] = memory_bytes // (1024**3)
            
            # CPU info
            result = subprocess.run(
                ["sysctl", "-n", "machdep.cpu.brand_string"], 
                capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                info["cpu"] = result.stdout.strip()
    
    except Exception as e:
        logger.warning(f"Could not detect full hardware info: {e}")
    
    return info