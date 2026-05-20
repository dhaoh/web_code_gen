import os

from openai import OpenAI


def get_deepseek_client() -> OpenAI | None:
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        return None
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")


DEEPSEEK_MODEL = "deepseek-v4-pro"
MAX_FEEDBACK_ITERATIONS = 3
