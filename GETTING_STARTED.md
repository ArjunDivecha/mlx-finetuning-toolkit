# 🚀 Getting Started with MLX Fine-Tuning Toolkit

## ⚡ Quick Setup (5 minutes)

### 1. Clone & Install
```bash
git clone https://github.com/yourusername/mlx-finetuning-toolkit.git
cd mlx-finetuning-toolkit
pip install -e .
```

### 2. Download Your First Model (500MB)
```bash
mlx-finetune download qwen3-0.5b-mlx
```
*This downloads the fastest, smallest model perfect for getting started*

### 3. Prepare Sample Data
Create a file called `my_data.jsonl`:
```json
{"messages": [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi! How can I help you today?"}]}
{"messages": [{"role": "user", "content": "What's the weather like?"}, {"role": "assistant", "content": "I don't have access to current weather data, but I'd be happy to help with other questions!"}]}
{"messages": [{"role": "user", "content": "Tell me a joke"}, {"role": "assistant", "content": "Why did the ML model go to therapy? It had too many layers of complexity!"}]}
```

### 4. Start Training
```bash
mlx-finetune train --data my_data.jsonl
```
*Uses the default model (qwen3-0.5b-mlx) - training will be very fast!*

### 5. Launch GUI (Optional)
```bash
mlx-finetune gui
```

## 📋 What Happens After Installation

Your directory structure will look like this:
```
mlx-finetuning-toolkit/
├── 📁 models/                 # Downloaded models (auto-created)
│   └── qwen3-0.5b-mlx/        # Your 500MB model
├── 📁 outputs/                # Training results (auto-created)  
│   └── run_20240824_120000/   # Today's training session
├── 📄 my_data.jsonl           # Your training data
└── ... (toolkit files)
```

## 🎯 Available Models

| Model | Size | Speed | Best For |
|-------|------|-------|----------|
| **qwen3-0.5b-mlx** ⭐ | 500MB | Ultra-fast | Getting started, testing |
| qwen2.5-1.5b-instruct | 900MB | Very fast | Experimentation |
| qwen2.5-3b-instruct | 1.9GB | Fast | Production use |
| qwen2.5-7b-instruct | 4.5GB | Moderate | High quality results |

**View all models**: `mlx-finetune download --list`

## 💡 Tips for Success

### Start Small
- Begin with `qwen3-0.5b-mlx` (default)
- Use 10-100 training examples first
- Training takes minutes, not hours

### Data Format
Your JSONL file should contain conversations:
```json
{"messages": [
  {"role": "user", "content": "Question here"},
  {"role": "assistant", "content": "Response here"}
]}
```

### Training Tips
- **Small model**: 10-50 examples = good results
- **Larger models**: 100-1000+ examples = better results
- **Training time**: 5-30 minutes depending on data size

### System Requirements
- **macOS 12.0+** (Apple Silicon recommended)
- **8GB RAM** minimum (16GB+ for larger models)
- **2GB disk space** for default setup

## 🚨 Troubleshooting

### "Model not found"
```bash
# Download the model first
mlx-finetune download qwen3-0.5b-mlx
```

### "Permission denied"
```bash
# Make sure you're in the right directory
cd mlx-finetuning-toolkit
```

### "Out of memory"
- Use smaller model: `qwen3-0.5b-mlx`
- Reduce batch size: `--batch-size 1`
- Close other applications

### "Training too slow"
- Use the default small model
- Reduce dataset size for testing
- Upgrade to Apple Silicon Mac if possible

## 🎉 Next Steps

Once your first model is trained:

1. **Test it**: Use the GUI to chat with your fine-tuned model
2. **Scale up**: Try a larger model like `qwen2.5-3b-instruct`  
3. **Add more data**: Expand your training dataset
4. **Share**: Your trained adapters are in the `outputs/` folder

## 📚 Learn More

- [📖 Full Documentation](README.md)
- [⚙️ Advanced Configuration](docs/CONFIGURATION.md)
- [❓ FAQ](docs/FAQ.md)

---

**Happy fine-tuning!** 🎯