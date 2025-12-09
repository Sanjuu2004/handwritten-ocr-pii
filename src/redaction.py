from typing import Dict, List, Tuple, Any
import numpy as np
import cv2

def redact_text(text: str, pii: Dict[str, List[str]]) -> str:
    redacted = text
    for _, values in pii.items():
        for v in values:
            if not v:
                continue
            redacted = redacted.replace(v, "[REDACTED]")
    return redacted


def analyze_and_redact_image(
    original_img: np.ndarray,
    blocks: List[Dict[str, Any]],
    pii: Dict[str, List[str]],
    conf_threshold: float = 0.4,
) -> Tuple[np.ndarray, np.ndarray, Dict[str, int]]:
    
    # Collect all sensitive strings
    sensitive_strings = set()
    for values in pii.values():
        for v in values:
            if v:
                sensitive_strings.add(v)

    # Copy images
    redacted_img = original_img.copy()
    preview_img = original_img.copy()

    total_blocks = len(blocks)
    pii_blocks = 0
    redacted_blocks = 0
    low_conf_pii_blocks = 0

    for block in blocks:
        text = block.get("text", "")
        score = float(block.get("score", 0.0))
        bbox = np.array(block["bbox"], dtype=int)  # shape (4, 2)

        xs = bbox[:, 0]
        ys = bbox[:, 1]
        x_min, x_max = xs.min(), xs.max()
        y_min, y_max = ys.min(), ys.max()

        # Does this block contain PII?
        has_pii = any(s in text for s in sensitive_strings)

        if has_pii:
            pii_blocks += 1
            if score >= conf_threshold:
                # High-confidence PII → redact + red box
                redacted_blocks += 1
                # Black box on redacted image
                cv2.rectangle(redacted_img, (x_min, y_min), (x_max, y_max), (0, 0, 0), thickness=-1)
                # Red box on preview
                cv2.rectangle(preview_img, (x_min, y_min), (x_max, y_max), (0, 0, 255), thickness=2)
            else:
                # Low-confidence PII → flag only (no redaction)
                low_conf_pii_blocks += 1
                # Yellow box on preview
                cv2.rectangle(preview_img, (x_min, y_min), (x_max, y_max), (0, 255, 255), thickness=2)
        else:
            # Non-PII text block → green box on preview
            cv2.rectangle(preview_img, (x_min, y_min), (x_max, y_max), (0, 255, 0), thickness=1)

    stats = {
        "total_blocks": total_blocks,
        "pii_blocks": pii_blocks,
        "redacted_blocks": redacted_blocks,
        "low_conf_pii_blocks": low_conf_pii_blocks,
    }

    return redacted_img, preview_img, stats
