# Quick Start Guide - Free LLM Auto-Installer

Get all major free LLMs installed and running in minutes!

## 🏃 Fastest Setup (Recommended for Windows)

### Option 1: PowerShell Script (Easiest)

```powershell
# Open PowerShell and run:
powershell -ExecutionPolicy Bypass -File install-llms.ps1
```

That's it! The script will:
- ✅ Install Ollama automatically
- ✅ Download 5 major LLMs (Llama 2, Mistral, Phi-3, Gemma, Neural Chat)
- ✅ Set up everything needed to run them

**Time: ~45 minutes** (depends on internet speed)

---

## Alternative Option 2: Python Script

```bash
# Install Python 3.8+ first if needed

# Install dependencies
pip install -r requirements.txt

# Run the installer
python install_llms.py
```

---

## 🎯 After Installation

### Run Your First Model

```bash
# Open Command Prompt or PowerShell and type:
ollama run llama2
```

You should see:
```
>>> 
```

Now you can chat! Try:
```
>>> What is machine learning?
```

Press `Ctrl+D` to exit.

---

### Available Models

After installation, you can run any of these:

```bash
ollama run llama2          # Llama 2 (7B)
ollama run mistral         # Mistral (7B) - faster
ollama run phi             # Phi-3 Mini (3.8B) - lightest
ollama run gemma:7b        # Gemma (7B)
ollama run neural-chat     # Neural Chat (7B) - best for chat
```

---

## 🔌 Use Models in Your Code

### Python Example

```python
import requests
import json

# Make sure Ollama is running: ollama serve

response = requests.post(
    'http://localhost:11434/api/generate',
    json={
        'model': 'llama2',
        'prompt': 'Why is the sky blue?',
        'stream': False
    }
)

result = json.loads(response.text)
print(result['response'])
```

### Using Ollama Python Library

```python
from ollama import Client

client = Client(host='http://localhost:11434')
response = client.generate(
    model='mistral',
    prompt='Tell me a joke'
)
print(response['response'])
```

---

## ⚙️ Customization

### Use Different Storage Location

Edit `config.yaml` and change:
```yaml
model_storage:
  path: "D:/My_LLM_Models"  # Change this path
```

Then run the installer.

### Download Only Specific Models

Edit `config.yaml` and set `enabled: false` for models you don't want:
```yaml
models:
  - name: "llama2"
    enabled: true     # Install this
  
  - name: "mistral"
    enabled: false    # Skip this
```

---

## 📊 Model Comparison

| Model | Size | Speed | Quality | RAM |
|-------|------|-------|---------|-----|
| **Phi-3** | 3.8B | ⚡⚡⚡ | ⭐⭐⭐ | 4GB |
| **Mistral** | 7B | ⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| **Llama 2** | 7B | ⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| **Gemma** | 7B | ⚡⚡ | ⭐⭐⭐⭐ | 8GB |
| **Neural Chat** | 7B | ⚡⚡ | ⭐⭐⭐⭐ | 8GB |

**For beginners:** Start with Phi-3 or Mistral

---

## 🐛 Troubleshooting

### "ollama: command not found"

PowerShell hasn't restarted after installation.
```bash
# Close PowerShell completely and reopen it
# Then try again
```

### Models won't download

Check your internet connection and disk space:
```bash
# View disk usage
Get-Volume C:

# Need at least 150GB free for all models
```

### Out of memory errors

Close other apps. If using Phi-3 (lightest):
```bash
ollama run phi
```

### Port 11434 already in use

Change the port in Ollama settings or stop the process using it.

---

## 📚 Learn More

- **Ollama Official Docs:** https://ollama.ai
- **Model Library:** https://ollama.ai/library
- **API Documentation:** https://github.com/ollama/ollama/blob/main/docs/api.md
- **Ollama GitHub:** https://github.com/ollama/ollama

---

## 💡 Pro Tips

1. **Run Ollama in background:**
   ```bash
   ollama serve &
   ```

2. **Use for ChatGPT-like interface:**
   - Install **Open WebUI** (web interface for Ollama)
   - Or use **LM Studio** GUI

3. **Fine-tune models** (advanced):
   - See Ollama documentation for custom model files

4. **Check what's running:**
   ```bash
   ollama list
   ```

5. **Monitor RAM usage:**
   - Open Task Manager → Performance tab
   - Watch memory while running models

---

## 🎉 You're Ready!

Your LLM setup is complete. Start building with AI! 🚀

**Questions?** Check the full [README.md](README.md) for more details.
