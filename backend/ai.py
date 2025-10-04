import os
import google.generativeai as genai
import dotenv

dotenv.load_dotenv() 

def file_description_and_keyfindings(prompt: str) -> str:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')

    description_prompt = f"""
    You are an expert descriptive analyst. Your task is to provide a brief, concise, and highly visual description of an object or scenario.

The description must adhere strictly to the following format:
1.  **Title:** A one-to-three-word title for the object/system.
2.  **Body:** A description, spanning 2-4 short, separate lines, focusing only on visually verifiable details. Do not interpret or analyze the function.
Do NOT include any headings like 'Title' or 'Body'.
---
**Examples to Follow:**

Access Card Reader

A person is holding an access card against a
card reader mounted near a door labeled "211
IDF/Electrical." The card reader has a light
indicator.

Biometric Attendance/Access System

A wall-mounted electronic biometric device
with fingerprint scanning, keypad, and display
screen showing time.

Visitors Logbook

A paper-based visitor logbook where
individuals manually write their name, reason
for visit, time in/out, and provide a signature.
Two entries are already filled in.

---
**New Item to Describe:**
{prompt}
"""

    response = model.generate_content(description_prompt)
    
    file_description = response.text 

    prompt = f"""
    Analyze the following file description and extract the key findings. The findings should summarize the system's purpose, functionality, advantages, and potential vulnerabilities. Follow the format of the examples provided.
    Don't include 'Key Findings' heading.
    ---
    **Example 1:**

    **File Description:**
    Access Card Reader

    A person is holding an access card against a card reader mounted near a door labeled "211 IDF/Electrical." The card reader has a light indicator.

    **Key Findings:**
    - Digital access control system using ID/employee cards.
    - Automates entry tracking by time-stamping when the card is swiped.
    - Dependent on card validity and system integrity (e.g., cards can be lost or borrowed).

    ---
    **Example 2:**

    **File Description:**
    Biometric Attendance/Access System

    A wall-mounted electronic biometric device with fingerprint scanning, keypad, and display screen showing time.

    **Key Findings:**
    - Uses biometric authentication (fingerprint) for high security.
    - Eliminates risks of proxy entry or shared access (unlike cards or logbooks).
    - Provides accurate, automated attendance and access logs.
    - Suitable for organizations seeking reliable and tamper-proof entry systems.

    ---
    **Example 3:**

    **File Description:**
    Visitors Logbook

    A paper-based visitor logbook where individuals manually write their name, reason for visit, time in/out, and provide a signature. Two entries are already filled in.

    **Key Findings:**
    - Manual entry system, dependent on handwriting.
    - Prone to errors, illegible writing, and falsification.
    - No automatic time tracking—relies on honesty and accuracy of the visitor.

    ---
    **New Request:**

    **File Description:**
    {file_description}

    **Key Findings:**
    """
    
    response = model.generate_content(prompt)
    raw_findings = response.text.strip()
    cleaned_findings_text = raw_findings.replace('\n-', '\n').replace('- ', '\n').replace('\n\n', '\n')
    findings_list = [
        item.strip()
        for item in cleaned_findings_text.split('\n')
        if item.strip()
    ]
    final_findings = "\n".join(f"- {finding}" for finding in findings_list)
    if not file_description:
        file_description = "No description generated."
    if not final_findings:
        final_findings = "No key findings generated."
    print("DEBUG: file_description =", file_description)
    print("DEBUG: final_findings =", final_findings)
    return file_description,final_findings


