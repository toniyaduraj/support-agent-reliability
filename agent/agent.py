import json
import pathlib
import time

import anthropic

from agent.config import AGENT_MODEL, MAX_TOKENS, MAX_TURNS
from agent.tools import TOOLS, run_tool

SYSTEM = (pathlib.Path(__file__).parent / "prompts" / "system.md").read_text()
client = anthropic.Anthropic()


def ask(question: str) -> dict:
    """Run the agent loop: call Claude, execute requested tools, repeat until a final answer."""
    t0 = time.time()
    messages = [{"role": "user", "content": question}]
    tool_calls, usage = [], {"input_tokens": 0, "output_tokens": 0}

    for turn in range(MAX_TURNS):
        resp = client.messages.create(
            model=AGENT_MODEL, max_tokens=MAX_TOKENS, system=SYSTEM, tools=TOOLS, messages=messages
        )
        usage["input_tokens"] += resp.usage.input_tokens
        usage["output_tokens"] += resp.usage.output_tokens

        if resp.stop_reason != "tool_use":
            answer = "".join(b.text for b in resp.content if b.type == "text")
            return {
                "answer": answer,
                "tool_calls": tool_calls,
                "turns": turn + 1,
                "usage": usage,
                "latency_s": round(time.time() - t0, 2),
            }

        messages.append({"role": "assistant", "content": resp.content})
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                out = run_tool(block.name, block.input)
                tool_calls.append({"name": block.name, "input": block.input, "output": out})
                results.append(
                    {"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(out)}
                )
        messages.append({"role": "user", "content": results})

    return {
        "answer": None,
        "tool_calls": tool_calls,
        "turns": MAX_TURNS,
        "usage": usage,
        "latency_s": round(time.time() - t0, 2),
        "error": "max_turns_exceeded",
    }
