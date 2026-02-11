
import logging
import asyncio
from typing import Optional, Dict, Any, List
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class LLMProvider(ABC):
    """Abstract Base Class for LLM Providers."""
    @abstractmethod
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        pass

class MockLLMProvider(LLMProvider):
    """Mock Provider for Testing (No API Costs)."""
    def __init__(self, predefined_responses: Optional[Dict[str, str]] = None):
        self.responses = predefined_responses or {}
        
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        logger.info(f"MOCK LLM Request: {prompt[:50]}...")
        # Return specific mock if prompt contains keyword, else default
        for key, val in self.responses.items():
            if key in prompt:
                return val
        return "I am a Mock LLM. I have received your request."

import google.generativeai as genai

class GeminiLLMProvider(LLMProvider):
    """Real implementation using Google Generative AI (Gemini)."""
    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-001"):
        if not api_key:
            raise ValueError("Gemini API Key is required.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
    async def generate(self, prompt: str, system_prompt: Optional[str] = None) -> str:
        # Gemini Python SDK handles async natively via generate_content_async since v0.3.0
        # Incorporate system prompt if supported or prepend it
        full_prompt = f"System: {system_prompt}\nUser: {prompt}" if system_prompt else prompt
        
        try:
            response = await self.model.generate_content_async(full_prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            raise RuntimeError(f"Gemini failed: {e}")

class LLMClient:
    """
    UMP-70-01: The Synapse.
    Gateway to the AI Mind.
    """
    def __init__(self, provider: LLMProvider):
        self.provider = provider
    
    async def think(self, prompt: str, system_context: str = "") -> str:
        """
        Sends a thought request to the provider.
        """
        try:
            return await self.provider.generate(prompt, system_context)
        except Exception as e:
            logger.error(f"Synapse Failure: {e}")
            raise RuntimeError(f"Mind failed to think: {e}")
