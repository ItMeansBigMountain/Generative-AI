import requests

class LLMInterface:
    def __init__(self, model_name="smollm2:135m"):
        self.model = model_name
        self.api_url = "http://localhost:11434"
    
    def query(self, prompt):
        try:
            response = requests.post(
                f"{self.api_url}/api/generate",
                json={"model": self.model, "prompt": prompt}
            )
            return response.json()["response"]
        except Exception as e:
            return f"Error: {str(e)}"

    def chat(self, messages):
        try:
            response = requests.post(
                f"{self.api_url}/api/chat",
                json={"model": self.model, "messages": messages}
            )
            return response.json()["message"]["content"]
        except Exception as e:
            return f"Error: {str(e)}"
    
    def set_model(self, model_name):
        self.model = model_name
        return f"Model changed to {model_name}"
