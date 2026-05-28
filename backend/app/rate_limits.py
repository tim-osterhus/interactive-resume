from __future__ import annotations

import time


class CooldownLimiter:
    def __init__(self, cooldown_seconds: int, idle_timeout_seconds: int = 600):
        self.cooldown_seconds = cooldown_seconds
        self.idle_timeout_seconds = idle_timeout_seconds
        self.last_seen: dict[str, float] = {}

    def _prune(self, now: float) -> None:
        expired = [
            session_id
            for session_id, last_seen in self.last_seen.items()
            if now - last_seen > self.idle_timeout_seconds
        ]
        for session_id in expired:
            self.last_seen.pop(session_id, None)

    def check(self, session_id: str) -> bool:
        now = time.time()
        self._prune(now)
        last = self.last_seen.get(session_id, 0)
        if now - last < self.cooldown_seconds:
            return False
        self.last_seen[session_id] = now
        return True

    def active_count(self) -> int:
        now = time.time()
        self._prune(now)
        return len(self.last_seen)
