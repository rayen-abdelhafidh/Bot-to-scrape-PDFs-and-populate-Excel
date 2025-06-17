from pdf2image import convert_from_path
import pytesseract
import tempfile
import os
import cv2
import numpy as np
from config.settings import OCR_LANG
import logging

logger = logging.getLogger("extractor.ocr_pdf")

def preprocess_image_cv2(pil_img):
    img = np.array(pil_img)
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text_from_scanned_pdf(path):
    try:
        with tempfile.TemporaryDirectory() as tempdir:
            images = convert_from_path(path, output_folder=tempdir)
            text = ""
            for i, img in enumerate(images):
                pre_img = preprocess_image_cv2(img)
                page_text = pytesseract.image_to_string(pre_img, lang=OCR_LANG)
                logger.info(f"OCR page {i+1} text (first 200 chars): {page_text[:200]}")
                text += page_text + "\n"
            return text
    except Exception as e:
        logger.error(f"Failed to OCR {path}: {e}")
        return ""

# Placeholder for cloud OCR integration
def extract_text_cloud_ocr(image):
    # Implement cloud OCR API call here
    return ""
