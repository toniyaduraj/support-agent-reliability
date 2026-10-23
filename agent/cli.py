import json
import sys

from agent.agent import ask

if __name__ == "__main__":
    result = ask(" ".join(sys.argv[1:]))
    print(result.get("answer") or f"[no answer: {result.get('error')}]")
    print("\n--- tool calls ---")
    for c in result["tool_calls"]:
        print(f"{c['name']} {json.dumps(c['input'])}")
    print(f"\nturns={result['turns']} latency={result['latency_s']}s usage={result['usage']}")
