from typing import Literal

from pydantic import BaseModel, ValidationInfo, field_validator

Category = Literal[
    "factual",
    "multi_hop",
    "version_specific",
    "unanswerable",
    "out_of_scope",
    "ambiguous",
    "injection",
]
Tool = Literal["search_docs", "get_doc", "get_changelog", "escalate", "none"]


class GoldenCase(BaseModel):
    id: str
    question: str
    category: Category
    expected_doc_ids: list[str] = []
    expected_tool: Tool
    should_escalate: bool
    reference_answer: str = ""
    must_include: list[str] = []
    must_not_include: list[str] = []
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    source: str = "handwritten"
    notes: str = ""

    @field_validator("expected_doc_ids")
    @classmethod
    def answerable_needs_docs(cls, v: list[str], info: ValidationInfo) -> list[str]:
        cat = info.data.get("category")
        if cat in {"factual", "multi_hop", "version_specific"} and not v:
            raise ValueError(f"{cat} case needs expected_doc_ids")
        return v
