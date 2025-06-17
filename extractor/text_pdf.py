import fitz
import camelot
import logging

logger = logging.getLogger("extractor.text_pdf")

def extract_text_from_pdf(path):
    try:
        with fitz.open(path) as doc:
            text = "\n".join([page.get_text("text") for page in doc])
            logger.info(f"Extracted text from {path} (first 500 chars): {text[:500]}")
            return text
    except Exception as e:
        logger.error(f"Failed to extract text from {path}: {e}")
        return ""

def extract_tables_from_pdf(path):
    try:
        tables = camelot.read_pdf(path, pages='all', flavor='stream')
        logger.info(f"Extracted {len(tables)} tables from {path}")
        return [t.df for t in tables]
    except Exception as e:
        logger.error(f"Failed to extract tables from {path}: {e}")
        return []
