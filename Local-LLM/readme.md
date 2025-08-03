# O-LLAMA
- CLI tool that works a lot like docker to containerize llm models and run them on your computer locally via cli

## download ollama here 
- https://ollama.com/

## Model Resources
### Uncensored Model Leaderboards
- [UGI Leaderboard](https://huggingface.co/spaces/beepbeepbruh/UGI-Leaderboard)
- [Alternative UGI Leaderboard](https://huggingface.co/spaces/DontPlanToEnd/UGI-Leaderboard)
- [Local Model Catalog](https://ollama.com/search)

--- 

# PROCEDURE
`O-llama runs on localhost as an api`

- Download (pull) A model 
    - `ollama pull smollm2:135m`
        - this saves to `C:\Users\username\.ollama\models`

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

---

# Fine-Tuning An LLM 
> Note: Fine-tuning adapts an existing model's behavior without modifying its core understanding.
`There are different teqniques to train an LLM`

1. **LoRA (Low-Rank Adaptation)**
   - Efficient fine-tuning for large models
   - Reduces memory requirements
   - Faster training times

2. **QLoRA (Quantized LoRA)**
   - Further memory optimization
   - Maintains model quality
   - Suitable for consumer hardware

3. **FlashAttention**
   - Improves attention mechanism efficiency
   - Reduces memory usage
   - Faster training and inference

---

