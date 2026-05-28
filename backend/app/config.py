from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def env_value(*names: str, default: str) -> str:
    for name in names:
        value = os.getenv(name)
        if value is not None:
            return value
    return default


def env_int(*names: str, default: int) -> int:
    return int(env_value(*names, default=str(default)))


def env_bool(*names: str, default: bool) -> bool:
    value = env_value(*names, default=str(default)).strip().lower()
    return value in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    host: str
    port: int
    api_cors_origins: str
    max_message_chars: int
    max_content_length_bytes: int
    message_cooldown_seconds: int
    max_queue_depth: int
    max_active_sessions: int
    session_idle_timeout_seconds: int
    max_concurrent_generations: int
    index_path: Path
    corpus_path: Path
    generation_provider: str
    ollama_base_url: str
    fast_model_name: str
    fast_think: bool
    fast_context_max_chars: int
    fast_candidate_k: int
    fast_final_source_count: int
    fast_generation_max_tokens: int
    thinking_model_name: str
    thinking_think: bool
    thinking_context_max_chars: int
    thinking_candidate_k: int
    thinking_final_source_count: int
    thinking_generation_max_tokens: int
    thinking_timeout_seconds: int
    embedding_model_name: str
    corpus_version: str


def load_settings() -> Settings:
    return Settings(
        host=env_value("RAG_API_HOST", "RAG_HOST", default="127.0.0.1"),
        port=env_int("RAG_API_PORT", "RAG_PORT", default=8788),
        api_cors_origins=env_value("RAG_ALLOWED_ORIGINS", "RAG_CORS_ORIGIN", default="*"),
        max_message_chars=env_int("RAG_MAX_MESSAGE_CHARS", default=2000),
        max_content_length_bytes=env_int("RAG_MAX_CONTENT_LENGTH_BYTES", default=8192),
        message_cooldown_seconds=env_int("RAG_MESSAGE_COOLDOWN_SECONDS", default=15),
        max_queue_depth=env_int("RAG_MAX_QUEUE_DEPTH", default=5),
        max_active_sessions=env_int("RAG_MAX_ACTIVE_SESSIONS", default=2),
        session_idle_timeout_seconds=env_int("RAG_SESSION_IDLE_TIMEOUT_SECONDS", default=600),
        max_concurrent_generations=env_int("RAG_MAX_CONCURRENT_GENERATIONS", default=1),
        index_path=Path(
            env_value("RAG_INDEX_PATH", "RAG_INDEX_DB_PATH", default=str(ROOT / "data" / "index" / "sources.json"))
        ),
        corpus_path=Path(
            env_value("RAG_CORPUS_PATH", "RAG_CORPUS_DIR", default=str(ROOT.parent / "examples" / "raw-corpus"))
        ),
        generation_provider=env_value("RAG_GENERATION_PROVIDER", default="placeholder"),
        ollama_base_url=env_value("RAG_OLLAMA_BASE_URL", "RAG_GENERATION_BASE_URL", default="http://127.0.0.1:11434"),
        fast_model_name=env_value("RAG_FAST_MODEL_NAME", default="placeholder-fast-model"),
        fast_think=env_bool("RAG_FAST_THINK", default=False),
        fast_context_max_chars=env_int("RAG_FAST_CONTEXT_MAX_CHARS", default=6000),
        fast_candidate_k=env_int("RAG_FAST_RETRIEVAL_CANDIDATE_K", default=20),
        fast_final_source_count=env_int("RAG_FAST_FINAL_SOURCE_COUNT", default=5),
        fast_generation_max_tokens=env_int("RAG_FAST_GENERATION_MAX_TOKENS", "RAG_GENERATION_MAX_TOKENS", default=768),
        thinking_model_name=env_value("RAG_THINKING_MODEL_NAME", default="placeholder-thinking-model"),
        thinking_think=env_bool("RAG_THINKING_THINK", default=True),
        thinking_context_max_chars=env_int("RAG_THINKING_CONTEXT_MAX_CHARS", default=16000),
        thinking_candidate_k=env_int("RAG_THINKING_RETRIEVAL_CANDIDATE_K", default=30),
        thinking_final_source_count=env_int("RAG_THINKING_FINAL_SOURCE_COUNT", default=5),
        thinking_generation_max_tokens=env_int("RAG_THINKING_GENERATION_MAX_TOKENS", default=1024),
        thinking_timeout_seconds=env_int("RAG_THINKING_TIMEOUT_SECONDS", "RAG_GENERATION_TIMEOUT_SECONDS", default=180),
        embedding_model_name=env_value("RAG_EMBEDDING_MODEL", "RAG_EMBEDDING_MODEL_NAME", default="keyword-retrieval"),
        corpus_version=env_value("RAG_CORPUS_VERSION", default="example-local"),
    )
