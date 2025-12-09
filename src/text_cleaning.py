import re

def clean_text(text: str) -> str:
    # remove weird characters that sometimes sneak in
    text = text.replace("|", " ").replace("\t", " ")
    # collapse multiple spaces
    text = re.sub(r" {2,}", " ", text)
    # normalize newlines (avoid 4–5 blank lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
