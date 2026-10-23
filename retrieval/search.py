import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

from agent.config import DB_URL, EMBED_MODEL, QUERY_PREFIX

_model: SentenceTransformer | None = None


def _get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBED_MODEL)
    return _model


def search_docs(query: str, k: int = 5) -> list[dict]:
    """Dense retrieval over the chunks table (cosine similarity)."""
    q = _get_model().encode(QUERY_PREFIX + query, normalize_embeddings=True)
    with psycopg.connect(DB_URL) as conn:
        register_vector(conn)
        rows = conn.execute(
            "SELECT chunk_id, doc_id, title, content, 1 - (embedding <=> %s) AS score"
            " FROM chunks ORDER BY embedding <=> %s LIMIT %s",
            (q, q, k),
        ).fetchall()
    return [
        {"chunk_id": c, "doc_id": d, "title": t, "snippet": txt[:800], "score": round(float(s), 3)}
        for c, d, t, txt, s in rows
    ]
