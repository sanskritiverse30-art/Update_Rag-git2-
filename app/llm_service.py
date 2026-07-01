from app.interfaces import LLMServiceInterface


class OllamaLLMService(LLMServiceInterface):
    def __init__(self, model_name: str = "llama3.2:latest"):
        try:
            from langchain_community.llms import Ollama
            self.llm = Ollama(model=model_name)
        except Exception:
            self.llm = None

    def generate(self, prompt: str) -> str:
        if self.llm is None:
            return "LLM not connected. Run: ollama serve"

        return self.llm.invoke(prompt)


class MockLLMService(LLMServiceInterface):
    def generate(self, prompt: str) -> str:
        return "Mock answer generated for testing."