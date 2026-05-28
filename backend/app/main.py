from __future__ import annotations

import time
import uuid

from flask import Flask, jsonify, request

from .config import load_settings
from .cors import install_cors
from .generation import generate_answer
from .prompts import ALLOWED_MODES, ALLOWED_MODEL_PROFILES, ALLOWED_ROLES
from .rate_limits import CooldownLimiter
from .retrieval import load_sources, retrieve

STARTED_AT = time.time()


def create_app() -> Flask:
    settings = load_settings()
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = settings.max_content_length_bytes
    install_cors(app, settings.api_cors_origins)
    limiter = CooldownLimiter(settings.message_cooldown_seconds, settings.session_idle_timeout_seconds)

    @app.get("/health")
    def health():
        active_sessions = limiter.active_count()
        return jsonify(
            {
                "ok": True,
                "model": settings.fast_model_name,
                "generation_provider": settings.generation_provider,
                "default_model_profile": "fast",
                "model_profiles": {
                    "fast": {
                        "model": settings.fast_model_name,
                        "think": settings.fast_think,
                        "candidate_k": settings.fast_candidate_k,
                        "context_max_chars": settings.fast_context_max_chars,
                        "final_source_count": settings.fast_final_source_count,
                        "packing_strategy": "keyword_sources_placeholder",
                    },
                    "thinking": {
                        "model": settings.thinking_model_name,
                        "think": settings.thinking_think,
                        "candidate_k": settings.thinking_candidate_k,
                        "context_max_chars": settings.thinking_context_max_chars,
                        "final_source_count": settings.thinking_final_source_count,
                        "packing_strategy": "keyword_sources_placeholder",
                    },
                },
                "embedding_model": settings.embedding_model_name,
                "corpus_version": settings.corpus_version,
                "uptime_seconds": int(time.time() - STARTED_AT),
                "queue_depth": 0,
                "max_queue_depth": settings.max_queue_depth,
                "active_sessions": active_sessions,
                "max_active_sessions": settings.max_active_sessions,
                "active_generations": 0,
                "max_concurrent_generations": settings.max_concurrent_generations,
                "max_message_chars": settings.max_message_chars,
                "message_cooldown_seconds": settings.message_cooldown_seconds,
            }
        )

    @app.post("/chat")
    def chat():
        payload = request.get_json(silent=True) or {}
        message = str(payload.get("message", "")).strip()
        role = str(payload.get("role", "recruiter")).strip()
        mode = payload.get("mode")
        model_profile = str(payload.get("model_profile", "fast")).strip()
        session_id = str(payload.get("session_id") or uuid.uuid4())

        if request.method == "OPTIONS":
            return ("", 204)
        if not message:
            return jsonify({"error": {"code": "empty_message", "message": "Message is required."}}), 400
        if len(message) > settings.max_message_chars:
            return jsonify({"error": {"code": "message_too_long", "message": "Message is too long."}}), 400
        if role not in ALLOWED_ROLES:
            return jsonify({"error": {"code": "invalid_role", "message": "Unknown role."}}), 400
        if model_profile not in ALLOWED_MODEL_PROFILES:
            return jsonify({"error": {"code": "invalid_model_profile", "message": "Unknown model profile."}}), 400
        if mode is not None and mode not in ALLOWED_MODES:
            return jsonify({"error": {"code": "invalid_mode", "message": "Unknown mode."}}), 400
        if limiter.at_capacity(session_id, settings.max_active_sessions):
            return jsonify({"error": {"code": "at_capacity", "message": "Too many active sessions."}}), 429
        if not limiter.check(session_id):
            return jsonify({"error": {"code": "rate_limited", "message": "Please wait before sending another message."}}), 429

        indexed_sources = load_sources(settings.index_path)
        source_limit = (
            settings.thinking_final_source_count
            if model_profile == "thinking"
            else settings.fast_final_source_count
        )
        sources = retrieve(message, indexed_sources, limit=source_limit)
        answer, model = generate_answer(settings, message, role, sources, mode, model_profile)
        confidence = "low" if not sources else "medium"
        return jsonify(
            {
                "answer": answer,
                "sources": sources,
                "confidence": confidence,
                "mode": mode or "proof",
                "role": role,
                "model_profile": model_profile,
                "model": model,
                "corpus_version": settings.corpus_version,
                "placeholder_generation": settings.generation_provider == "placeholder",
            }
        )

    return app


def main() -> None:
    settings = load_settings()
    create_app().run(host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
