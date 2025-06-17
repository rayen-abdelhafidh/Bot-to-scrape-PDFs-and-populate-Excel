import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '..', 'pdfs'))
OUTPUT_FILE = os.path.abspath(os.path.join(BASE_DIR, '..', 'output', 'output.xlsx'))
LOG_FILE = os.path.abspath(os.path.join(BASE_DIR, '..', 'logs', 'extractor.log'))
FIELDS_CONFIG = os.path.abspath(os.path.join(BASE_DIR, 'fields.yaml'))
SUMMARY_REPORT = os.path.abspath(os.path.join(BASE_DIR, '..', 'output', 'summary.txt'))
OCR_LANG = 'eng'  # Add this for multi-language OCR

# OpenRouter API is now used for QA and summarization (see utils/hf_qa.py)
# OPENROUTER_API_KEY is hardcoded in utils/hf_qa.py

# Excel output configuration for best compatibility
EXCEL_ENGINE = "openpyxl"  # Ensures compatibility and formatting
EXCEL_SHEET_NAME = "Invoices"  # Custom sheet name for clarity