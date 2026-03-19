"""Centralized application settings."""

from __future__ import annotations

from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # API Settings
    app_name: str = Field(default="Classic OCR Engine", validation_alias="APP_NAME")
    app_env: str = Field(default="dev", validation_alias="APP_ENV")
    app_version: str = Field(default="1.0.0", validation_alias="APP_VERSION")
    api_prefix: str = Field(default="/api/v1", validation_alias="API_PREFIX")
    debug: bool = Field(default=False, validation_alias="DEBUG")
    docs_enabled: bool = Field(default=True, validation_alias="DOCS_ENABLED")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    host: str = Field(default="0.0.0.0", validation_alias="HOST")
    port: int = Field(default=9003, validation_alias="PORT")
    request_timeout_seconds: int = Field(default=300, validation_alias="REQUEST_TIMEOUT_SECONDS")
    gzip_min_size: int = Field(default=1024, validation_alias="GZIP_MIN_SIZE")
    cors_origins: list[str] = Field(default_factory=list, validation_alias="CORS_ORIGINS")
    allowed_hosts: list[str] = Field(default_factory=lambda: ["*"], validation_alias="ALLOWED_HOSTS")

    # OCR Settings
    max_file_size_mb: int = Field(default=100, validation_alias="MAX_FILE_SIZE_MB")
    supported_formats: list[str] = Field(
        default_factory=lambda: ["pdf", "docx", "html", "txt"],
        validation_alias="SUPPORTED_FORMATS",
    )
    enable_ocr: bool = Field(default=True, validation_alias="ENABLE_OCR")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        level = value.upper()
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if level not in valid:
            raise ValueError(f"Invalid LOG_LEVEL '{value}'. Expected one of {sorted(valid)}")
        return level

    @field_validator("api_prefix")
    @classmethod
    def validate_api_prefix(cls, value: str) -> str:
        if not value:
            return ""
        return value if value.startswith("/") else f"/{value}"

    @field_validator("request_timeout_seconds", "gzip_min_size", "max_file_size_mb")
    @classmethod
    def validate_positive_int(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Value must be >= 1.")
        return value

    @field_validator("cors_origins", "allowed_hosts", mode="before")
    @classmethod
    def parse_str_list(cls, value: Any) -> list[str]:
        if value is None:
            return []
        if isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                return []
            return [item.strip() for item in cleaned.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        raise ValueError("Expected a comma-separated string or list.")

    @field_validator("supported_formats", mode="before")
    @classmethod
    def parse_formats(cls, value: Any) -> list[str]:
        if value is None:
            return ["pdf", "docx", "html", "txt"]
        if isinstance(value, str):
            return [f.strip().lower() for f in value.split(",") if f.strip()]
        if isinstance(value, list):
            return [str(f).strip().lower() for f in value if str(f).strip()]
        raise ValueError("Expected a comma-separated string or list.")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return a cached settings instance."""
    return Settings()
