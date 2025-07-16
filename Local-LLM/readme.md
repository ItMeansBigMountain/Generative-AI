# O-LLAMA
- CLI tool that works a lot like docker to containerize llm models and run them on your computer locally via cli

## download ollama here 
- https://ollama.com/

### Local Model Catalog
- https://ollama.com/search
    - Model files you can import 

---
# Uncensored LLM Leaderboards

- You can check more uncensored models on these leaderboards
    - https://huggingface.co/spaces/beepbeepbruh/UGI-Leaderboard
    - https://huggingface.co/spaces/DontPlanToEnd/UGI-Leaderboard

---

# PROCEDURE
`O-llama runs on localhost as an api`

- Download (pull) A model 
    - `ollama pull smollm2:135m`
        - this saves to `C:\Users\faree\.ollama\models`

- Delete a model 
    - `ollama rm smollm2:135m`

- Run a model 
    - `ollama run smollm2:135m`

- List All Downloaded Models
    - `ollama list`

---
# API Usage
- Start conversation:
    ```bash
    curl http://localhost:11434/api/chat -d '{
        "model": "smollm2:135m",
        "messages": [{"role": "user", "content": "Hello"}]
    }'
    ```

- Generate completion:
    ```bash
    curl http://localhost:11434/api/generate -d '{
        "model": "smollm2:135m",
        "prompt": "Write a hello world program"
    }'
    ```
