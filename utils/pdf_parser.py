# utils/pdf_parser.py - Extracts text from PDF files

import PyPDF2

def extract_text_from_pdf(pdf_file):
    """
    Extracts text from an uploaded PDF file.
    
    Args:
        pdf_file: Uploaded PDF file (from Streamlit)
    
    Returns:
        tuple: (text, error_message) - text is None if error
    """
    try:
        # Create PDF reader
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        # Check if PDF is encrypted
        if pdf_reader.is_encrypted:
            return None, "PDF is password protected. Please provide an unencrypted PDF."
        
        # Extract text from all pages
        text = ""
        for page in pdf_reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
        
        # Check if text was extracted
        if not text.strip():
            return None, "No text found in PDF. It may be a scanned image. Please use a text-based PDF."
        
        return text.strip(), None
        
    except Exception as e:
        return None, f"Error parsing PDF: {str(e)}"