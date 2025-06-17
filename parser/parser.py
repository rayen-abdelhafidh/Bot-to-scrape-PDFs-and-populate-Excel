import re
from dateutil import parser as dateparser
import yaml
from config.settings import FIELDS_CONFIG
import spacy
from utils.hf_qa import extract_excel_rows_from_pdf
import logging

nlp = spacy.load("en_core_web_sm")
logger = logging.getLogger("parser")

def load_fields():
    with open(FIELDS_CONFIG, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

FIELDS = load_fields()

def extract_invoice_data(text, tables=None):
    if not text or not text.strip():
        logger.error("No text extracted from PDF for extraction.")
        return []
    logger.info(f"Extracted PDF text (first 500 chars): {text[:500]}")
    try:
        # Use the LLM to extract all rows for Excel as a list of dicts
        rows = extract_excel_rows_from_pdf(text)
        return rows
    except Exception as e:
        logger.error(f"LLM extraction failed: {e}")
        return [{"Error": f"LLM extraction failed: {e}"}]

def extract_field(text, pattern, default=None):
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else default

def extract_date(text, doc=None):
    # Try spaCy NER first
    if doc:
        for ent in doc.ents:
            if ent.label_ == "DATE":
                try:
                    return str(dateparser.parse(ent.text).date())
                except:
                    continue
    date_matches = re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b', text)
    for date_str in date_matches:
        try:
            return str(dateparser.parse(date_str).date())
        except:
            continue
    return "N/A"

def extract_client_name(doc, text, default):
    # Try spaCy NER for PERSON/ORG
    for ent in doc.ents:
        if ent.label_ in ("PERSON", "ORG"):
            return ent.text
    return default

def extract_total(doc, text, default):
    # Try spaCy NER for MONEY
    for ent in doc.ents:
        if ent.label_ == "MONEY":
            return ent.text
    # fallback to regex
    return extract_field(text, r'Total\s*[:]*\s*\$?(\d+[.,]\d+)', default)

def extract_from_tables(tables):
    # Example: look for "Total" in tables
    result = {}
    for df in tables:
        for col in df.columns:
            for idx, val in enumerate(df[col]):
                if isinstance(val, str) and "total" in val.lower():
                    try:
                        result["Total (table)"] = df.iloc[idx, col+1]
                    except:
                        continue
    return result

def extract_fields(text, fields_config):
    result = {}
    for field in fields_config['fields']:
        if 'pattern' in field:
            import re
            match = re.search(field['pattern'], text, re.IGNORECASE)
            if match:
                value = match.group(2).strip() if match.lastindex else match.group(1).strip()
                logger.info(f"Extracted {field['name']}: {value}")
                result[field['name']] = value
            else:
                logger.warning(f"Could not extract {field['name']}, using default: {field.get('default', '')}")
                result[field['name']] = field.get('default', '')
    return result