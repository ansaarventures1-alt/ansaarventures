# Advanced Usage Guide

Professional workflows and custom configurations for LLMs

## 🔧 API Server Setup

### Start Ollama Server

```bash
ollama serve
# Server starts on http://localhost:11434
```

### Using the REST API

#### Generate Text

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "llama2",
  "prompt": "Why is the sky blue?",
  "stream": false
}'
```

#### Streaming Response

```bash
curl http://localhost:11434/api/generate -d '{
  "model": "mistral",
  "prompt": "Tell me a story",
  "stream": true
}'
```

---

## 🐍 Python Integration

### Using Requests Library

```python
import requests
import json

def ask_llm(model: str, prompt: str) -> str:
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={
            'model': model,
            'prompt': prompt,
            'stream': False
        }
    )
    return json.loads(response.text)['response']

# Usage
answer = ask_llm('llama2', 'What is Python?')
print(answer)
```

### Using Ollama Library

```python
from ollama import Client

client = Client(host='http://localhost:11434')

# Simple generation
response = client.generate(
    model='mistral',
    prompt='Explain quantum computing'
)
print(response['response'])

# With parameters
response = client.generate(
    model='llama2',
    prompt='Write a poem',
    temperature=0.7,
    num_ctx=2048,
)
print(response['response'])
```

### Streaming Responses

```python
from ollama import Client

client = Client(host='http://localhost:11434')

stream = client.generate(
    model='neural-chat',
    prompt='Tell me a long story',
    stream=True
)

for chunk in stream:
    print(chunk['response'], end='', flush=True)
```

---

## 📊 Batch Processing

### Process Multiple Prompts

```python
import requests
import json
from concurrent.futures import ThreadPoolExecutor

def query_model(model: str, prompt: str) -> str:
    response = requests.post(
        'http://localhost:11434/api/generate',
        json={'model': model, 'prompt': prompt, 'stream': False}
    )
    return json.loads(response.text)['response']

# Batch prompts
prompts = [
    "What is AI?",
    "Explain machine learning",
    "How do neural networks work?"
]

# Process in parallel
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(
        lambda p: query_model('mistral', p),
        prompts
    ))

for prompt, result in zip(prompts, results):
    print(f"Q: {prompt}")
    print(f"A: {result}\n")
```

---

## 🎯 Model Parameters

Control generation behavior with these parameters:

```python
from ollama import Client

client = Client()

response = client.generate(
    model='llama2',
    prompt='Your prompt here',
    
    # Generation parameters
    temperature=0.7,      # 0.0 = deterministic, 1.0 = creative
    top_k=40,            # Top K tokens to consider
    top_p=0.9,           # Nucleus sampling
    num_predict=100,     # Max tokens to generate
    num_ctx=2048,        # Context window size
    
    # Advanced parameters
    repeat_last_n=64,    # Tokens to consider for repeat penalty
    repeat_penalty=1.1,  # Penalize repetition
    presence_penalty=0,  # Penalize new tokens
    frequency_penalty=0, # Penalize frequent tokens
)
```

---

## 🏗️ Multi-Model Setup

### Query Different Models

```python
from ollama import Client

client = Client()

models = {
    'fast': 'mistral',      # Fast responses
    'accurate': 'llama2',   # Accurate but slower
    'light': 'phi',         # Runs on CPU
}

prompt = "What is the capital of France?"

for label, model in models.items():
    response = client.generate(
        model=model,
        prompt=prompt,
        stream=False
    )
    print(f"{label.upper()} ({model}):")
    print(response['response'])
    print()
```

---

## 💾 Custom Model Creation

### Create Custom Model from Base

```bash
# Create a Modelfile
cat > Modelfile << 'EOF'
FROM llama2
PARAMETER temperature 0.7
PARAMETER top_k 40
PARAMETER top_p 0.9

# Custom system prompt
SYSTEM """You are an expert Python programmer. 
Provide clear, well-documented code examples."""
EOF

# Create the model
ollama create my-python-expert -f Modelfile

# Use your custom model
ollama run my-python-expert
```

### Custom Python Tutor

```bash
cat > Modelfile << 'EOF'
FROM mistral
PARAMETER temperature 0.5
SYSTEM """You are an expert Python tutor with 20 years of experience.
Explain concepts clearly with examples. Be patient and thorough."""
EOF

ollama create python-tutor -f Modelfile
ollama run python-tutor
```

---

## 🔍 Embeddings (Advanced)

Generate embeddings for semantic search:

```python
import requests
import json

def get_embedding(model: str, text: str) -> list:
    response = requests.post(
        'http://localhost:11434/api/embeddings',
        json={'model': model, 'prompt': text}
    )
    return json.loads(response.text)['embedding']

# Get embeddings
text1 = "The cat sat on the mat"
text2 = "A feline rested on a rug"

emb1 = get_embedding('mistral', text1)
emb2 = get_embedding('mistral', text2)

# Calculate similarity
import math

def cosine_similarity(a, b):
    dot = sum(x*y for x,y in zip(a,b))
    norm_a = math.sqrt(sum(x*x for x in a))
    norm_b = math.sqrt(sum(x*x for x in b))
    return dot / (norm_a * norm_b)

similarity = cosine_similarity(emb1, emb2)
print(f"Similarity: {similarity:.2f}")
```

---

## 🌐 Web Application Example

### Flask Web Interface

```python
from flask import Flask, request, jsonify
from ollama import Client

app = Flask(__name__)
client = Client(host='http://localhost:11434')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    model = data.get('model', 'mistral')
    prompt = data.get('prompt')
    
    try:
        response = client.generate(
            model=model,
            prompt=prompt,
            stream=False
        )
        return jsonify({
            'success': True,
            'response': response['response']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Test with cURL

```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2",
    "prompt": "Hello! How are you?"
  }'
```

---

## 📈 Performance Optimization

### Monitor Resource Usage

```bash
# Windows: Check GPU usage
nvidia-smi

# Windows: Check memory
Get-Process | Where-Object {$_.Name -eq 'ollama'} | Format-Table Name, @{Name='Memory (MB)'; Expression={[math]::Round($_.WorkingSet/1MB, 2)}}
```

### Reduce Memory Usage

1. **Use smaller models:**
   ```bash
   ollama run phi  # 3.8B - uses ~4GB RAM
   ```

2. **Reduce context window:**
   ```python
   client.generate(model='llama2', prompt='...', num_ctx=1024)
   ```

3. **Unload unused models:**
   ```bash
   ollama show llama2  # Check if loaded
   ```

---

## 🔐 Security Considerations

### Run with Authentication (Advanced)

```bash
# Bind to localhost only (default)
ollama serve

# Or specify custom port
OLLAMA_HOST=127.0.0.1:8080 ollama serve
```

### Secure Remote Access

Use reverse proxy (nginx):

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api/ {
        proxy_pass http://localhost:11434;
        proxy_set_header Host $host;
        proxy_buffering off;
    }
}
```

---

## 📋 Troubleshooting Advanced Issues

### GPU Not Being Used

```bash
# Windows: Check NVIDIA GPU
ollama list
# Look for GPU info in output

# Force CPU
OLLAMA_NUM_GPU=0 ollama serve
```

### Memory Leaks

```bash
# Monitor memory over time
while true; do
    Get-Process ollama | Select-Object Name, WorkingSet
    Start-Sleep -Seconds 5
}
```

### Slow Generation

```python
# Profile your generation
import time

start = time.time()
response = client.generate(model='llama2', prompt='...', stream=False)
end = time.time()

print(f"Generation time: {end - start:.2f}s")
print(f"Tokens/sec: {len(response['response'].split()) / (end - start):.2f}")
```

---

## 📚 Resources

- **Ollama API Docs:** https://github.com/ollama/ollama/blob/main/docs/api.md
- **Modelfile Spec:** https://github.com/ollama/ollama/blob/main/docs/modelfile.md
- **Model Library:** https://ollama.ai/library

---

**Happy LLM-ing! 🚀**
