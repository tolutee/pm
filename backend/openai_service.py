import os
from typing import Optional

from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Create and return an OpenAI client using OPENAI_API_KEY from environment."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return OpenAI(api_key=api_key)


def simple_math_calculation(expression: str) -> Optional[str]:
    """
    Test function: ask OpenAI to evaluate a simple math expression.
    Returns the calculated result or None if there's an error.
    """
    try:
        client = get_openai_client()
        message = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": f"Calculate this math expression and return only the numeric result: {expression}",
                }
            ],
            temperature=0,
            max_tokens=50,
        )
        return message.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"OpenAI API error: {str(e)}")
