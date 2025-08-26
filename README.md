# MLX Fine-Tuning Toolkit

[![macOS](https://img.shields.io/badge/macOS-Apple%20Silicon-blue)](https://apple.com/mac)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://python.org)
[![MLX](https://img.shields.io/badge/MLX-Apple%20Silicon-green)](https://github.com/ml-explore/mlx)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

A complete toolkit for fine-tuning Large Language Models using Apple's MLX framework on macOS.

## Features

### 🚀 **One-Line Installation**
```bash
curl -sSL https://install.mlx-finetuning-toolkit.com | bash
```

### ⚡ **Apple Silicon Optimized**
- Native MLX framework integration
- Metal Performance Shaders acceleration
- Memory-efficient training with gradient checkpointing
- Automatic hardware detection and optimization

### 🎯 **User-Friendly Experience**
- Modern CLI with rich progress bars and status
- Desktop GUI application for visual training
- Comprehensive model management and downloading
- Real-time training monitoring and logging

### 🛡️ **Production Ready**
- Comprehensive testing framework
- Configuration validation and error handling
- Automated CI/CD pipeline
- Professional documentation

## Quick Start

### Prerequisites
- **macOS 12.0+** (Monterey or later)
- **Apple Silicon Mac** (M1/M2/M3/M4) recommended
- **Python 3.9+** or later
- **Storage Space**: 2-15GB depending on model size (see table below)
- **Memory**: 8GB RAM minimum (16GB+ recommended for larger models)

### ⚠️ Environment Setup (Important!)
If you're using Anaconda/conda and see pydantic import errors:
```bash
# Deactivate conda to avoid conflicts
conda deactivate

# Use system Python for clean installation
/usr/bin/python3 -m venv mlx-finetune-env
source mlx-finetune-env/bin/activate
```
See [ENVIRONMENT_SETUP.md](ENVIRONMENT_SETUP.md) for detailed troubleshooting.

### Installation

**Option 1: One-Line Install (Recommended)**
```bash
curl -sSL https://install.mlx-finetuning-toolkit.com | bash
```

**Option 2: Manual Install**
```bash
git clone https://github.com/yourusername/mlx-finetuning-toolkit.git
cd mlx-finetuning-toolkit
pip install -e .
```

### Basic Usage

1. **Download a model** (starts with the fastest, smallest model):
```bash
mlx-finetune download qwen3-0.5b-mlx
# Or see all available models: mlx-finetune download --list
```

2. **Use sample data (or prepare your own)** - Ready-to-use samples included!:
```bash
# Option A: Use included sample data (15 examples)
mlx-finetune train --data sample_training_data.jsonl --validation sample_validation_data.jsonl

# Option B: Create your own JSONL file
# Format: {"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]}
```

3. **Start training** (uses the default model and sample data):
```bash
# Quick test with samples (recommended first run)
mlx-finetune train --data sample_training_data.jsonl

# With validation (tracks training progress)
mlx-finetune train --data sample_training_data.jsonl --validation sample_validation_data.jsonl
```

4. **Launch GUI (optional)**:
```bash
# Launch GUI from CLI
mlx-finetune gui

# Or run GUI directly
cd gui && python run_gui.py
```

### 📁 **File Structure After Installation**

After running the commands above, your directory will look like this:
```
mlx-finetuning-toolkit/
├── models/                         # Downloaded models stored here
│   └── qwen3-0.5b-mlx/            # Your downloaded model (500MB)
├── outputs/                        # Training outputs (adapters, logs)
│   └── run_20240826_120000/       # Individual training session
├── sample_training_data.jsonl      # ✨ Ready-to-use training examples (15 samples)
├── sample_validation_data.jsonl    # ✨ Ready-to-use validation examples (5 samples)
├── GETTING_STARTED.md              # 5-minute quick start guide
└── ... (toolkit files)
```

**Model Storage:**
- Models are downloaded to `./models/` directory by default
- You can specify custom location with `--dir` flag
- Models are reused across training sessions
- No need to re-download unless you want different models

**Training Outputs:**
- Fine-tuned adapters saved to `./outputs/`
- Logs and checkpoints included
- Each training run gets its own subdirectory

## Documentation

- [📖 Installation Guide](docs/INSTALLATION.md)
- [🚀 Quick Start Guide](docs/QUICKSTART.md)
- [⚙️ Configuration Reference](docs/CONFIGURATION.md)
- [🏗️ Architecture Overview](docs/ARCHITECTURE.md)
- [❓ FAQ & Troubleshooting](docs/FAQ.md)

## Supported Models

| Model | Size | Training Speed | Description |
|-------|------|---------------|-------------|
| **qwen3-0.5b-mlx** ⭐ | 500MB | Ultra-fast | **Default** - Perfect for getting started, rapid prototyping |
| qwen2.5-1.5b-instruct | 900MB | Very fast | Small model for testing and experimentation |
| qwen2.5-3b-instruct | 1.9GB | Fast | Balanced model for most production use cases |
| qwen2.5-7b-instruct | 4.5GB | Moderate | High-quality results, requires more time/memory |
| llama-3.2-3b-instruct | 1.8GB | Fast | Compact Llama model alternative |
| llama-3.1-8b-instruct | 4.9GB | Slow | Good performance alternative to Qwen |
| mistral-7b-instruct | 4.1GB | Moderate | European open source model |

### 💡 **Choosing the Right Model:**
- **New users**: Start with `qwen3-0.5b-mlx` (default)
- **Production**: Use `qwen2.5-3b-instruct` or larger
- **Memory-constrained**: Stick with models ≤1.5B parameters
- **High quality**: Use 7B+ models for best results

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [MLX](https://github.com/ml-explore/mlx) - Apple's machine learning framework
- [Hugging Face](https://huggingface.co) - Model hub and transformers library
- The open source machine learning community

---

Made with ❤️ for the Apple Silicon ML community