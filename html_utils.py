# advanced_text_cleaner/html_utils.py
from bs4 import BeautifulSoup
import re

def strip_html_tags(text: str) -> str:
    """Remove HTML tags and collapse entities. Keeps visible text."""
    if not text:
        return text
    try:
        soup = BeautifulSoup(text, "html.parser")
        # remove script/style
        for s in soup(["script", "style"]):
            s.decompose()
        visible = soup.get_text(separator=" ")
        # collapse whitespace
        visible = re.sub(r'\s+', ' ', visible).strip()
        return visible
    except Exception:
        # fallback: naive tag removal
        return re.sub(r'<[^>]+>', ' ', text)
