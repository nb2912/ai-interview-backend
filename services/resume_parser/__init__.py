from resume_parser import parse_pdf, extract_skills

# Example usage:
if __name__ == "__main__":
    pdf_path = "path/to/your/resume.pdf"
    parsed_text = parse_pdf(pdf_path)
    if parsed_text:
        skills = extract_skills(parsed_text)
        print("Extracted Skills:", skills)
    else:
        print("Could not parse the PDF.")