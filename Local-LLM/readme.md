# O-LLAMA
- CLI tool that works a lot like docker to containerize llm models and run them on your computer locally via cli

## download ollama here 
- https://ollama.com/

### Local Model Catalog
- https://ollama.com/search
    - Model files you can import 

---

# PROCEDURE
`O-llama runs on localhost as an api`

- Download (pull) A model 
    - `ollama pull smollm2:135m`
        - this saves to `C:\Users\faree\.ollama\models`

- Delete a model 
    - `ollama rm smollm2:135ms`
    - `ollama rm --all`

- List All Downloaded Models
    - `ollama list`