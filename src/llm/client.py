from __future__ import annotations

import json
from typing import Any

from openai import OpenAI

from src.config import get_deepseek_client, DEEPSEEK_MODEL


def call_llm(
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float = 0.3,
    max_tokens: int = 8192,
    response_format: str | None = None,
) -> str:
    client = get_deepseek_client()
    if client is None:
        raise RuntimeError(
            "DeepSeek client not configured. Set DEEPSEEK_API_KEY environment variable."
        )

    kwargs: dict[str, Any] = dict(
        model=DEEPSEEK_MODEL,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    if response_format == "json_object":
        kwargs["response_format"] = {"type": "json_object"}

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        **kwargs,
    )
    return response.choices[0].message.content or ""


def call_llm_json(
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float = 0.1,
    max_tokens: int = 8192,
) -> dict[str, Any]:
    content = call_llm(
        system_prompt,
        user_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        response_format="json_object",
    )
    return json.loads(content)
