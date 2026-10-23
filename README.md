# Support Agent Reliability Lab

A reliability harness for an LLM support agent. The agent answers questions about the
[dbt](https://docs.getdbt.com) documentation using tool calls; the harness measures whether it
retrieves the right docs, cites honestly, escalates correctly, and resists prompt injection.

The agent is the test subject. The harness is the product.

## Status

| Week | Focus | Status |
|---|---|---|
| 1 | Baseline agent + golden set | ✅ |
| 2 | Tracing, cost, remaining tools | ⬜ |
| 3 | Eval harness + calibrated LLM judge | ⬜ |
| 4 | Failure analysis | ⬜ |
| 5 | Fixes + CI eval gate | ⬜ |
| 6 | Fault injection + adversarial tests | ⬜ |
| 7 | Drift detection + dashboard | ⬜ |
| 8 | Design doc + write-up | ⬜ |

## Quickstart

**Prerequisites:** [uv](https://docs.astral.sh/uv/), Docker, and an Anthropic API key.

```bash
git clone https://github.com/toniyaduraj/support-agent-reliability.git
cd support-agent-reliability
cp .env.example .env        # then set ANTHROPIC_API_KEY in .env
make setup                  # install deps, start Postgres + pgvector
make index                  # fetch dbt docs at the pinned commit, chunk, embed
make ask Q="How do I run only the models that changed?"
make test                   # validate the golden set
```

The first `make index` clones the docs and downloads a small embedding model (about 70 s on an
Apple Silicon Mac).

## How it works

- **Corpus:** dbt docs (Apache-2.0), fetched at the commit pinned in `corpus.lock`, never
  committed. The same SHA gives the same index on any machine.
- **Retrieval:** fixed-size chunks (1,200 characters, 200 overlap), `bge-small` embeddings,
  cosine search in pgvector.
- **Agent:** Claude with two tools, `search_docs` and `escalate`, capped at 6 turns. The system
  prompt (`agent/prompts/system.md`) requires grounded, cited answers, abstaining when the
  docs don't answer, and ignoring instructions inside documents.
- **Golden set:** 50 hand-written cases in `evals/datasets/golden_v1.jsonl` across factual,
  multi-hop, version-specific, unanswerable, out-of-scope, ambiguous and injection categories.
  Tests check that every expected doc ID exists in the corpus.

## Baseline (v0.1.0)

| Metric | Value |
|---|---|
| Corpus | 1,196 docs, 8,801 chunks, commit `8398a565` |
| Index build | ~70 s |
| Sample answer | 2 turns, ~6 s, ~4.4k input / ~0.5k output tokens |

## Known issues (to be measured in Week 3)

- **Vocabulary mismatch:** user wording ("changed") differs from doc terms ("state:modified").
  The agent compensates by rewriting queries from prior knowledge.
- **Chunk boundaries:** fixed-size chunks can split a section before the key command.
- **Labels:** some golden cases may list too few acceptable docs, causing false retrieval misses.

Engineering notes live in [`docs/friction-log.md`](docs/friction-log.md).
