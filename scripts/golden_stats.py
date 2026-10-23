import collections
import json
import pathlib

TARGET = {
    "factual": 15,
    "multi_hop": 7,
    "version_specific": 5,
    "unanswerable": 8,
    "out_of_scope": 5,
    "ambiguous": 5,
    "injection": 5,
}
lines = pathlib.Path("evals/datasets/golden_v1.jsonl").read_text().splitlines()
counts = collections.Counter(json.loads(x)["category"] for x in lines if x.strip())
for cat, target in TARGET.items():
    print(f"{cat:<17} {counts[cat]:>2} / {target}")
print(f"{'total':<17} {sum(counts.values()):>2} / {sum(TARGET.values())}")
