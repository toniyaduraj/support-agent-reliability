# Friction log

- setup-uv has no moving major tags; pinned to an exact version (v10.3.1).
- Baseline index: 8,801 chunks / 1,196 docs (fixed 1200-char chunks, 200 overlap), corpus 8398a565, built in 69s on M-series Mac.
- Sparse clone with blob filter still pulled 286k objects of history; consider shallow fetch for CI.
- Corpus license: dbt docs are Apache-2.0; fetched at pinned SHA, not redistributed.
- Follow-up: top-1 (best-practice-workflows#8) IS the slim-CI section, but fixed-size chunking cuts it mid-sentence before the actual command. Second failure mode: chunk boundaries split sections. Test heading-aware chunking in Week 5.
- First agent run (prompt v1): correct, all claims cited. Agent rewrote query to 'state:modified' using prior knowledge, so one search sufficed. Eval idea: measure recall@5 for raw user query vs agent query. Limitation: rewriting relies on model already knowing dbt. Baseline: 2 turns, 6.7s, 4431 in / 637 out tokens.
- Escalation tests pass (out_of_scope, account_specific). Policy question: escalating obviously off-topic questions (weather) wastes human time; consider decline-only for off-topic. Ticket ID shown inconsistently.
- ruff BLE001 flagged blind except in run_tool. Kept it deliberately (tool boundary returns errors to model) with noqa + reason. Revisit in Week 6: typed errors vs catch-all.
- Writing reference answers: my first q-049 answer (from an assistant's prior knowledge) described only v1 tracks; doc shows v2 Nightly/Stable/Extended/Fallback + v1 tracks. Lesson: reference answers must come from the doc, not memory, same failure q-048 tests the agent for.
