import os

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@localhost:5432/agent")
AGENT_MODEL = os.getenv("AGENT_MODEL", "claude-sonnet-5-5")
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-en-v1.5")
EMBED_DIM = 384
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "
MAX_TURNS = int(os.getenv("MAX_TURNS", "6"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "1024"))
UPSTREAM_DIR = "data/upstream"
DOCS_SUBDIR = "website/docs"
