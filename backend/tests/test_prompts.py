from __future__ import annotations

import pytest

from app.prompts import ALLOWED_ROLES, build_prompt


def test_all_allowed_roles_have_prompt_addendums():
    for role in ALLOWED_ROLES:
        prompt = build_prompt(
            "What matters?",
            role,
            [{"id": "S1", "title": "Sample Project", "excerpt": "Built a useful thing."}],
        )

        assert "Answer only from provided evidence" in prompt
        assert "[S1] Sample Project" in prompt
        assert "Question: What matters?" in prompt


def test_prompt_includes_mode_only_when_supplied():
    prompt_without_mode = build_prompt("What matters?", "builder", [])
    prompt_with_mode = build_prompt("What matters?", "builder", [], mode="proof")

    assert "Requested evidence mode" not in prompt_without_mode
    assert "Requested evidence mode: proof." in prompt_with_mode
    assert "No relevant evidence was retrieved." in prompt_without_mode


def test_unknown_role_fails_closed():
    with pytest.raises(KeyError):
        build_prompt("What matters?", "admin", [])
