from __future__ import annotations

import requests

from .prompts import build_prompt


def placeholder_answer(message: str, sources: list[dict]) -> str:
    if not sources:
        return (
            "I do not have enough retrieved evidence to answer that from the corpus. "
            "Add or ingest a source document that covers this topic."
        )
    lower_message = message.lower()
    if any(term in lower_message for term in ("revenue", "fundraising", "traffic")):
        return (
            f"The retrieved evidence does not prove revenue, fundraising, or production "
            f"traffic for this sample. Treat those claims as missing evidence unless the "
            f"owner adds a public-safe source [{sources[0]['id']}]."
        )
    lead = sources[0]
    source_list = ", ".join(f"[{source['id']}]" for source in sources)
    return (
        f"Based on the available example evidence, the strongest answer is in "
        f"{lead['title']} {source_list}. This placeholder generator is for smoke "
        f"testing only; configure a local model runtime before public launch."
    )


def ollama_answer(
    base_url: str,
    model: str,
    prompt: str,
    *,
    think: bool = False,
    max_tokens: int = 768,
    timeout: int = 60,
) -> str:
    response = requests.post(
        f"{base_url.rstrip('/')}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False,
            "think": think,
            "options": {"num_predict": max_tokens},
        },
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json().get("response", "").strip()


def generate_answer(settings, message: str, role: str, sources: list[dict], mode: str | None, profile: str) -> tuple[str, str]:
    model = settings.thinking_model_name if profile == "thinking" else settings.fast_model_name
    if settings.generation_provider == "ollama":
        prompt = build_prompt(message, role, sources, mode)
        think = settings.thinking_think if profile == "thinking" else settings.fast_think
        max_tokens = (
            settings.thinking_generation_max_tokens
            if profile == "thinking"
            else settings.fast_generation_max_tokens
        )
        timeout = settings.thinking_timeout_seconds if profile == "thinking" else 60
        return (
            ollama_answer(
                settings.ollama_base_url,
                model,
                prompt,
                think=think,
                max_tokens=max_tokens,
                timeout=timeout,
            ),
            model,
        )
    return placeholder_answer(message, sources), model
