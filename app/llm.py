import requests

from app.prompt import SYSTEM_PROMPT


class GeminiLLM:
    def __init__(self):
        self.model_name = "mistral"
        self.ollama_url = "http://localhost:11434/api/generate"

    def generate_answer(self, question: str, context: str) -> str:
        prompt = SYSTEM_PROMPT.format(
            context=context,
            question=question
        )

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "stream": False
        }

        try:
            response = requests.post(
                self.ollama_url,
                json=payload,
                timeout=120
            )

            response.raise_for_status()
            result = response.json()

            return result.get(
                "response",
                "I could not find this information in the provided documents."
            ).strip()

        except Exception as e:
            return f"Local LLM error: {str(e)}"