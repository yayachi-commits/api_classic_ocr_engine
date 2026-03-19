"""Document conversion endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, File, HTTPException, Query, Request, UploadFile, status

from ..internal.logs import get_logger
from ..internal.models import ConversionResponse, MessageResponse
from ..orchestrator.manager import ConversionManager

logger = get_logger("api.convert")

router = APIRouter(prefix="/convert", tags=["conversion"])


def get_manager(request: Request) -> ConversionManager:
    """Get the conversion manager from app state via dependency injection.

    Args:
        request: FastAPI request object

    Returns:
        ConversionManager instance

    Raises:
        HTTPException: If manager is not initialized
    """
    manager = getattr(request.app.state, "manager", None)
    if not isinstance(manager, ConversionManager):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Conversion service manager is not initialized",
        )
    return manager


@router.get(
    "/formats",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def list_formats(
    request: Request = None,
    manager: ConversionManager = Depends(get_manager),
) -> MessageResponse:
    """List supported file formats for conversion."""
    request_id = getattr(request.state, "request_id", None) if request else None

    formats = manager.get_supported_formats()
    logger.info("Listed supported formats: %s | request_id=%s", formats, request_id)

    return MessageResponse(
        success=True,
        message=f"Supported formats: {', '.join(formats)}",
        request_id=request_id,
    )


@router.post(
    "",
    response_model=ConversionResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"description": "Invalid file or format"},
        422: {"description": "Validation error"},
        413: {"description": "File too large"},
    },
)
async def convert(
    file: UploadFile = File(..., description="Document file to convert (pdf, docx, html, txt)"),
    format: str = Query(None, description="File format (auto-detected from extension if not provided)"),
    use_ocr: bool = Query(False, description="Enable OCR for image-based PDFs"),
    request: Request = None,
    manager: ConversionManager = Depends(get_manager),
) -> ConversionResponse:
    """Convert a document to clean text.

    - **file**: Document file (PDF, DOCX, HTML, or TXT)
    - **format**: File format (optional, auto-detected if not provided)
    - **use_ocr**: Enable OCR fallback for image-based PDFs
    """
    request_id = getattr(request.state, "request_id", None) if request else None

    # Get file extension
    if not file.filename:
        logger.warning("Missing filename | request_id=%s", request_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must have a valid filename with extension",
        )

    # Determine format
    detected_format = format or file.filename.split(".")[-1].lower()
    if not detected_format:
        logger.warning("Cannot determine file format | request_id=%s", request_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot determine file format. Provide format parameter or use valid extension.",
        )

    # Validate format
    if not manager.validate_format(detected_format):
        available = manager.get_supported_formats()
        logger.warning(
            "Unsupported format: %s | available: %s | request_id=%s",
            detected_format,
            available,
            request_id,
        )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unsupported format '{detected_format}'. Supported: {', '.join(available)}",
        )

    # Check file size
    file_size_mb = 0
    file_content = await file.read()
    file_size_mb = len(file_content) / (1024 * 1024)

    if file_size_mb > manager.settings.max_file_size_mb:
        logger.warning(
            "File too large: %.2f MB (max: %d MB) | request_id=%s",
            file_size_mb,
            manager.settings.max_file_size_mb,
            request_id,
        )
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum size of {manager.settings.max_file_size_mb} MB",
        )

    try:
        logger.info(
            "Converting file | name=%s format=%s size=%.2f MB use_ocr=%s | request_id=%s",
            file.filename,
            detected_format,
            file_size_mb,
            use_ocr,
            request_id,
        )

        # Perform conversion
        result = manager.convert(file_content, detected_format, use_ocr=use_ocr)

        response = ConversionResponse(
            success=True,
            input_file=file.filename,
            file_format=detected_format,
            lines_extracted=result["line_count"],
            text_content=result["text"],
            request_id=request_id,
        )

        logger.info(
            "Conversion successful | lines=%d | request_id=%s",
            result["line_count"],
            request_id,
        )

        return response

    except ValueError as e:
        logger.error("Validation error: %s | request_id=%s", str(e), request_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.exception("Conversion failed | request_id=%s", request_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Conversion failed: {str(e)}",
        )
