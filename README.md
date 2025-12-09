## Handwritten OCR and PII Extraction Pipeline

This repository contains an end-to-end OCR and PII-extraction pipeline for handwritten JPEG documents, implemented as part of an AI/ML engineering assignment. The system performs image pre-processing, OCR, text cleaning, PII detection, confidence-aware redaction, and document-level reporting. A Streamlit-based web interface is also included for interactive inspection and validation.

**1. Overview**

The pipeline processes handwritten documents and extracts personally identifiable information (PII) using a structured workflow:
```text
Input (JPEG) → Pre-processing → OCR → Text Cleaning → PII Detection → Smart Redaction → Reporting
```
The solution is designed to handle slightly tilted images, variable handwriting styles, and basic clinical or form-like handwritten notes.

**2. Features**
**2.1 Image Pre-processing**
```text
Grayscale conversion

Contrast enhancement using CLAHE

Adaptive thresholding

Automatic deskewing to correct tilt
```
**2.2 Handwritten OCR**
```text
EasyOCR-based text extraction

Per-block text bounding boxes

Confidence scores for each text block
```
**2.3 Text Cleaning**
```text
Removal of OCR artifacts

Normalization of whitespace and line structure
```
**2.4 PII Detection**

**Regex-based detection of:**
```text
Email

Phone numbers

Dates

Identifiers (ID, Patient ID, MRN)

Designed to support clinic-style and general-purpose handwritten notes.
```
**2.5 Smart, Confidence-Based Redaction**
```text
Redaction occurs only when OCR confidence exceeds a configurable threshold (default: 0.4):

High-confidence PII → Automatically redacted in image

Low-confidence PII → Flagged but not redacted

This avoids incorrect masking due to ambiguous handwriting and aligns with human-in-the-loop safety principles.
```
**2.6 OCR Preview Visualization**

A color-coded preview image is generated to visualize OCR block classifications:
```text
Green: Non-PII text blocks

Red: High-confidence PII (redacted)

Yellow: Low-confidence PII candidates
```
**2.7 Document-Level Summary Reports**

Each processed document includes a structured JSON report containing:

OCR confidence statistics

PII detected

Redaction statistics

Output file locations

Automatically generated warnings (e.g., low OCR confidence)

**2.8 Streamlit Web Application**
```text
A simple web interface is provided for uploading handwritten documents and visualizing:

Original vs. redacted image

OCR preview with bounding boxes

Extracted text

Detected PII

Confidence-based alerts

Full summary report
```
**3. Repository Structure**
```text
handwritten-ocr-pii/
│
├── samples/                       # Handwritten JPEG inputs
├── outputs/                       # Extracted text, redacted files, reports
│
├── src/
│   ├── preprocessing.py           # Pre-processing pipeline
│   ├── ocr_module.py              # EasyOCR wrapper
│   ├── text_cleaning.py           # Cleanup utilities
│   ├── pii_detection.py           # Regex-based PII detector
│   ├── redaction.py               # Smart redaction + preview
│   └── pipeline.py                # End-to-end orchestrator
│
├── main.py                        # Command-line driver
├── streamlit_app.py               # Interactive UI
├── requirements.txt
└── README.md
```
**4. Installation**
```text
git clone <repo-url>
cd handwritten-ocr-pii

python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```
**5. Usage (Command Line)**

Process all samples
```text
python main.py
```
Process a single image
```text
python main.py --input samples/1.jpeg
```
Adjust redaction confidence threshold
```text
python main.py --input samples/1.jpeg --conf-threshold 0.6
```
Outputs generated per file
```text
<name>_text.txt – Cleaned OCR text

<name>_pii.json – PII detection results

<name>_redacted_text.txt – Text with PII masked

<name>_redacted.jpg – Image with sensitive sections redacted

<name>_ocr_preview.jpg – Visual highlight of OCR blocks

<name>_report.json – Consolidated analysis and warnings
```
**6. Streamlit Web Interface**
**Launch the UI:**
```text
streamlit run streamlit_app.py
```

The interface supports:
```text
Viewing original and redacted images

OCR preview visualization

Extracted text exploration

PII summary

Redaction behavior based on confidence

Structured JSON report
```
**Example UI Screenshots**
<img width="1919" height="1199" alt="image" src="https://github.com/user-attachments/assets/b42d09be-69c4-4af2-9118-f435b6725453" />
<img width="1751" height="892" alt="image" src="https://github.com/user-attachments/assets/ea1d63d2-913f-4997-835c-d4d52053a485" />
<img width="896" height="836" alt="image" src="https://github.com/user-attachments/assets/fc154531-530f-4708-9129-ef598bd106b5" />



**Original vs. Redacted Image**

**OCR Preview (Color-Coded Bounding Boxes)**

**Extracted Text and PII Detection**

**Summary Report and Warnings**

**7. Design Choices and Rationale**

EasyOCR was chosen for its robustness on handwritten text compared to rule-based OCR engines such as Tesseract.

Confidence-aware redaction allows safer handling by avoiding false positives.

JSON reporting improves transparency, auditability, and debugging.

Streamlit UI provides a clear visualization layer for both technical reviewers and non-technical users.

**8. Limitations and Possible Extensions**

Handwriting style, lighting, and image noise significantly affect OCR accuracy.

Regex rules may require modification for domain-specific forms.

Advanced NER models (spaCy, transformer models) could improve name and ID detection.

Additional image enhancement (denoising, morphological filters) may further improve OCR quality.


