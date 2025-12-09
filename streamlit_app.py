import json
import tempfile
from pathlib import Path

import streamlit as st
from PIL import Image

from src.pipeline import process_image, DEFAULT_CONF_THRESHOLD


def main():
    st.set_page_config(page_title="Handwritten OCR + PII Redactor", layout="wide")
    st.title("📝 Handwritten OCR + PII Extraction Demo")

    st.markdown(
        "Upload a handwritten note or clinic-style form (JPEG/PNG). "
        "The app will run pre-processing → OCR → PII detection → smart redaction."
    )

    uploaded_file = st.file_uploader(
        "Upload an image file",
        type=["jpg", "jpeg", "png"],
    )

    conf_threshold = st.slider(
        "Confidence threshold for redacting PII blocks in the image",
        min_value=0.1,
        max_value=0.9,
        step=0.05,
        value=DEFAULT_CONF_THRESHOLD,
    )

    if uploaded_file is not None:
        # Save uploaded file to a temporary path
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = Path(tmp.name)

        st.info("Running OCR + PII pipeline...")
        result = process_image(tmp_path, conf_threshold=conf_threshold)
        report = result["report"]

        col1, col2 = st.columns(2)

        # Left: original vs redacted/preview
        with col1:
            st.subheader("Original Image")
            uploaded_file.seek(0)
            st.image(uploaded_file, use_column_width=True)

            st.subheader("Redacted Image (High-Confidence PII)")
            red_img = Image.open(result["redacted_image_path"])
            st.image(red_img, use_column_width=True)

        with col2:
            st.subheader("OCR Preview (Color-Coded)")
            preview_img = Image.open(result["preview_image_path"])
            st.image(preview_img, use_column_width=True)

            st.subheader("Extracted Text")
            text_content = Path(result["text_path"]).read_text(encoding="utf-8")
            st.text_area("OCR Text", value=text_content, height=250)

        st.subheader("Detected PII")
        st.json(report.get("pii_detected", {}))

        st.subheader("Summary & Warnings")
        st.markdown(
            f"- **Total OCR blocks**: {report['ocr']['blocks_total']}\n"
            f"- **Average confidence**: {report['ocr']['confidence']['avg']:.2f}"
        )

        if report.get("warnings"):
            st.warning("\n".join(f"- {w}" for w in report["warnings"]))
        else:
            st.success("No major issues detected for this document.")

        with st.expander("Raw summary report (JSON)"):
            st.code(json.dumps(report, indent=2), language="json")


if __name__ == "__main__":
    main()
