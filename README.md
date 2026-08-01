#Live Link

https://contactless-fingerprint-qc-4jbkbuyoxhsvnurmxhrf67.streamlit.app/

# Contactless Fingerprint Quality Assessment

## Project Overview

This project implements a **Contactless Fingerprint Quality Assessment** pipeline for mobile-based fingerprint authentication.

The system evaluates the quality of a fingerprint image before biometric processing by analyzing multiple image quality metrics and generating a composite quality score. It also provides user guidance to improve image capture quality.

---

## Features

- Blur Detection using Laplacian Variance
- Brightness Analysis
- Glare Detection
- ROI (Region of Interest) Completeness
- Ridge Clarity using Gabor Filter
- Composite Quality Score (0–100)
- Pass/Reject Decision
- User Guidance for Image Retake
- Streamlit Web Interface
- Batch Dataset Evaluation
- CSV Result Generation

---

## Project Structure

```text
contactless-fingerprint-qc/
│
├── quality_assessment.py
├── quality_app.py
├── test_quality.py
├── prepare_dataset.py
├── quality_results.csv
├── report.pdf
├── requirements.txt
├── README.md
├── screenshots/
│   ├── good/
│   ├── blurry/
│   ├── dark/
│   └── glare/
└── test_dataset/
    ├── good/
    ├── blurry/
    ├── dark/
    └── glare/
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/contactless-fingerprint-qc.git
cd contactless-fingerprint-qc
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Run the Streamlit Application

```bash
streamlit run quality_app.py
```

The application allows users to upload a fingerprint image and receive:

- Composite Quality Score
- Pass/Reject Decision
- Individual Quality Metrics
- Capture Guidance

---

## Run Batch Evaluation

```bash
python test_quality.py
```

Evaluation results are automatically saved to:

```text
quality_results.csv
```

---

## Quality Metrics

| Metric | Method |
|---------|--------|
| Blur | Laplacian Variance |
| Brightness | Mean Grayscale Intensity |
| Glare | Bright Pixel Analysis |
| ROI Completeness | Threshold-Based Finger Segmentation |
| Ridge Clarity | Gabor Filter Response |

---

## Composite Quality Score

The final quality score combines all five quality metrics into a score ranging from **0 to 100**.

### Decision Rule

- **Score ≥ 60** → Accept
- **Score < 60** → Reject

The final decision also considers individual quality checks such as blur, brightness, glare, ROI completeness, and ridge clarity.

---

## Dataset

A subset of the **SOCOFing (Sokoto Coventry Fingerprint Dataset)** was used for evaluation.

The evaluation dataset contains four categories:

- Good fingerprint images
- Blurry fingerprint images
- Dark fingerprint images
- Glare-affected fingerprint images

Blur, dark, and glare images were generated programmatically from the original fingerprint images for evaluation purposes.

---

## Technologies Used

- Python
- OpenCV
- NumPy
- Pandas
- Streamlit

---

## Author

**Surla Vagesh Kumar**
