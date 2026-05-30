# Free LLM Auto-Installer for Windows

Automatically download and install all major free open-source LLMs on your Windows machine with a single command.

## 📋 What Gets Installed

This repo provides automated setup for the following free LLMs:

- **Llama 3** (8B) - Best all-round performance
- **Mistral 7B** - Fast and efficient
- **Phi-3 Mini** - Lightweight, runs on CPU
- **Gemma 7B** - Google's open model
- **Neural Chat** - Optimized for conversations

## 🚀 Quick Start (Windows)

### Option 1: Automatic Installation (Recommended)
```bash
# Run the PowerShell script
powershell -ExecutionPolicy Bypass -File install-llms.ps1
```

### Option 2: Manual Installation with Ollama
```bash
# Install Ollama from https://ollama.com
ollama pull llama2
ollama pull mistral
ollama run llama2
```

### Option 3: Using Python Script
```bash
# Install dependencies
pip install -r requirements.txt

# Run the auto-installer
python install_llms.py
```

## 📁 Directory Structure

```
ansaarventures/
├── install-llms.ps1          # PowerShell automation script
├── install_llms.py           # Python installation script
├── requirements.txt          # Python dependencies
├── config.yaml               # Configuration for model storage
├── README.md                 # This file
└── models/                   # Default storage location for downloaded models
```

## 💾 Storage Locations

By default, models are stored in:
- **Ollama:** `C:\Users\[YourUsername]\.ollama\models`
- **Python:** `./models/` (current directory)
- **Custom:** Edit `config.yaml` to specify a different path

## 🎯 Hardware Requirements

| Model Size | GPU | CPU | Storage |
|-----------|-----|-----|---------|
| 3-7B      | Optional | ✅ | 5-20GB |
| 7-14B     | Recommended | Possible | 15-50GB |
| 70B       | Required (strong) | ❌ | 150GB+ |

## ⚙️ Configuration

Edit `config.yaml` to customize:
- Model storage location
- Which models to install
- Download concurrency
- Ollama vs Python preference

## 🔧 Troubleshooting

### Models won't download
- Check internet connection
- Verify disk space (at least 150GB recommended)
- Try downloading one model manually: `ollama pull mistral`

### Ollama not found
- Install from: https://ollama.com/download/windows
- Restart PowerShell after installation

### Out of memory errors
- Close other applications
- Use smaller models (3B-7B instead of 70B)
- Enable GPU acceleration if available

## 📖 Using Your Installed Models

### With Ollama (Easiest)
```bash
ollama run llama2
ollama run mistral
ollama serve  # Starts API on localhost:11434
```

### With Python
```python
from ollama import Client
client = Client(host='http://localhost:11434')
response = client.generate(model='llama2', prompt='Hello!')
print(response['response'])
```

### Web Interface
After running `ollama serve`, visit: http://localhost:11434

## 📚 Resources

- **Ollama Docs:** https://ollama.com
- **Hugging Face Models:** https://huggingface.co
- **LM Studio GUI:** https://lmstudio.ai

## 💡 Tips

- Start with smaller models (Phi-3, Mistral 7B) for testing
- Use Ollama for simplicity, Python for customization
- Models are cached after first download
- You can run multiple models simultaneously with enough RAM

## 📄 License

MIT License - Free to use and modify

## 🤝 Contributing

Found a bug or want to add more models? Feel free to contribute!

---

**Happy LLM-ing! 🎉**
