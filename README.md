Handwritten OCR and PII Extraction Pipeline

This repository contains an end-to-end OCR and PII-extraction pipeline for handwritten JPEG documents, implemented as part of an AI/ML engineering assignment. The system performs image pre-processing, OCR, text cleaning, PII detection, confidence-aware redaction, and document-level reporting. A Streamlit-based web interface is also included for interactive inspection and validation.

1. Overview

The pipeline processes handwritten documents and extracts personally identifiable information (PII) using a structured workflow:

Input (JPEG) → Pre-processing → OCR → Text Cleaning → PII Detection → Smart Redaction → Reporting

The solution is designed to handle slightly tilted images, variable handwriting styles, and basic clinical or form-like handwritten notes.

2. Features
2.1 Image Pre-processing

Grayscale conversion

Contrast enhancement using CLAHE

Adaptive thresholding

Automatic deskewing to correct tilt

2.2 Handwritten OCR

EasyOCR-based text extraction

Per-block text bounding boxes

Confidence scores for each text block

2.3 Text Cleaning

Removal of artifacts

Normalization of whitespace and line structure

2.4 PII Detection

Regex-based detection of:

Email

Phone numbers

Dates

Identifiers (ID, Patient ID, MRN)

Designed to support clinic-style and general-purpose notes

2.5 Smart, Confidence-Based Redaction

Unlike basic redaction, this system selectively redacts PII only when OCR confidence exceeds a threshold (default: 0.4):

High-confidence PII → redacted in image

Low-confidence PII → flagged but not auto-redacted

This avoids incorrect masking due to uncertain OCR output and aligns with human-in-the-loop design principles.

2.6 OCR Preview Visualization

For transparency and debugging, the system produces a color-coded preview image:

Green: Non-PII text blocks

Red: High-confidence PII blocks (redacted)

Yellow: Low-confidence PII candidates

2.7 Document-Level Summary Reports

Each processed document includes a JSON report containing:

OCR confidence statistics

PII detected

Redaction statistics

Output file locations

Automatically generated warnings for edge cases (e.g., low OCR confidence, no text detected)

2.8 Streamlit Web Application

A simple UI is provided for uploading handwritten documents and visualizing:

Original vs. redacted image

OCR preview with bounding boxes

Extracted text

Detected PII

Confidence-based warnings

Full JSON report

3. Repository Structure
handwritten-ocr-pii/
│
├─ samples/                         # Handwritten JPEG inputs
├─ outputs/                         # Extracted text, redacted files, reports
│
├─ src/
│   ├─ preprocessing.py             # Pre-processing pipeline
│   ├─ ocr_module.py                # EasyOCR wrapper
│   ├─ text_cleaning.py             # Cleanup utilities
│   ├─ pii_detection.py             # Regex-based PII detector
│   ├─ redaction.py                 # Smart redaction + preview
│   └─ pipeline.py                  # End-to-end orchestrator
│
├─ main.py                          # Command-line driver
├─ streamlit_app.py                 # Interactive UI
├─ requirements.txt
└─ README.md

4. Installation
git clone <repo-url>
cd handwritten-ocr-pii

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt

5. Usage (Command Line)
Process all samples
python main.py

Process a single image
python main.py --input samples/1.jpeg

Adjust redaction confidence threshold
python main.py --input samples/1.jpeg --conf-threshold 0.6

Outputs generated per file

<name>_text.txt – cleaned OCR text

<name>_pii.json – PII detection results

<name>_redacted_text.txt – text with PII masked

<name>_redacted.jpg – image with PII masked

<name>_ocr_preview.jpg – visualization of detected text blocks

<name>_report.json – consolidated analysis and warnings

6. Streamlit Web Interface

To launch the web UI:

streamlit run streamlit_app.py


The interface supports file uploads and displays:

Original image

Redacted output

OCR preview with bounding boxes

Extracted text

Detected PII elements

Confidence analysis

Full JSON report

Example UI Screenshots

Replace the placeholders below with uploaded GitHub image links:

Original vs Redacted Image

OCR Preview (Color-Coded Bounding Boxes)

Extracted Text and PII Detection

Summary Report and Warnings

7. Design Choices and Rationale

EasyOCR is used due to its robustness on non-uniform handwriting compared to strict rule-based OCR like Tesseract.

Confidence-based redaction prevents over-redaction and ensures reliability in ambiguous handwriting scenarios.

Report generation and warnings are included to simulate production-grade auditability.

The Streamlit UI provides transparency and demonstrates real-world user interaction and model interpretability.

8. Limitations and Possible Extensions

Handwriting quality and photograph clarity significantly affect OCR reliability.

Regex rules may require customization for specific forms or clinical workflows.

Additional NER models (spaCy, transformers) could enhance name detection.

Image enhancement techniques such as denoising and morphological operations can be explored.

9. License

This project is intended for evaluation purposes and educational demonstration only.
