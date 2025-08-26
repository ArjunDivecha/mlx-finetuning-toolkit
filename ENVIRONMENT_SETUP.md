# Environment Setup Guide

## Issue: Anaconda Environment Conflicts

If you're seeing this error:
```
Error while loading conda entry point: anaconda-cloud-auth (cannot import name 'AliasGenerator' from 'pydantic')
```

This is a known conflict between Anaconda's conda environment and the required pydantic versions.

## Solution: Use Isolated Python Environment

### Option 1: Use System Python (Recommended)
```bash
# Deactivate conda
conda deactivate

# Use system Python to create isolated environment
/usr/bin/python3 -m venv mlx-finetune-env
source mlx-finetune-env/bin/activate

# Install the toolkit
pip install -e .

# Test CLI
mlx-finetune --version
```

### Option 2: Create Clean Conda Environment
```bash
# Create new conda environment with clean Python
conda create -n mlx-finetune python=3.11 -y
conda activate mlx-finetune

# Install the toolkit
pip install -e .

# Test CLI
mlx-finetune --version
```

### Option 3: Fix Current Environment (Advanced)
```bash
# Force reinstall pydantic in current environment
pip install --force-reinstall pydantic>=2.8.0

# If that doesn't work, uninstall and reinstall
pip uninstall pydantic -y
pip install pydantic>=2.8.0
```

## Environment Variables
Add to your shell profile (~/.zshrc or ~/.bash_profile):
```bash
# Disable conda auto-activation if needed
export CONDA_AUTO_ACTIVATE_BASE=false

# Use system Python for MLX tools
alias mlx-python='/usr/bin/python3'
```

## Verification
After setup, verify everything works:
```bash
# Test CLI
mlx-finetune doctor

# Test model download
mlx-finetune download qwen3-0.5b-mlx

# Test training (dry run)
mlx-finetune train --data sample_training_data.jsonl --dry-run
```