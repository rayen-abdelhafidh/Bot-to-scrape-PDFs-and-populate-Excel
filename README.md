# 📄 PDF Scraper & Excel Populator

A Python tool to **extract structured data from PDFs** (including scanned documents), use AI to recognize and extract fields, and write the results to a smartly sorted Excel file.

---

## ✨ Features

- 📝 Extracts text from both native and scanned PDFs (OCR)
- 🤖 Uses OpenRouter AI (GPT) for robust data extraction (e.g., client info, invoice fields)
- 📊 Outputs results to a clean, sorted Excel file
- 👥 Handles multiple clients/records per PDF
- 🪵 Logs errors and raw AI responses for easy debugging

---

## 🚀 Quick Start

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/pdf-scraper-excel.git
cd pdf-scraper-excel
```

### 2. Install dependencies

```sh
pip install -r requirements.txt
```

### 3. Install Tesseract & Poppler

- **Windows:**  
  Download and install [Tesseract](https://github.com/tesseract-ocr/tesseract/wiki) and [Poppler](http://blog.alivate.com.au/poppler-windows/).
- **Linux:**  
  ```sh
  sudo apt-get install tesseract-ocr poppler-utils
  ```

### 4. Configure your API key

- The OpenRouter API key is set in `utils/hf_qa.py`.  
  Replace it with your own if needed.

### 5. Add your PDF files

- Place your PDFs in the `pdfs/` directory.

---

## 🛠️ Usage

Run the main script:

```sh
python main.py
```

- Extracted data will be written to: `output/output.xlsx`
- A summary report will be written to: `output/summary.txt`
- Logs and raw AI responses (if errors) are saved in the `logs/` directory

---

## ⚙️ Configuration

- **Excel output:**  
  Change sheet name or engine in `config/settings.py`
- **Field extraction patterns:**  
  Edit `config/fields.yaml` to adjust regex patterns for your documents
- **OCR language:**  
  Set `OCR_LANG` in `config/settings.py` for multi-language support

---

## 🐞 Troubleshooting

- If the Excel file is empty or missing data:
  - Check `logs/extractor.log` and `llm_raw_response.txt` for errors or incomplete AI responses
  - Make sure your OpenRouter API key is valid and you have internet access
  - For large PDFs, the AI may truncate output; try splitting large PDFs

---

## 📄 License

MIT License

---

> **Contributions welcome!**  
> Feel free to open issues or submit pull requests.
