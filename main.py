# main.py
from pathlib import Path
import argparse

from src.pipeline import SAMPLES_DIR, process_image, DEFAULT_CONF_THRESHOLD


def main():
    parser = argparse.ArgumentParser(
        description="OCR + PII extraction pipeline for handwritten JPEG documents"
    )
    parser.add_argument(
        "--input",
        type=str,
        help="Path to a single image. If not provided, all JPEGs in samples/ are processed.",
    )
    parser.add_argument(
        "--conf-threshold",
        type=float,
        default=DEFAULT_CONF_THRESHOLD,
        help="Confidence threshold (0–1) for deciding whether to redact a PII block in the image.",
    )
    args = parser.parse_args()

    if args.input:
        files = [Path(args.input)]
    else:
        files = list(SAMPLES_DIR.glob("*.jpg")) + list(SAMPLES_DIR.glob("*.jpeg"))
        if not files:
            print("No JPEG files found in samples/ and no input path provided.")
            return

    for img_path in files:
        print(f"\nProcessing {img_path} with conf_threshold={args.conf_threshold} ...")
        result = process_image(img_path, conf_threshold=args.conf_threshold)

        print(f"  → Text:              {result['text_path']}")
        print(f"  → PII JSON:          {result['pii_path']}")
        print(f"  → Redacted text:     {result['redacted_text_path']}")
        print(f"  → Redacted image:    {result['redacted_image_path']}")
        print(f"  → OCR preview image: {result['preview_image_path']}")
        print(f"  → Summary report:    {result['report_path']}")

        # Show quick warning summary in console
        report = result["report"]
        if report.get("warnings"):
            print("  Warnings:")
            for w in report["warnings"]:
                print(f"    - {w}")


if __name__ == "__main__":
    main()
