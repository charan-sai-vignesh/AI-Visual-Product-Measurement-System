"""Data schemas for the visual product measurement system."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class VisualDimension(BaseModel):
    """A visual dimension measurement from -5.0 to +5.0."""
    gender_expression: float = Field(..., ge=-5.0, le=5.0, description="Masculine (-5) to Feminine (+5)")
    visual_weight: float = Field(..., ge=-5.0, le=5.0, description="Sleek/Light (-5) to Bold/Heavy (+5)")
    embellishment: float = Field(..., ge=-5.0, le=5.0, description="Simple (-5) to Ornate (+5)")
    unconventionality: float = Field(..., ge=-5.0, le=5.0, description="Classic (-5) to Avant-garde (+5)")
    formality: float = Field(..., ge=-5.0, le=5.0, description="Casual (-5) to Formal (+5)")


class VisualAttributes(BaseModel):
    """Other observable visual attributes."""
    visible_wirecore: Optional[bool] = None
    frame_geometry: Optional[str] = None  # e.g., "rectangular", "round", "cat-eye", "aviator"
    transparency_opacity: Optional[str] = None  # e.g., "transparent", "opaque", "semi-transparent"
    dominant_colors: Optional[List[str]] = None
    visible_textures: Optional[List[str]] = None
    suitable_for_kids: Optional[bool] = None


class VisualMetadata(BaseModel):
    """Basic visual metadata."""
    image_format: Optional[str] = None
    dimensions: Optional[Dict[str, int]] = None  # width, height
    has_multiple_items: Optional[bool] = None
    primary_product_visible: Optional[bool] = None


class MeasurementResult(BaseModel):
    """Complete measurement result for a product."""
    product_id: Optional[str] = None
    image_urls: List[str]
    dimensions: VisualDimension
    attributes: VisualAttributes
    metadata: VisualMetadata
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    processing_notes: Optional[List[str]] = None


class AnalysisRequest(BaseModel):
    """Request to analyze product images."""
    image_urls: List[str] = Field(..., min_items=1, description="List of image URLs to analyze")
    product_id: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    details: Optional[Dict[str, Any]] = None

