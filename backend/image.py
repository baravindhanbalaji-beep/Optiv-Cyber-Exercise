import os
import google.generativeai as genai
import dotenv
from PIL import Image
import io

dotenv.load_dotenv()

def image_file_description_and_keyfindings(image_path: str) -> str:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-2.5-flash')
    image = Image.open(image_path)
    description_prompt = f"""
    You are a visual summarizer.

Look at the image and write a short, clear, and factual description in **exactly two parts**:

1. **Title:** 2–4 words only, describing the main object or system.
2. **Body:** 1–2 lines that summarize what is happening or shown. 
   - Be simple and factual (e.g., "A person is holding an access card against a wall-mounted reader.").
   - Do NOT describe colors, lighting, materials, or text positioning.
   - Do NOT include sensory or interpretive words like 'appears', 'seems', 'shows', or 'likely'.


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

"""

    response = model.generate_content([description_prompt,image])
    
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
    
    return file_description,final_findings

