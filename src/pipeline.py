# src/pipeline.py
from pathlib import Path
import json
import cv2
from typing import Dict, Any, List

from .preprocessing import preprocess
from .ocr_module import run_ocr
from .text_cleaning import clean_text
from .pii_detection import detect_pii
from .redaction import redact_text, analyze_and_redact_image

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLES_DIR = BASE_DIR / "samples"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

DEFAULT_CONF_THRESHOLD = 0.4


def _compute_confidence_stats(blocks: List[Dict[str, Any]]) -> Dict[str, float]:
    if not blocks:
        return {"avg": 0.0, "min": 0.0, "max": 0.0}

    scores = [float(b.get("score", 0.0)) for b in blocks]
    avg = sum(scores) / len(scores)
    return {"avg": avg, "min": min(scores), "max": max(scores)}


def process_image(image_path: Path, conf_threshold: float = DEFAULT_CONF_THRESHOLD) -> Dict[str, Any]:
    name = image_path.stem

    # 1) Preprocess
    original, processed = preprocess(str(image_path))

    # 2) OCR
    ocr_result = run_ocr(processed)
    raw_text = ocr_result["text"]
    blocks = ocr_result["blocks"]

    # 3) Clean text
    cleaned_text = clean_text(raw_text)

    # 4) Detect PII
    pii = detect_pii(cleaned_text)

    # 5) Redact text
    redacted_txt = redact_text(cleaned_text, pii)

    # 6) Smart image redaction + preview
    redacted_img, preview_img, redaction_stats = analyze_and_redact_image(
        original_img=original,
        blocks=blocks,
        pii=pii,
        conf_threshold=conf_threshold,
    )

    # 7) Confidence stats
    conf_stats = _compute_confidence_stats(blocks)

    # 8) Warnings / edge-case documentation
    warnings: List[str] = []
    if not blocks:
        warnings.append("No text blocks detected by OCR. Image may be too noisy, blank, or unreadable.")
    elif conf_stats["avg"] < 0.4:
        warnings.append(
            f"Low average OCR confidence ({conf_stats['avg']:.2f}). "
            f"Handwriting quality, lighting, or tilt may be affecting recognition."
        )

    if not any(pii.values()):
        warnings.append("No PII detected in this document given the current regex rules.")

    if redaction_stats["low_conf_pii_blocks"] > 0:
        warnings.append(
            f"{redaction_stats['low_conf_pii_blocks']} text blocks contained possible PII "
            f"but had low OCR confidence and were not auto-redacted in the image."
        )

    # 9) Save outputs
    text_path = OUTPUT_DIR / f"{name}_text.txt"
    red_text_path = OUTPUT_DIR / f"{name}_redacted_text.txt"
    pii_path = OUTPUT_DIR / f"{name}_pii.json"
    red_img_path = OUTPUT_DIR / f"{name}_redacted.jpg"
    preview_img_path = OUTPUT_DIR / f"{name}_ocr_preview.jpg"
    report_path = OUTPUT_DIR / f"{name}_report.json"

    text_path.write_text(cleaned_text, encoding="utf-8")
    red_text_path.write_text(redacted_txt, encoding="utf-8")

    with open(pii_path, "w", encoding="utf-8") as f:
        json.dump(pii, f, indent=2, ensure_ascii=False)

    cv2.imwrite(str(red_img_path), redacted_img)
    cv2.imwrite(str(preview_img_path), preview_img)

    # 10) Summary report JSON
    report: Dict[str, Any] = {
        "document_name": image_path.name,
        "confidence_threshold_for_redaction": conf_threshold,
        "ocr": {
            "blocks_total": len(blocks),
            "confidence": conf_stats,  # avg / min / max
        },
        "pii_detected": pii,
        "redaction_stats": redaction_stats,
        "output_paths": {
            "clean_text": str(text_path),
            "pii_json": str(pii_path),
            "redacted_text": str(red_text_path),
            "redacted_image": str(red_img_path),
            "ocr_preview_image": str(preview_img_path),
        },
        "warnings": warnings,
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Return everything useful to caller (CLI or Streamlit)
    result = {
        "text_path": text_path,
        "pii_path": pii_path,
        "redacted_text_path": red_text_path,
        "redacted_image_path": red_img_path,
        "preview_image_path": preview_img_path,
        "report_path": report_path,
        "report": report,
    }
    return result
