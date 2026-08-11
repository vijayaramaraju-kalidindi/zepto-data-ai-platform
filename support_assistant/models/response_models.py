"""
Pydantic response models for the Support Assistant.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class FinalAnswer(BaseModel):
    """
    Structured final response for the Support Assistant.
    """

    answer: str

    sources: list[str] = Field(
        default_factory=list,
    )

    confidence: float = Field(
        ge=0.0,
        le=1.0,
    )