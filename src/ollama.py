from langchain.llms import BaseLLM
from langchain.schema import LLMResult, Generation
from pydantic import Field
import requests


class OllamaLLM(BaseLLM):
    model_url: str = Field(..., description="The URL of the Ollama")

    def _call(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "llama2",  
            "messages": [{"role": "user", "content": prompt}]
        }

        response = requests.post(self.model_url, json=data, headers=headers)

        if response.status_code == 200:
            response_content = response.json()["choices"][0]["message"]["content"]
            return response_content.strip()
        else:
            return f"Error: {response.status_code} - {response.text}"

    def _generate(self, prompts: list[str], stop: list[str] = None) -> LLMResult:
        # For simplicity, handle only the first prompt
        prompt = prompts[0]
        response_text = self._call(prompt)

        return LLMResult(
            generations=[[Generation(text=response_text)]],
            llm_output=None
        )

    @property
    def _llm_type(self) -> str:
        return "ollama"  

    @property
    def _identifying_params(self) -> dict:
        return {"model_url": self.model_url}