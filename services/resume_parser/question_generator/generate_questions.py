# question_generator/generate_questions.py

import json
import google.generativeai as genai
from typing import List, Dict

# Initialize Gemini API (replace with your actual API key - consider using environment variables)
GEMINI_API_KEY = "AIzaSyDlYrVWROFEhXqdESZ3wxEE_UK-_V3sTJs"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Load question templates from JSON files
try:
    with open("question_generator/templates/js.json", 'r') as f:
        js_templates = json.load(f)
    with open("question_generator/templates/python.json", 'r') as f:
        python_templates = json.load(f)
except FileNotFoundError as e:
    print(f"Error loading templates: {e}")
    js_templates = {}
    python_templates = {}
except json.JSONDecodeError as e:
    print(f"Error decoding JSON in templates: {e}")
    js_templates = {}
    python_templates = {}

def generate_questions_with_gemini(prompt: str) -> List[str]:
    """
    Generates interview questions using the Gemini API based on the provided prompt.
    """
    try:
        response = model.generate_content(prompt)
        response.raise_for_status()
        if response.text:
            return [q.strip() for q in response.text.split('\n') if q.strip()]
        else:
            return []
    except Exception as e:
        print(f"Error generating questions with Gemini: {e}")
        return []

def create_prompt_from_template(resume_data: Dict[str, str], template: str, num_questions: int = 3) -> str:
    """
    Creates a prompt for Gemini using a predefined template and resume data.
    """
    prompt = template.format(**resume_data, num_questions=num_questions)
    return prompt

def generate_interview_questions(resume_data: Dict[str, str], question_type: str = "general", num_questions: int = 3) -> List[str]:
    """
    Orchestrates the generation of interview questions based on resume data and type.
    """
    if not resume_data:
        return ["No resume data provided."]

    prompt = f"Generate {num_questions} insightful interview questions for a candidate with the following background:\n\n"
    for key, value in resume_data.items():
        prompt += f"{key}: {value}\n"

    if question_type == "behavioral":
        prompt += "\nFocus on behavioral questions related to their experience, teamwork, problem-solving, and adaptability."
    elif question_type == "technical":
        # Example of using templates based on skills
        skills = resume_data.get("Skills", "").lower()
        if "javascript" in skills and js_templates.get("technical"):
            prompt = create_prompt_from_template(resume_data, js_templates["technical"], num_questions)
        elif "python" in skills and python_templates.get("technical"):
            prompt = create_prompt_from_template(resume_data, python_templates["technical"], num_questions)
        else:
            prompt += "\nFocus on technical questions related to the skills and technologies mentioned."
    elif question_type == "skills-based":
        prompt += f"\nFocus on questions that assess their proficiency in the key skills mentioned."
    else:
        prompt += "\nInclude a mix of general interview questions based on their experience."

    prompt += "\nPlease provide the questions as a numbered list or separated by newlines."
    return generate_questions_with_gemini(prompt)

if __name__ == "__main__":
    sample_resume_data = {
        "Summary": "Experienced software engineer with 5+ years in Python and web development.",
        "Skills": "Python, Django, JavaScript, React, SQL, AWS",
        "Experience": "Developed and deployed web applications, worked in agile teams."
    }
    behavioral_questions = generate_interview_questions(sample_resume_data, question_type="behavioral", num_questions=2)
    print("Behavioral Questions:\n", behavioral_questions)

    technical_questions = generate_interview_questions(sample_resume_data, question_type="technical", num_questions=2)
    print("\nTechnical Questions:\n", technical_questions)