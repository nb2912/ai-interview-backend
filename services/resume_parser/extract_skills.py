# resume_parser/extract_skills.py

import re
import spacy
import json
from typing import List

# Load the spaCy English language model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading en_core_web_sm language model for spaCy...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load skills from the JSON file
try:
    with open("resume_parser/skill_keywords.json", 'r') as f:
        skill_data = json.load(f)
        TECHNICAL_SKILLS = skill_data.get("technical_skills", [])
        SOFT_SKILLS = skill_data.get("soft_skills", [])
        # You can access other categories as needed
except FileNotFoundError:
    print("Error: skill_keywords.json not found in resume_parser directory.")
    TECHNICAL_SKILLS = []
    SOFT_SKILLS = []
except json.JSONDecodeError:
    print("Error: Could not decode JSON from skill_keywords.json.")
    TECHNICAL_SKILLS = []
    SOFT_SKILLS = []

def extract_skills(text: str) -> List[str]:
    """
    Extracts technical and soft skills from the given text using keywords.

    Args:
        text: The text extracted from the resume.

    Returns:
        A list of identified skills.
    """
    found_skills = set()
    all_skills = [skill.lower() for skill in TECHNICAL_SKILLS + SOFT_SKILLS]

    # 1. Keyword matching
    for skill in TECHNICAL_SKILLS + SOFT_SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            found_skills.add(skill)

    # 2. Using spaCy for potential noun/proper noun skills (less strict matching)
    doc = nlp(text)
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"]:
            if token.text.lower() in all_skills:
                found_skills.add(token.text)
        elif token.dep_ in ["compound"] and token.head.pos_ in ["NOUN", "PROPN"]:
            compound_skill = token.text + " " + token.head.text
            if compound_skill.lower() in all_skills:
                found_skills.add(compound_skill)

    return sorted(list(found_skills))

if __name__ == "__main__":
    resume_text = """
    Experienced software engineer with expertise in Python, Java, and C++.
    Proficient in developing web applications using React and Node.js.
    Strong understanding of SQL and NoSQL databases. Experience with AWS and Docker.
    Excellent communication and teamwork skills. Adept at problem-solving and critical thinking.
    Familiar with Agile and Scrum methodologies. Also uses Jira and Slack.
    """
    skills = extract_skills(resume_text)
    print("Extracted Skills:", skills)