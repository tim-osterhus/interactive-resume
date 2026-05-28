from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from .config import load_settings
from .generation import generate_answer
from .retrieval import load_sources, retrieve


CITATION_RE = re.compile(r"\[S[0-9]+\]")
MISSING_EVIDENCE_TERMS = ("not have enough", "missing", "weak", "no relevant evidence")


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def score_row(row: dict, answer: str, sources: list[dict]) -> dict:
    answer_lower = answer.lower()
    source_text = " ".join(
        [source.get("title", "") + " " + source.get("source_slug", "") for source in sources]
    ).lower()
    expected = [item.lower() for item in row.get("expected_source_tags", [])]
    required = [item.lower() for item in row.get("required_phrases", [])]
    forbidden = [item.lower() for item in row.get("forbidden_phrases", [])]
    return {
        "citation_contract_ok": bool(CITATION_RE.search(answer)) if sources else True,
        "expected_source_recall": sum(1 for item in expected if item in source_text),
        "expected_source_total": len(expected),
        "required_phrase_hits": sum(1 for item in required if item in answer_lower),
        "required_phrase_total": len(required),
        "forbidden_phrase_hits": sum(1 for item in forbidden if item in answer_lower),
        "missing_evidence_ok": (
            any(term in answer_lower for term in MISSING_EVIDENCE_TERMS)
            if row.get("must_admit_missing_evidence")
            else True
        ),
    }


def run_eval(questions: Path, output_dir: Path) -> dict:
    settings = load_settings()
    indexed_sources = load_sources(settings.index_path)
    rows = read_jsonl(questions)
    results = []
    for row in rows:
        profile = row.get("model_profile", "fast")
        source_limit = (
            settings.thinking_final_source_count
            if profile == "thinking"
            else settings.fast_final_source_count
        )
        sources = retrieve(row["question"], indexed_sources, limit=source_limit)
        answer, model = generate_answer(
            settings,
            row["question"],
            row.get("role", "recruiter"),
            sources,
            row.get("mode"),
            profile,
        )
        scores = score_row(row, answer, sources)
        results.append({"id": row["id"], "answer": answer, "sources": sources, "model": model, "scores": scores})

    summary = {
        "question_count": len(rows),
        "citation_contract_failures": sum(1 for item in results if not item["scores"]["citation_contract_ok"]),
        "forbidden_phrase_failures": sum(1 for item in results if item["scores"]["forbidden_phrase_hits"]),
        "missing_evidence_failures": sum(1 for item in results if not item["scores"]["missing_evidence_ok"]),
        "expected_source_hits": sum(item["scores"]["expected_source_recall"] for item in results),
        "expected_source_total": sum(item["scores"]["expected_source_total"] for item in results),
    }
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ-smoke-eval")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{run_id}.json"
    output_path.write_text(json.dumps({"summary": summary, "results": results}, indent=2), encoding="utf-8")
    return {"summary": summary, "output_path": str(output_path)}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run local smoke evals.")
    parser.add_argument("--questions", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("data/evals/runs"))
    args = parser.parse_args()
    result = run_eval(args.questions, args.output_dir)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
