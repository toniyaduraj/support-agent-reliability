import json
import pathlib

import pytest

from evals.schema import GoldenCase

PATH = pathlib.Path("evals/datasets/golden_v1.jsonl")
CORPUS = pathlib.Path("data/upstream/website/docs")


def load() -> list[dict]:
    return [json.loads(line) for line in PATH.read_text().splitlines() if line.strip()]


def test_cases_valid_and_enough():
    cases = [GoldenCase(**c) for c in load()]
    assert len(cases) >= 50, f"only {len(cases)} cases"


def test_ids_unique():
    ids = [c["id"] for c in load()]
    assert len(ids) == len(set(ids))


@pytest.mark.skipif(not CORPUS.exists(), reason="corpus not fetched (CI)")
def test_expected_docs_exist():
    missing = [
        (c["id"], d)
        for c in load()
        for d in c.get("expected_doc_ids", [])
        if not any((CORPUS / f"{d}{ext}").exists() for ext in (".md", ".mdx"))
    ]
    assert not missing, f"unknown doc ids: {missing}"
