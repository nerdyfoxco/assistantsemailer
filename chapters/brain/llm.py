from abc import ABC, abstractmethod
from typing import Optional, List
import os
from openai import OpenAI, AuthenticationError
from dotenv import load_dotenv

load_dotenv()

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, model: str = "gpt-4-turbo") -> str:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self):
        self.keys = [
            os.getenv("OPENAI_API_KEY_PRIMARY"),
            os.getenv("OPENAI_API_KEY_SECONDARY")
        ]
        self.keys = [k for k in self.keys if k] # Filter None
        
        if not self.keys:
            print("WARNING: No OpenAI Keys found in .env")

    def generate(self, system_prompt: str, user_prompt: str, model: str = "gpt-4-turbo") -> str:
        last_error = None
        for key in self.keys:
            try:
                client = OpenAI(api_key=key)
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7
                )
                return response.choices[0].message.content
            except AuthenticationError as e:
                print(f"WARN: Key failed auth: {str(e)[:50]}... Trying next.")
                last_error = e
                continue
            except Exception as e:
                raise RuntimeError(f"OpenAI Generation Failed: {e}")
        
        raise RuntimeError(f"All OpenAI Keys failed. Last error: {last_error}")

# Factory to get safe provider
def get_llm_provider() -> LLMProvider:
    if os.getenv("OPENAI_API_KEY_PRIMARY"):
        return OpenAIProvider()
    return MockLLM()

class MockLLM(LLMProvider):
    def generate(self, system_prompt: str, user_prompt: str, model: str = "mock") -> str:
        return "This is a mocked AI response for testing."
