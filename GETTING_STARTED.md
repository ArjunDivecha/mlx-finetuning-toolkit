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

### 3. Use Ready-Made Sample Data (Already Included!)
No need to create files - we've included comprehensive samples:
```bash
# See what's included
ls sample_*.jsonl
# sample_training_data.jsonl    (15 diverse examples)
# sample_validation_data.jsonl  (5 validation examples)
```

### 4. Start Training (Zero Setup!)
```bash
mlx-finetune train --data sample_training_data.jsonl --validation sample_validation_data.jsonl
```
*Uses default model (qwen3-0.5b-mlx) + included sample data - training will be very fast!*

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

### Sample Data Contents
The included sample datasets contain diverse conversation examples:
- **Greetings & casual conversation**
- **Question answering** (weather, technology, life advice)
- **Creative tasks** (jokes, stories, recommendations)
- **Educational content** (explanations, tutorials, study tips)
- **Practical help** (recipes, emails, motivation)

**Data Format** (if you create your own):
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