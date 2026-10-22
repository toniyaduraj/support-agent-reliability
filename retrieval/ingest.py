import pathlib
import subprocess

from agent.config import DOCS_SUBDIR, UPSTREAM_DIR

REPO = "https://github.com/dbt-labs/docs.getdbt.com.git"
LOCK = pathlib.Path("corpus.lock")


def _git(*args: str) -> str:
    out = subprocess.run(
        ["git", "-C", UPSTREAM_DIR, *args], check=True, capture_output=True, text=True
    )
    return out.stdout.strip()


def fetch() -> str:
    """Clone docs (sparse) and check out the pinned SHA if corpus.lock exists."""
    if not pathlib.Path(UPSTREAM_DIR).exists():
        subprocess.run(
            ["git", "clone", "--filter=blob:none", "--sparse", REPO, UPSTREAM_DIR], check=True
        )
        _git("sparse-checkout", "set", DOCS_SUBDIR)
    if LOCK.exists():
        sha = LOCK.read_text().strip()
        _git("fetch", "origin", sha)
        _git("checkout", sha)
    sha = _git("rev-parse", "HEAD")
    LOCK.write_text(sha + "\n")
    return sha


def iter_docs():
    """Yield (doc_id, text) for every markdown doc in the corpus."""
    root = pathlib.Path(UPSTREAM_DIR) / DOCS_SUBDIR
    paths = sorted([*root.rglob("*.md"), *root.rglob("*.mdx")])
    for path in paths:
        doc_id = str(path.relative_to(root).with_suffix(""))
        yield doc_id, path.read_text(encoding="utf-8", errors="ignore")
