import json
import pathlib
import uuid
from typing import Literal

from pydantic import BaseModel, Field

from retrieval.search import search_docs


class SearchInput(BaseModel):
    query: str = Field(description="Search query about dbt")
    k: int = Field(default=5, ge=1, le=10, description="Number of chunks to return")


class EscalateInput(BaseModel):
    reason: Literal["out_of_scope", "insufficient_docs", "bug_report", "account_specific"]
    summary: str = Field(description="One-sentence summary for the human agent")


TOOLS = [
    {
        "name": "search_docs",
        "description": (
            "Search the dbt documentation. Returns chunks with chunk_id, doc_id, title and "
            "snippet. Use for any question about dbt features, commands or configuration."
        ),
        "input_schema": SearchInput.model_json_schema(),
    },
    {
        "name": "escalate",
        "description": (
            "Hand off to a human when the question is outside dbt, the docs do not answer it, "
            "it reports a bug, or it concerns a specific user's account or billing."
        ),
        "input_schema": EscalateInput.model_json_schema(),
    },
]


def run_tool(name: str, args: dict) -> dict:
    """Validate inputs and run a tool. Errors are returned, never raised, so the agent sees them."""
    try:
        if name == "search_docs":
            a = SearchInput(**args)
            return {"results": search_docs(a.query, a.k)}
        if name == "escalate":
            a = EscalateInput(**args)
            ticket = f"T-{uuid.uuid4().hex[:8]}"
            log = pathlib.Path("data/escalations.jsonl")
            log.parent.mkdir(exist_ok=True)
            with log.open("a") as f:
                f.write(json.dumps({"ticket": ticket, **a.model_dump()}) + "\n")
            return {"ticket_id": ticket}
        return {"error": f"unknown tool {name}"}
    except Exception as e:  # noqa: BLE001 - tool boundary: any failure is returned to the model
        return {"error": f"{type(e).__name__}: {e}"}
