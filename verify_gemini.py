
import asyncio
import os
from dotenv import load_dotenv
from spine.chapters.mind.llm_client import GeminiLLMProvider, LLMClient
from spine.core.config import settings

# Force load .env
load_dotenv()

async def verify_gemini():
    """Verifies that the Real Gemini Integration works with the provided key."""
    api_key = settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("FAIL: No GEMINI_API_KEY found in settings or env.")
        return

    print(f"Initializing Gemini Provider with Key: {api_key[:5]}...{api_key[-4:]}")
    
    try:
        provider = GeminiLLMProvider(api_key=api_key)
        client = LLMClient(provider)
        
        print("Sending request: 'What is 2+2?'")
        response = await client.think("What is 2+2? Reply with just the number.")
        
        print(f"Response: {response}")
        
        if "4" in response:
            print("SUCCESS: Gemini is thinking!")
            # Generate Visual Log
            with open("verify_gemini.log", "w") as f:
                f.write(f"Gemini Verification: PASSED\nResponse: {response}\nKey Hash: {hash(api_key)}")
        else:
            print("WARNING: Unexpected response.")
            
    except Exception as e:
        print(f"FAIL: Error during execution: {e}")

if __name__ == "__main__":
    asyncio.run(verify_gemini())
