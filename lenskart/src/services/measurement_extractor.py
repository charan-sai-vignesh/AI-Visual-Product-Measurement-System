"""Extract visual attributes and metadata from images and captions."""

import logging
from typing import List
from src.models.schemas import VisualAttributes, VisualMetadata, VisualDimension

logger = logging.getLogger(__name__)


class MeasurementExtractor:
    """
    Extracts visual measurements including dimensions, attributes, and metadata.
    """

    # --------------------------------------------------
    # DIMENSIONS
    # --------------------------------------------------

    def extract_dimensions(self, analysis_text: str, image_descriptions: List[str]) -> VisualDimension:
        """
        Extract dimensional measurements from analysis.
        
        Uses rule-based extraction and keyword analysis to determine scores.
        
        Args:
            analysis_text: Combined analysis text
            image_descriptions: List of individual image descriptions
            
        Returns:
            VisualDimension object with scores
        """
        # Combine all text for analysis
        combined_text = analysis_text.lower() + " " + " ".join([d.lower() for d in image_descriptions])
        
        # Gender Expression: -5 (masculine) to +5 (feminine)
        gender_score = 0.0
        masculine_keywords = ['masculine', 'men', 'male', 'bold', 'angular', 'strong', 'thick frame']
        feminine_keywords = ['feminine', 'women', 'female', 'delicate', 'curved', 'thin frame', 'cat-eye', 'round']
        unisex_keywords = ['unisex', 'neutral', 'versatile', 'classic']
        
        masculine_count = sum(1 for kw in masculine_keywords if kw in combined_text)
        feminine_count = sum(1 for kw in feminine_keywords if kw in combined_text)
        unisex_count = sum(1 for kw in unisex_keywords if kw in combined_text)
        
        if masculine_count > feminine_count:
            gender_score = -min(5.0, masculine_count * 1.5)
        elif feminine_count > masculine_count:
            gender_score = min(5.0, feminine_count * 1.5)
        elif unisex_count > 0:
            gender_score = 0.0
        
        # Visual Weight: -5 (sleek/light) to +5 (bold/heavy)
        weight_score = 0.0
        light_keywords = ['light', 'sleek', 'thin', 'minimal', 'delicate', 'air', 'wire']
        heavy_keywords = ['bold', 'thick', 'heavy', 'chunky', 'substantial', 'large', 'wide', 'dark']
        
        light_count = sum(1 for kw in light_keywords if kw in combined_text)
        heavy_count = sum(1 for kw in heavy_keywords if kw in combined_text)
        
        if light_count > heavy_count:
            weight_score = -min(5.0, light_count * 1.2)
        elif heavy_count > light_count:
            weight_score = min(5.0, heavy_count * 1.2)
        
        # Embellishment: -5 (simple) to +5 (ornate)
        embellishment_score = 0.0
        simple_keywords = ['simple', 'plain', 'minimal', 'basic', 'clean', 'unadorned']
        ornate_keywords = ['decorative', 'patterned', 'embellished', 'ornate', 'detailed', 'textured', 'design']
        
        simple_count = sum(1 for kw in simple_keywords if kw in combined_text)
        ornate_count = sum(1 for kw in ornate_keywords if kw in combined_text)
        
        if simple_count > ornate_count:
            embellishment_score = -min(5.0, simple_count * 1.2)
        elif ornate_count > simple_count:
            embellishment_score = min(5.0, ornate_count * 1.2)
        
        # Unconventionality: -5 (classic) to +5 (avant-garde)
        unconventionality_score = 0.0
        classic_keywords = ['classic', 'traditional', 'standard', 'conventional', 'timeless', 'regular']
        avant_keywords = ['unique', 'unusual', 'distinctive', 'modern', 'contemporary', 'stylish', 'trendy', 'fashion']
        
        classic_count = sum(1 for kw in classic_keywords if kw in combined_text)
        avant_count = sum(1 for kw in avant_keywords if kw in combined_text)
        
        if classic_count > avant_count:
            unconventionality_score = -min(5.0, classic_count * 1.2)
        elif avant_count > classic_count:
            unconventionality_score = min(5.0, avant_count * 1.2)
        
        # Formality: -5 (casual) to +5 (formal)
        formality_score = 0.0
        casual_keywords = ['casual', 'everyday', 'sport', 'relaxed', 'comfortable', 'fun']
        formal_keywords = ['formal', 'professional', 'elegant', 'sophisticated', 'business', 'refined']
        
        casual_count = sum(1 for kw in casual_keywords if kw in combined_text)
        formal_count = sum(1 for kw in formal_keywords if kw in combined_text)
        
        if casual_count > formal_count:
            formality_score = -min(5.0, casual_count * 1.2)
        elif formal_count > casual_count:
            formality_score = min(5.0, formal_count * 1.2)
        
        return VisualDimension(
            gender_expression=round(gender_score, 2),
            visual_weight=round(weight_score, 2),
            embellishment=round(embellishment_score, 2),
            unconventionality=round(unconventionality_score, 2),
            formality=round(formality_score, 2)
        )

    # --------------------------------------------------
    # ATTRIBUTES
    # --------------------------------------------------

    def extract_attributes(self, analysis_text: str, image_descriptions: List[str]) -> VisualAttributes:
        combined_text = (analysis_text + " " + " ".join(image_descriptions)).lower()

        # Wirecore detection
        visible_wirecore = None
        if "wire" in combined_text:
            visible_wirecore = True
        elif any(k in combined_text for k in ["plastic", "acetate", "thick"]):
            visible_wirecore = False

        # Frame geometry
        frame_geometry = None
        geometry_patterns = {
            "rectangular": ["rectangular", "square", "boxy"],
            "round": ["round", "circular"],
            "cat-eye": ["cat-eye", "cat eye"],
            "aviator": ["aviator", "pilot"],
            "oval": ["oval"],
            "browline": ["browline", "clubmaster"],
            "wayfarer": ["wayfarer"],
        }

        for geom, keywords in geometry_patterns.items():
            if any(k in combined_text for k in keywords):
                frame_geometry = geom
                break

        # Transparency
        transparency_opacity = None
        if "transparent" in combined_text or "clear" in combined_text:
            transparency_opacity = "transparent"
        elif "opaque" in combined_text or "solid" in combined_text:
            transparency_opacity = "opaque"
        elif "tinted" in combined_text:
            transparency_opacity = "semi-transparent"

        # Dominant colors
        color_keywords = [
            "black", "brown", "gold", "silver", "red",
            "blue", "green", "white", "grey", "gray",
            "tortoise", "transparent", "clear"
        ]
        dominant_colors = list(
            {color.title() for color in color_keywords if color in combined_text}
        )[:5]

        # Textures
        texture_keywords = [
            "textured", "patterned", "matte",
            "glossy", "brushed", "polished",
            "tortoiseshell", "marbled", "metal"
        ]
        visible_textures = list(
            {tex.title() for tex in texture_keywords if tex in combined_text}
        )

        # Kids suitability
        suitable_for_kids = None
        if "kids" in combined_text or "child" in combined_text:
            suitable_for_kids = True
        elif "adult" in combined_text or "professional" in combined_text:
            suitable_for_kids = False

        return VisualAttributes(
            visible_wirecore=visible_wirecore,
            frame_geometry=frame_geometry,
            transparency_opacity=transparency_opacity,
            dominant_colors=dominant_colors or None,
            visible_textures=visible_textures or None,
            suitable_for_kids=suitable_for_kids,
        )

    # --------------------------------------------------
    # METADATA
    # --------------------------------------------------

    def extract_metadata(self, images: List) -> VisualMetadata:
        if not images:
            return VisualMetadata()

        first_image = images[0]

        return VisualMetadata(
            image_format=first_image.format or "JPEG",
            dimensions={
                "width": first_image.width,
                "height": first_image.height,
            },
            has_multiple_items=len(images) > 1,
            primary_product_visible=True,
        )
