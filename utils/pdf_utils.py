import fitz


def extract_text_from_pdf(file):
    """Extract text from an uploaded PDF."""

    text = ""

    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text.strip()