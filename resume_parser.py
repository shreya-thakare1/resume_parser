import sys
sys.stdout.reconfigure(encoding='utf-8')
import re
import pdfplumber
import spacy

nlp = spacy.load("en_core_web_sm")


# -------- PDF TEXT EXTRACT --------
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text


# -------- REGEX SECTION EXTRACT --------
def extract_section(text, section_name):

    pattern = rf"""
        ^\s*{section_name}\s*$
        (.*?)
        (?=^\s*[A-Z][A-Za-z ]+\s*$|\Z)
    """

    match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE)
    return match.group(1).strip() if match else "Not found"


# -------- NER CHECK (spaCy Validation) --------
def ner_process(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


# -------- PARSER --------
def parse_resume(file_path):

    text = extract_text_from_pdf(file_path)

    skills = extract_section(text, "skills")
    education = extract_section(text, "education")
    experience = extract_section(text, "experience")

    # run NLP entity detection
    ner_entities = ner_process(text)

    return {
        "Skills": skills,
        "Education": education,
        "Experience": experience,
        "Detected Entities": ner_entities[:10]   # show first 10 only
    }


# -------- RUN --------
result = parse_resume("Shreya_Thakare_YCCE_7th_Sem.pdf")

for key, value in result.items():
    print(f"\n----- {key} -----\n{value}")
