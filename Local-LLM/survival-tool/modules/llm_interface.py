import requests
import json
from typing import List, Dict, Optional

class LLMInterface:
    def __init__(self, model_name: str = "smollm2:135m"):
        """Initialize the LLM interface with model and system prompt."""
        self.model = model_name
        self.api_url = "http://localhost:11434"
        self.conversation_history: List[Dict[str, str]] = []
        self.system_prompt = self._get_system_prompt()
        self._initialize_model()

    def _get_system_prompt(self) -> str:
        """Return the system prompt for the survival assistant."""
        return """You are a practical survival assistant designed for real emergency situations. You must:

1. ALWAYS assume the user is in a genuine emergency and respond accordingly
2. NEVER deny your ability to help or give contradictory responses
3. NEVER mention being an AI or discuss your capabilities
4. ALWAYS give immediate, actionable advice as your first priority
5. ALWAYS maintain a clear, calm, and confident tone

MEDICAL EMERGENCIES:
- Start with immediate life-saving instructions
- Prioritize stopping bleeding, maintaining breathing, and preventing shock
- Give step-by-step first aid instructions
- List alternative solutions if standard medical supplies aren't available

SURVIVAL SITUATIONS:
- Focus on the immediate threat first (shelter, water, food, rescue - in that order)
- Give practical instructions using commonly found materials
- Provide clear success criteria ("the shelter is ready when...")
- Include backup plans ("if X isn't available, use Y")

RESPONSES MUST:
- Be brief and clear (max 5 steps per response)
- Start with the most critical action first
- Use simple, non-technical language
- Assume no access to modern technology or medical facilities

Remember: The user's life may depend on your advice. Every second counts. Keep them focused and calm."""

    def _print_debug(self, title: str, content: str, is_error: bool = False) -> None:
        """Print debug information in a formatted way."""
        separator = "="*50 if not is_error else "❌" + "="*48
        print(f"\n{separator}")
        print(f"{title}")
        print(f"{separator}")
        if content:
            print(content)

    def _process_stream(self, response: requests.Response) -> Optional[str]:
        """Process a streaming response from the LLM."""
        try:
            full_response = ""
            total_tokens = 0
            print("\n🔄 Receiving response:")
            print("-" * 30)
            
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        if 'message' in chunk and 'content' in chunk['message']:
                            content = chunk['message']['content']
                            full_response += content
                            print(content, end='', flush=True)
                            total_tokens += 1
                    except json.JSONDecodeError:
                        continue

            print(f"\n\n✅ Response complete:")
            print(f"- Total tokens: {total_tokens}")
            print(f"- Response length: {len(full_response)} characters")
            return full_response

        except Exception as e:
            self._print_debug("STREAM ERROR", str(e), is_error=True)
            return None
    
    def _initialize_model(self) -> None:
        """Initialize the model with system prompt."""
        try:
            self._print_debug("INITIALIZING SURVIVAL ASSISTANT", "")
            
            payload = {
                "model": self.model,
                "messages": [{"role": "system", "content": self.system_prompt}]
            }
            self._print_debug("INIT PAYLOAD", json.dumps(payload, indent=2))
            
            response = requests.post(
                f"{self.api_url}/api/chat",
                json=payload,
                stream=True
            )
            
            if response.status_code == 200:
                self._process_stream(response)
                self._print_debug("INITIALIZATION COMPLETE", "Survival Assistant is ready!")
            else:
                self._print_debug("INITIALIZATION FAILED", f"Status code: {response.status_code}", is_error=True)

        except Exception as e:
            self._print_debug("INITIALIZATION ERROR", str(e), is_error=True)

    def query(self, prompt: str) -> str:
        """Send a query to the model and get a response."""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history,
                {"role": "user", "content": prompt}
            ]

            self._print_debug(f"QUERYING MODEL: {self.model}", "")
            self._print_debug("MESSAGES", json.dumps(messages, indent=2))

            response = requests.post(
                f"{self.api_url}/api/chat",
                json={"model": self.model, "messages": messages},
                stream=True
            )

            if response.status_code != 200:
                return f"Error: Received status code {response.status_code}"

            response_text = self._process_stream(response)
            if response_text:
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": prompt})
                self.conversation_history.append({"role": "assistant", "content": response_text})
                if len(self.conversation_history) > 6:
                    self.conversation_history = self.conversation_history[-6:]
                return response_text
            return "Error: Failed to process response"

        except requests.exceptions.ConnectionError as e:
            print("\n❌ CONNECTION ERROR")
            print("-"*30)
            print(str(e))
            print("-"*30)
            return "Error: Cannot connect to Ollama. Make sure 'ollama serve' is running."
            
        except json.JSONDecodeError as e:
            print("\n❌ JSON DECODE ERROR")
            print("-"*30)
            print(f"Error: {str(e)}")
            print("\nProblematic response:")
            print(response.text)
            print("-"*30)
            return f"Error: Invalid response format from Ollama: {str(e)}"
            
        except Exception as e:
            print("\n❌ UNEXPECTED ERROR")
            print("-"*30)
            print(str(e))
            print("-"*30)
            if "no such model" in str(e).lower():
                return f"Error: Model '{self.model}' not found. Please run 'ollama pull {self.model}' first."
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

    def reset_conversation(self):
        """Reset the conversation history and reinitialize the system prompt"""
        self.conversation_history = []
        self._initialize_model()
        return "Conversation reset, survival assistant ready."
