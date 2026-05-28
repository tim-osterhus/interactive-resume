from __future__ import annotations

from pathlib import Path

from app.evaluate import read_jsonl, run_eval, score_row


def test_score_row_checks_citations_required_forbidden_and_missing_evidence():
    row = {
        "expected_source_tags": ["sample-project"],
        "required_phrases": ["citation popups"],
        "forbidden_phrases": ["guaranteed revenue"],
        "must_admit_missing_evidence": True,
    }
    answer = "The corpus is missing revenue proof, but it does mention citation popups [S1]."
    sources = [{"id": "S1", "title": "Sample Project", "source_slug": "sample-project"}]

    scores = score_row(row, answer, sources)

    assert scores["citation_contract_ok"] is True
    assert scores["expected_source_recall"] == 1
    assert scores["required_phrase_hits"] == 1
    assert scores["forbidden_phrase_hits"] == 0
    assert scores["missing_evidence_ok"] is True


def test_read_jsonl_skips_blank_lines(tmp_path: Path):
    path = tmp_path / "questions.jsonl"
    path.write_text('{"id":"one"}\n\n{"id":"two"}\n', encoding="utf-8")

    assert [row["id"] for row in read_jsonl(path)] == ["one", "two"]


def test_run_eval_writes_summary(configured_env, tmp_path: Path):
    questions = tmp_path / "questions.jsonl"
    output_dir = tmp_path / "runs"
    questions.write_text(
        '{"id":"q1","question":"What shipped citation popups?","role":"builder",'
        '"expected_source_tags":["sample-project"],"required_phrases":["placeholder generator"]}\n',
        encoding="utf-8",
    )

    result = run_eval(questions, output_dir)

    assert result["summary"]["question_count"] == 1
    assert result["summary"]["citation_contract_failures"] == 0
    assert Path(result["output_path"]).exists()
