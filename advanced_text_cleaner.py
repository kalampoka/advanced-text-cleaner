# advanced_text_cleaner/cleaner.py
from typing import Optional, List, Dict
import re
import ftfy
from .html_utils import strip_html_tags
from .emoji_utils import remove_or_replace_emojis
from unidecode import unidecode

# Optional imports (only used if available)
try:
    from langdetect import detect
except Exception:
    detect = None

# Pipeline config dataclass-ish dict (keeps it simple)
DEFAULT_CONFIG = {
    "lowercase": True,
    "fix_text": True,              # use ftfy to fix mojibake / encoding errors
    "strip_html": True,
    "remove_urls": True,
    "remove_emails": True,
    "normalize_unicode": True,     # use unidecode to normalize accents
    "remove_extra_whitespace": True,
    "remove_punctuation": False,   # optional: often you want punctuation for NLP
    "remove_emojis": False,        # True removes, "replace" replaces with textual aliases
    "emoji_replace_with_alias": True,
    "remove_non_printable": True,
    "language_filter": None,       # e.g. "en" to require English; None = skip
    "min_length": 1,               # minimal length after cleaning
}

URL_RE = re.compile(r'https?://\S+|www\.\S+')
EMAIL_RE = re.compile(r'\b[\w.-]+?@\w+?\.\w+?\b')
NON_PRINTABLE_RE = re.compile(r'[\x00-\x1f\x7f-\x9f]')
MULTI_SPACE_RE = re.compile(r'\s+')

PUNCT_RE = re.compile(r'[^\w\s]')  # basic punctuation removal (keeps underscores/digits/letters)


class AdvancedTextCleaner:
    def __init__(self, config: Optional[Dict] = None):
        cfg = DEFAULT_CONFIG.copy()
        if config:
            cfg.update(config)
        self.cfg = cfg

    def clean(self, text: str) -> Optional[str]:
        if not isinstance(text, str):
            return None
        t = text

        # 1. fix mojibake / encoding issues (ftfy)
        if self.cfg.get("fix_text", True):
            try:
                t = ftfy.fix_text(t)
            except Exception:
                pass

        # 2. optionally strip HTML
        if self.cfg.get("strip_html", True):
            t = strip_html_tags(t)

        # 3. remove URLs and emails
        if self.cfg.get("remove_urls", True):
            t = URL_RE.sub(" ", t)
        if self.cfg.get("remove_emails", True):
            t = EMAIL_RE.sub(" ", t)

        # 4. normalize unicode (accents -> ascii)
        if self.cfg.get("normalize_unicode", True):
            try:
                t = unidecode(t)
            except Exception:
                pass

        # 5. handle emojis
        if self.cfg.get("remove_emojis", False):
            t = remove_or_replace_emojis(t, replace=not self.cfg.get("emoji_replace_with_alias", False))
        elif self.cfg.get("emoji_replace_with_alias", False):
            # if replace aliases set and not removing
            t = remove_or_replace_emojis(t, replace=True)

        # 6. remove non-printable
        if self.cfg.get("remove_non_printable", True):
            t = NON_PRINTABLE_RE.sub(" ", t)

        # 7. lowercase
        if self.cfg.get("lowercase", True):
            t = t.lower()

        # 8. remove punctuation (optional)
        if self.cfg.get("remove_punctuation", False):
            t = PUNCT_RE.sub(" ", t)

        # 9. collapse whitespace
        if self.cfg.get("remove_extra_whitespace", True):
            t = MULTI_SPACE_RE.sub(" ", t).strip()

        # 10. language filter (optional)
        lang = None
        if self.cfg.get("language_filter") and detect:
            try:
                lang = detect(t) if t.strip() else None
                if lang != self.cfg.get("language_filter"):
                    return None
            except Exception:
                pass

        # 11. min length check
        if len(t) < self.cfg.get("min_length", 1):
            return None

        return t
