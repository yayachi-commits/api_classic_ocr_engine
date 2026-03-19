"""Pydantic response models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Standard error response."""

    success: bool = False
    error_code: str
    message: str
    request_id: str | None = None


class MessageResponse(BaseModel):
    """Generic message response."""

    success: bool = True
    message: str
    request_id: str | None = None


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    version: str
    uptime_seconds: int


class ConversionResponse(BaseModel):
    """OCR/Conversion response."""

    success: bool = Field(default=True, description="Whether conversion was successful")
    input_file: str = Field(description="Name of the input file")
    file_format: str = Field(description="Format of the input file (pdf, docx, html, txt)")
    lines_extracted: int = Field(description="Number of text lines extracted")
    text_content: str = Field(description="Extracted text content")
    request_id: str | None = Field(default=None, description="Request ID for tracking")
