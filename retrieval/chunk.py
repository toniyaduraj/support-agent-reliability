import re


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return (frontmatter, body). Frontmatter is the --- block at the top."""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[3:end], text[end + 4 :]
    return "", text


def title_of(frontmatter: str, fallback: str) -> str:
    m = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", frontmatter, re.MULTILINE)
    return m.group(1) if m else fallback


def fixed_chunks(text: str, size: int = 1200, overlap: int = 200) -> list[str]:
    """Baseline: fixed-size character windows with overlap."""
    text = text.strip()
    chunks, i = [], 0
    while i < len(text):
        chunks.append(text[i : i + size])
        i += size - overlap
    return [c for c in chunks if len(c.strip()) > 50]
