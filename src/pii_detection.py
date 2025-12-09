from typing import Dict, List
import re

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[A-Za-z]{2,}")
PHONE_REGEX = re.compile(r"(\+?\d[\d\-\s]{7,}\d)")   # picks up most phone numbers
DATE_REGEX = re.compile(r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b")
ID_REGEX = re.compile(r"\b(?:ID|Patient\s*ID|MRN)[:\s]*([A-Za-z0-9\-]{3,})\b", re.IGNORECASE)

def _unique(matches):
    out = []
    for m in matches:
        if isinstance(m, tuple):
            m = "".join(m)
        if m and m not in out:
            out.append(m)
    return out

def detect_pii(text: str) -> Dict[str, List[str]]:
    emails = _unique(EMAIL_REGEX.findall(text))
    phones = _unique(PHONE_REGEX.findall(text))
    dates = _unique(DATE_REGEX.findall(text))
    ids = _unique(ID_REGEX.findall(text))

    return {
        "email": emails,
        "phone": phones,
        "date": dates,
        "id": ids,
    }
