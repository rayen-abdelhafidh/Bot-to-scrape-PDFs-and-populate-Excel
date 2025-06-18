import requests
import logging
import json
import os

OPENROUTER_API_KEY = "..."
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODEL = "openai/gpt-3.5-turbo"

logger = logging.getLogger("openrouter")
if not logger.hasHandlers():
    logging.basicConfig(level=logging.INFO)

def extract_excel_rows_from_pdf(pdf_text):
    """
    Ask the LLM to extract all relevant rows for the Excel file as a JSON array.
    Each row should be a dict with all fields/columns for one client or record.
    """
    # Log the PDF text being sent to the AI (first 500 chars)
    logger.info(f"PDF text sent to LLM (first 500 chars): {pdf_text[:500]}")
    messages = [
        {"role": "system", "content": (
            "You are an expert at extracting structured tabular data from documents. "
            "Given the full text of a document, extract all relevant records as a JSON array. "
            "Each record should be a JSON object with these fields: Name, ID, Email, Notes. "
            "If the document contains multiple clients, return one object per client. "
            "If a field is missing, use 'N/A'. "
            "Ignore irrelevant text. "
            "Return only a valid JSON array, no explanation, no markdown, no extra text."
        )},
        {"role": "user", "content": f"Document text:\n{pdf_text}\n\nExtract all client records as a JSON array for Excel export."}
    ]
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": messages,
        "max_tokens": 1024,
        "temperature": 0
    }
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=120)
        logger.info(f"OpenRouter API status: {response.status_code}")
        if not response.ok:
            logger.error(f"OpenRouter API error: {response.text}")
            raise RuntimeError(f"OpenRouter API error: {response.status_code} {response.text}")
        result = response.json()
        content = result["choices"][0]["message"]["content"].strip()
        logger.info(f"Raw LLM response: {content}")
        # Remove markdown code block markers if present
        if content.startswith("```"):
            content = content.split("```")[1].strip()
        # Try to parse the JSON array from the response
        try:
            content_stripped = content.strip()
            json_start = content_stripped.find('[')
            json_end = content_stripped.rfind(']') + 1
            if json_start == -1 or json_end == 0:
                # Try to recover from a truncated array
                if content_stripped.startswith('['):
                    # Find the last closing curly brace
                    last_obj_end = content_stripped.rfind('}')
                    if last_obj_end != -1:
                        partial_json = content_stripped[:last_obj_end+1] + ']'
                        try:
                            data = json.loads(partial_json)
                            logger.warning("Parsed partial JSON array due to truncation.")
                            return data
                        except Exception:
                            pass
                logger.error(f"No JSON array found in LLM response: {content}")
                # Save the raw response for inspection
                with open("llm_raw_response.txt", "w", encoding="utf-8") as f:
                    f.write(content)
                raise ValueError("No JSON array found in LLM response")
            json_str = content_stripped[json_start:json_end]
            # Fallback: if the string starts with [ and ends with ], use the whole string
            if json_str.strip().startswith('[') and json_str.strip().endswith(']'):
                try:
                    data = json.loads(json_str)
                except Exception:
                    # Try to load the whole content if json_str fails
                    data = json.loads(content_stripped)
            else:
                data = json.loads(json_str)
            logger.info(f"Extracted Excel rows JSON: {data}")
            return data
        except Exception as e:
            logger.error(f"Failed to parse JSON from LLM response: {content}")
            # Save the raw response for inspection
            with open("llm_raw_response.txt", "w", encoding="utf-8") as f:
                f.write(content)
            raise
    except Exception as e:
        logger.exception("OpenRouter API call failed")
        raise
