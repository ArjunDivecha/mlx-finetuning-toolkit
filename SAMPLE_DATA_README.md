# Sample Dataset Documentation

## 📊 Dataset Overview

This repository includes ready-to-use sample datasets to get you started with fine-tuning immediately!

### Files Included

| File | Examples | Purpose | Content |
|------|----------|---------|---------|
| `sample_training_data.jsonl` | 15 | Training | Diverse conversation examples |
| `sample_validation_data.jsonl` | 5 | Validation | Test examples for monitoring progress |

## 🎯 Training Data Contents (15 examples)

**Conversation Types:**
- ✅ **Greetings & Social** - Natural conversation starters
- ✅ **Question & Answer** - Weather, technology, explanations
- ✅ **Creative Tasks** - Jokes, storytelling, recommendations
- ✅ **Educational** - Teaching concepts (ML, programming, quantum computing)
- ✅ **Practical Help** - Recipes, emails, study tips, motivation
- ✅ **Life Advice** - Stress management, learning languages, exercise
- ✅ **Technical Explanations** - AI, coding, complex topics made simple

**Example Topics:**
- Machine learning explanations
- Cooking recipes (chocolate chip cookies)
- Programming tutorials
- Book recommendations
- Language learning advice
- Exercise motivation
- Thank you email templates
- Study strategies

## 🔍 Validation Data Contents (5 examples)

Focused on core conversation skills:
- Greeting responses
- Technical explanations
- Quick practical help
- Study advice  
- Beginner-friendly coding explanations

## 🚀 Quick Usage

### Test Run (Recommended First Time)
```bash
# Download the default model
mlx-finetune download qwen3-0.5b-mlx

# Train with samples (very fast!)
mlx-finetune train --data sample_training_data.jsonl --validation sample_validation_data.jsonl
```

### Expected Results
With the default `qwen3-0.5b-mlx` model and sample data:
- **Training time**: 2-5 minutes
- **Memory usage**: ~2-4GB RAM
- **Storage needed**: ~500MB (model) + minimal (outputs)
- **Quality**: Good for conversational responses

## 📝 Data Format

Each line in the JSONL files contains a conversation:
```json
{
  "messages": [
    {"role": "user", "content": "User's question or request"},
    {"role": "assistant", "content": "Assistant's helpful response"}
  ]
}
```

## 🎨 Customization Tips

### Expanding the Dataset
1. **Add more examples** following the same format
2. **Focus on your domain** (e.g., customer service, education, coding)
3. **Include edge cases** and common user questions
4. **Balance conversation types** for well-rounded responses

### Creating Your Own Dataset
1. **Start small** - 10-20 high-quality examples
2. **Be consistent** - maintain the same response style
3. **Include variety** - different question types and lengths
4. **Test incrementally** - train on small batches first

### Advanced Usage
```bash
# Train on just training data (no validation)
mlx-finetune train --data sample_training_data.jsonl

# Combine with your own data
cat sample_training_data.jsonl your_data.jsonl > combined_training.jsonl
mlx-finetune train --data combined_training.jsonl
```

## ⚡ Performance Expectations

| Model Size | Sample Data | Training Time | Quality |
|------------|-------------|---------------|---------|
| qwen3-0.5b-mlx (default) | 15 examples | 2-3 minutes | Good for testing |
| qwen2.5-1.5b-instruct | 15 examples | 5-8 minutes | Better responses |
| qwen2.5-3b-instruct | 15 examples | 10-15 minutes | High quality |

## 🔧 Troubleshooting

**"Not enough data" warning:**
- Normal for small datasets
- Add more examples for better results
- Sample data is designed for quick testing

**"Training too fast" concern:**
- This is expected with small models and data
- Results are still meaningful
- Scale up model/data for production use

**Memory issues:**
- Stick with default `qwen3-0.5b-mlx` model
- Close other applications
- Reduce batch size if needed

## 📚 Next Steps

1. **Test the samples** - Run training with included data
2. **Evaluate results** - Use the GUI to chat with your fine-tuned model  
3. **Create custom data** - Add examples specific to your use case
4. **Scale up** - Try larger models with more data
5. **Deploy** - Use your fine-tuned model in applications

The sample datasets are designed to give you immediate success and a foundation for building your own fine-tuned models!