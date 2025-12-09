import easyocr
from typing import Dict, Any, List
import numpy as np

# Initialize once
_reader = easyocr.Reader(['en'], gpu=False)

def run_ocr(image: np.ndarray) -> Dict[str, Any]:
    results = _reader.readtext(image)
    lines = []
    blocks: List[Dict[str, Any]] = []

    for bbox, text, score in results:
        lines.append(text)
        blocks.append({
            "text": text,
            "bbox": bbox,         
            "score": float(score)
        })

    full_text = "\n".join(lines)
    return {"text": full_text, "blocks": blocks}
