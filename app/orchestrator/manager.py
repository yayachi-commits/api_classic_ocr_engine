"""Orchestrator manager for handling document conversions."""

from __future__ import annotations

from .converter import convert_bytes_to_txt
from ..internal.config import Settings
from ..internal.logs import get_logger

logger = get_logger("orchestrator.manager")


class ConversionManager:
    """Manager for document conversions."""

    def __init__(self, settings: Settings):
        """Initialize the conversion manager.

        Args:
            settings: Application settings
        """
        self.settings = settings
        logger.info("ConversionManager initialized")

    def is_ready(self) -> bool:
        """Check if the manager is ready to process conversions.

        Returns:
            True if ready
        """
        return True

    def convert(
        self,
        file_bytes: bytes,
        file_format: str,
        use_ocr: bool | None = None,
    ) -> dict:
        """Convert a document to text.

        Args:
            file_bytes: File content as bytes
            file_format: File format (pdf, docx, html, txt)
            use_ocr: Whether to enable OCR (defaults to settings.enable_ocr)

        Returns:
            Dictionary with conversion results containing:
            - lines: List of text lines
            - line_count: Number of lines extracted

        Raises:
            ValueError: If file format is not supported
        """
        if use_ocr is None:
            use_ocr = self.settings.enable_ocr

        logger.info("Starting conversion: format=%s use_ocr=%s", file_format, use_ocr)

        lines, line_count = convert_bytes_to_txt(
            file_bytes,
            file_format,
            use_ocr=use_ocr,
        )

        text_content = "\n".join(lines)

        result = {
            "lines": lines,
            "line_count": line_count,
            "text": text_content,
        }

        logger.info("Conversion complete: lines=%d", line_count)
        return result

    def validate_format(self, file_format: str) -> bool:
        """Check if a file format is supported.

        Args:
            file_format: File format to validate

        Returns:
            True if format is supported
        """
        return file_format.lower().strip() in self.settings.supported_formats

    def get_supported_formats(self) -> list[str]:
        """Get list of supported file formats.

        Returns:
            List of supported formats
        """
        return self.settings.supported_formats
