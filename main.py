from extractor.text_pdf import extract_text_from_pdf, extract_tables_from_pdf
from extractor.ocr_pdf import extract_text_from_scanned_pdf
from utils.file_utils import is_scanned_pdf, get_pdf_files
from excel.writer import write_to_excel
from parser.parser import extract_invoice_data
from config.settings import PDF_FOLDER, OUTPUT_FILE, LOG_FILE, SUMMARY_REPORT
import logging
import os
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import warnings

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Suppress specific font warnings from PyMuPDF/fitz
warnings.filterwarnings("ignore", message="Could get FontBBox from font descriptor*")

def process_pdf(filepath):
    try:
        logging.info(f"Processing file: {filepath}")
        tables = None
        if is_scanned_pdf(filepath):
            text = extract_text_from_scanned_pdf(filepath)
        else:
            text = extract_text_from_pdf(filepath)
            tables = extract_tables_from_pdf(filepath)
        if not text or not text.strip():
            logging.warning(f"No text extracted from {filepath}")
        rows = extract_invoice_data(text, tables)
        # Add filename to each row for traceability
        for row in rows:
            row['Filename'] = os.path.basename(filepath)
            row['Error'] = row.get('Error', "")
        return rows
    except Exception as e:
        logging.error(f"Failed to process {filepath}: {e}")
        return [{"Filename": os.path.basename(filepath), "Error": str(e)}]

if __name__ == "__main__":
    all_data = []
    pdf_files = get_pdf_files(PDF_FOLDER)

    with Pool(cpu_count()) as pool:
        results = list(tqdm(pool.imap(process_pdf, pdf_files), total=len(pdf_files), desc="Processing PDFs"))

    # Flatten the list of lists into a single list of rows
    for rows in results:
        all_data.extend(rows)

    write_to_excel(all_data, OUTPUT_FILE)

    # Summary report
    total = len(all_data)
    errors = sum(1 for d in all_data if d.get('Error'))
    with open(SUMMARY_REPORT, "w", encoding="utf-8") as f:
        f.write(f"Processed: {total}\nSuccess: {total - errors}\nErrors: {errors}\n")
    logging.info(f"Processed {total} records. Success: {total - errors}, Errors: {errors}")
    with open(SUMMARY_REPORT, "w", encoding="utf-8") as f:
        f.write(f"Processed: {total}\nSuccess: {total - errors}\nErrors: {errors}\n")
    logging.info(f"Processed {total} PDFs. Success: {total - errors}, Errors: {errors}")
