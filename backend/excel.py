from ai import file_description_and_keyfindings
import os
import pandas as pd
import re
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

pii_patterns = {
    "EMPLOYEE_ID": r'\bEMP\d+\b',                        
    "EMAIL": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
    "TOKEN_SERIAL": r'\bHT-\d+-[A-Z]+\b',                
    "FULL_NAME": r'\b(?:Mr|Mrs|Ms|Dr)\.?\s+[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b|\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)+\b',
    "CREDIT_CARD": r"\b(?:\d[ -]*?){13,16}\b",
}

def mask_pii(text: str) -> str:
    if not isinstance(text,str):
        text = str(text) if pd.notna(text) else ""
    modified_text = text
    for label, pattern in pii_patterns.items():
        modified_text = re.sub(pattern, f"<{label}>", modified_text, flags=re.IGNORECASE)
    return modified_text

def process_excel_file(file_path: str) -> str:
    """Read Excel, mask PII, save masked Excel as 'clean.xlsx', return file path."""
    try:
        df = pd.read_excel(file_path, engine="openpyxl", dtype=str)
        df_masked = df.applymap(mask_pii)
        '''
        output_file = "clean.xlsx"
        df_masked.to_excel(output_file, index=False, engine="openpyxl")
        print(f"Masked file saved as: {output_file}")
        return output_file
        '''
        cleansed_text = df_masked.to_string(index=False, header=True)
        return cleansed_text
    except Exception as e:
        print(f"Error processing file: {e}")
        return ""

def excel_main(file_path:str):
    cleansed_text = process_excel_file(file_path)
    if cleansed_text:
        prompt = f"""
        Analyze the following cleansed spreadsheet data (Excel file). Generate a descriptive 
        title and a file caption of about 30 words that summarizes the data's content, 
        focusing on the security/IT-related context (e.g., Firewall rules, User Access Log, 
        Token Issuance, etc.).
        Cleansed Spreadsheet Content:
        ---
        {cleansed_text}
        """
        file_description,key_findings = file_description_and_keyfindings(prompt)
        return file_description,key_findings
    else:
        return "Failed to process the Excel file."


