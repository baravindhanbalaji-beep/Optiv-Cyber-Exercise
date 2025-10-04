import os
import re
from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
from ai import file_description_and_keyfindings

# ------------------- PII Masking -------------------
pii_patterns = {
    "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
    "PHONE": r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}\b",
    "IP": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
    "NAME_TITLE": r"\b(?:Mr|Mrs|Ms|Dr)\.?\s+[A-Z][a-z]+\b",
    "TOKEN_SERIAL": r'\bHT-\d+-[A-Z]+\b', 
}

def mask_pii(text: str) -> str:
    """Replaces PII patterns in text with placeholders."""
    if not text:
        return text
    masked_text = text
    for label, pattern in pii_patterns.items():
        masked_text = re.sub(pattern, f"<{label}>", masked_text)
    return masked_text

# ------------------- PDF Extraction -------------------
def extract_text_from_pdf(file_path: str) -> str:
    """Extracts text from a PDF using PyPDF (for selectable text) and OCR (for images)."""
    full_text = ""

    # 1. Extract selectable text with PyPDF
    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text with PyPDF: {e}")

    # 2. OCR for image-based text
    try:
        poppler_path = r"C:\Program Files (x86)\poppler-25.07.0\Library\bin"  
        pages = convert_from_path(file_path, poppler_path=poppler_path, dpi=300)
        for page in pages:
            ocr_text = pytesseract.image_to_string(page)
            if ocr_text.strip():
                full_text += "\n" + ocr_text
    except Exception as e:
        print(f"Error extracting text via OCR: {e}")

    return full_text.strip()

# ------------------- Main -------------------
def pdf_main(file_path: str):
    text_content = extract_text_from_pdf(file_path)
    if text_content:
        # Mask PII
        text_content_masked = mask_pii(text_content)

        prompt = f"""
        Analyze the following extracted PDF text content. Generate a descriptive 
        title and a file caption of about 30 words that summarizes the document's 
        content, focusing on the security/IT-related context.

        Extracted PDF Content:
        ---
        {text_content_masked}
        """
        file_description,key_findings = file_description_and_keyfindings(prompt)
        return file_description,key_findings
    else:
        print("Failed to extract text from the PDF file.")


