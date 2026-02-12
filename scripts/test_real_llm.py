import sys
import os
sys.path.append(os.getcwd())

from chapters.brain.llm import OpenAIProvider

def test_real_brain():
    print(">>> Testing Real OpenAI Connection...")
    try:
        provider = OpenAIProvider()
        print(f"    Loaded {len(provider.keys)} keys.")
        
        response = provider.generate(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say 'Hello World' key verification."
        )
        print(f"    Response: {response}")
        print(">>> SUCCESS: Real LLM is Online.")
    except Exception as e:
        print(f"    FAIL: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_real_brain()
