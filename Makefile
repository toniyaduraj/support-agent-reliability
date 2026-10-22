.PHONY: setup index ask test lint
setup:
	uv sync
	docker compose up -d db
index:
	uv run python -m retrieval.index
ask:
	uv run python -m agent.cli "$(Q)"
test:
	uv run pytest -q
lint:
	uv run ruff check . && uv run ruff format --check .
