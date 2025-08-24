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
- macOS 12.0+ (Monterey or later)
- Apple Silicon Mac (M1/M2/M3/M4) recommended
- Python 3.9 or later

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

1. **Download a model**:
```bash
mlx-finetune download qwen2.5-7b-instruct
```

2. **Prepare your data** (JSONL format):
```json
{"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi there!"}]}
```

3. **Start training**:
```bash
mlx-finetune train --model qwen2.5-7b-instruct --data my_training_data.jsonl
```

4. **Launch GUI (optional)**:
```bash
mlx-finetune gui
```

## Documentation

- [📖 Installation Guide](docs/INSTALLATION.md)
- [🚀 Quick Start Guide](docs/QUICKSTART.md)
- [⚙️ Configuration Reference](docs/CONFIGURATION.md)
- [🏗️ Architecture Overview](docs/ARCHITECTURE.md)
- [❓ FAQ & Troubleshooting](docs/FAQ.md)

## Supported Models

| Model | Size | Description |
|-------|------|-------------|
| qwen2.5-7b-instruct | 4.5GB | Recommended for most use cases |
| qwen2.5-3b-instruct | 1.9GB | Smaller model for faster training |
| llama-3.1-8b-instruct | 4.9GB | Good performance alternative |
| mistral-7b-instruct | 4.1GB | European open source model |

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