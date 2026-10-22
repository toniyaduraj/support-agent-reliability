import time

import psycopg
from pgvector.psycopg import register_vector
from sentence_transformers import SentenceTransformer

from agent.config import DB_URL, EMBED_MODEL
from retrieval.chunk import fixed_chunks, split_frontmatter, title_of
from retrieval.ingest import fetch, iter_docs


def main() -> None:
    t0 = time.time()
    sha = fetch()
    rows = []
    for doc_id, raw in iter_docs():
        fm, body = split_frontmatter(raw)
        title = title_of(fm, doc_id.split("/")[-1])
        for n, chunk in enumerate(fixed_chunks(body)):
            rows.append((f"{doc_id}#{n}", doc_id, title, chunk))
    print(f"{len(rows)} chunks from corpus {sha[:8]}")

    model = SentenceTransformer(EMBED_MODEL)
    embs = model.encode(
        [r[3] for r in rows], normalize_embeddings=True, batch_size=64, show_progress_bar=True
    )

    with psycopg.connect(DB_URL) as conn:
        register_vector(conn)
        conn.execute("TRUNCATE chunks")
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO chunks (chunk_id, doc_id, title, content, corpus_sha, embedding)"
                " VALUES (%s, %s, %s, %s, %s, %s)",
                [(cid, did, t, c, sha, e) for (cid, did, t, c), e in zip(rows, embs)],
            )
    print(f"index built in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
