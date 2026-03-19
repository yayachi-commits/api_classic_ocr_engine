"""Document conversion engine supporting PDF, DOCX, HTML, and TXT formats."""

from __future__ import annotations

import re
import tempfile
from typing import List

import fitz  # PyMuPDF
import docx

try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None  # OCR is optional

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None  # HTML parsing is optional

from ..internal.logs import get_logger

logger = get_logger("orchestrator.converter")


# ============================================================
# TEXT CLEANING UTILITIES
# ============================================================


def clean_ascii(text: str) -> str:
    """Clean ASCII and special characters from text."""
    if not text:
        return ""
    bullet_like = r"[•▪◦●·‣■□▪◘◙▶►◆]"
    text = re.sub(bullet_like, "-", text)
    text = "".join("-" if 0x25A0 <= ord(c) <= 0x25FF else c for c in text)
    text = text.replace("\t", " ").strip()
    return text


def clean_line(text: str) -> str:
    """Clean a single line of text."""
    text = clean_ascii(text)
    text = re.sub(r" {2,}", " ", text)
    return text


# ============================================================
# PDF → TXT
# ============================================================


def pdf_to_txt(pdf_bytes: bytes, use_ocr: bool = False) -> List[str]:
    """
    Extract clean text paragraphs from a PDF.
    If use_ocr=True, will try OCR for pages with no text.

    Args:
        pdf_bytes: PDF file content as bytes
        use_ocr: Whether to enable OCR fallback for image-based PDFs

    Returns:
        List of text paragraphs extracted from the PDF
    """
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    output_lines = []

    for i, page in enumerate(doc, start=1):
        raw = page.get_text("text")
        if not raw and use_ocr and pytesseract:
            # Render page as image and run OCR
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            raw = pytesseract.image_to_string(img)
            logger.debug("Applied OCR to PDF page %d", i)

        if not raw:
            continue

        # Merge lines into paragraphs if possible
        lines = raw.split("\n")
        paragraph = ""
        for line in lines:
            line = clean_line(line)
            if not line:
                if paragraph:
                    output_lines.append(paragraph.strip())
                    paragraph = ""
                continue
            if paragraph:
                paragraph += " " + line
            else:
                paragraph = line
        if paragraph:
            output_lines.append(paragraph.strip())

    logger.info("Extracted %d lines from PDF (%d pages)", len(output_lines), len(doc))
    return output_lines


# ============================================================
# DOCX → TXT
# ============================================================


def docx_to_txt(docx_bytes: bytes) -> List[str]:
    """
    Extract clean text from a DOCX file.

    Args:
        docx_bytes: DOCX file content as bytes

    Returns:
        List of paragraphs extracted from the DOCX
    """
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        tmp.write(docx_bytes)
        tmp.flush()
        document = docx.Document(tmp.name)

    output_lines = []
    for para in document.paragraphs:
        text = clean_line(para.text)
        if text:
            output_lines.append(text)

    logger.info("Extracted %d lines from DOCX", len(output_lines))
    return output_lines


# ============================================================
# HTML → TXT
# ============================================================


def html_to_txt(html_bytes: bytes) -> List[str]:
    """
    Extract clean text from an HTML file.

    Args:
        html_bytes: HTML file content as bytes

    Returns:
        List of text lines extracted from the HTML
    """
    if not BeautifulSoup:
        raise ImportError(
            "BeautifulSoup4 is required for HTML conversion. "
            "Install with: pip install beautifulsoup4"
        )

    html_content = html_bytes.decode("utf-8", errors="replace")
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()

    # Get text and split into paragraphs
    text = soup.get_text()
    lines = text.split("\n")

    output_lines = []
    for line in lines:
        line = clean_line(line)
        if line:
            output_lines.append(line)

    logger.info("Extracted %d lines from HTML", len(output_lines))
    return output_lines


# ============================================================
# TXT → TXT (Passthrough with cleaning)
# ============================================================


def txt_to_txt(txt_bytes: bytes) -> List[str]:
    """
    Clean and parse a plain text file.

    Args:
        txt_bytes: TXT file content as bytes

    Returns:
        List of cleaned text lines
    """
    text_content = txt_bytes.decode("utf-8", errors="replace")
    lines = text_content.split("\n")

    output_lines = []
    for line in lines:
        line = clean_line(line)
        if line:
            output_lines.append(line)

    logger.info("Extracted %d lines from TXT", len(output_lines))
    return output_lines


# ============================================================
# MASTER CONVERSION FUNCTION
# ============================================================


def convert_bytes_to_txt(
    file_bytes: bytes,
    file_format: str,
    use_ocr: bool = False,
) -> tuple[List[str], int]:
    """
    Convert document bytes to clean text lines.

    Args:
        file_bytes: File content as bytes
        file_format: File format (pdf, docx, html, txt)
        use_ocr: Whether to enable OCR for PDF (if available)

    Returns:
        Tuple of (list of text lines, number of lines)

    Raises:
        ValueError: If file format is not supported
    """
    file_format = file_format.lower().strip()

    try:
        if file_format == "pdf":
            lines = pdf_to_txt(file_bytes, use_ocr=use_ocr)
        elif file_format == "docx":
            lines = docx_to_txt(file_bytes)
        elif file_format == "html":
            lines = html_to_txt(file_bytes)
        elif file_format == "txt":
            lines = txt_to_txt(file_bytes)
        else:
            raise ValueError(
                f"Unsupported file format '{file_format}'. "
                "Supported formats: pdf, docx, html, txt"
            )

        logger.info("Conversion successful for format=%s lines=%d", file_format, len(lines))
        return lines, len(lines)

    except Exception as e:
        logger.error("Conversion failed for format=%s: %s", file_format, str(e))
        raise
