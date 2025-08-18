# services/chatgpt.py
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = "sk-FVfnGCatZKcW1ykd1BfH13dDCYjX8fadVBFSGZnANukUeCKK"

def get_chatgpt_response(prompt: str, model: str = "gpt-5-mini", temperature: float = 0.3, max_tokens: int = 4000) -> str:
    """
    Get response from ChatGPT using the OpenAI API.

    Args:
        prompt (str): The user prompt.
        model (str): Model to use, e.g., 'gpt-5-mini' or 'gpt-4o'.
        temperature (float): Creativity of the output (0-1).
        max_tokens (int): Maximum tokens to generate.

    Returns:
        str: Full response text from ChatGPT.
    """

    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "hello"}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )

    # Extract text from the response
    return response.choices[0].message["content"]
