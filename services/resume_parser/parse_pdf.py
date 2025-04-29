# resume_parser/parse_pdf.py

from PyPDF2 import PdfReader
from typing import Optional

def parse_pdf(pdf_path: str) -> Optional[str]:
    """
    Extracts text content from a PDF file.

    Args:
        pdf_path: The path to the PDF file.

    Returns:
        The extracted text content as a string, or None if an error occurs.
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text
    except FileNotFoundError:
        print(f"Error: PDF file not found at {pdf_path}")
        return None
    except Exception as e:
        print(f"An error occurred while parsing the PDF: {e}")
        return None

if __name__ == "__main__":
    pdf_file_path = "example.pdf"  # Replace with the actual path to your PDF file

    # Create a dummy PDF file for testing if it doesn't exist
    try:
        with open(pdf_file_path, 'wb') as f:
            from reportlab.pdfgen import canvas
            c = canvas.Canvas(f)
            c.drawString(100, 750, "This is a sample PDF file for testing.")
            c.drawString(100, 700, "It contains some text that should be extracted.")
            c.save()
        print(f"Created a dummy PDF file: {pdf_file_path}")
    except ImportError:
        print("Please create a sample PDF file named 'example.pdf' in the same directory.")

    extracted_text = parse_pdf(pdf_file_path)

    if extracted_text:
        print("Extracted Text:\n", extracted_text)
    else:
        print("No text extracted or an error occurred.")