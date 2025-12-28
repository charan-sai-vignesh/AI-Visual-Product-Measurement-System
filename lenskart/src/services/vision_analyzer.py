import logging
from typing import Dict
from PIL import Image
import numpy as np

from src.config import USE_BLIP, BLIP_MODEL_NAME

logger = logging.getLogger(__name__)


class VisionAnalyzer:
    """
    Hybrid Vision Analyzer

    - BLIP (optional) for semantic captioning
    - Deterministic image statistics for visual measurements
    - Stable output schema (no downstream changes)
    """

    def __init__(self):
        self.use_blip = USE_BLIP
        self.blip_processor = None
        self.blip_model = None

        if self.use_blip:
            self._load_blip()

    # -------------------------------------------------
    # BLIP LOADING
    # -------------------------------------------------
    def _load_blip(self):
        try:
            from transformers import BlipProcessor, BlipForConditionalGeneration
            import torch

            self.blip_processor = BlipProcessor.from_pretrained(BLIP_MODEL_NAME)
            self.blip_model = BlipForConditionalGeneration.from_pretrained(BLIP_MODEL_NAME)
            self.blip_model.eval()

            logger.info("✅ BLIP model loaded successfully")

        except Exception as e:
            logger.error(f"❌ Failed to load BLIP model: {e}")
            self.use_blip = False

    # -------------------------------------------------
    # BLIP CAPTION
    # -------------------------------------------------
    def _generate_blip_caption(self, image: Image.Image) -> str:
        inputs = self.blip_processor(image, return_tensors="pt")
        output = self.blip_model.generate(**inputs, max_length=40)
        caption = self.blip_processor.decode(output[0], skip_special_tokens=True)
        return caption

    # -------------------------------------------------
    # MAIN ANALYSIS
    # -------------------------------------------------
    def analyze_image(self, image: Image.Image) -> Dict[str, object]:

        # -----------------------------
        # IMAGE STATISTICS 
        # -----------------------------
        img = np.array(image.convert("RGB")) / 255.0

        brightness = img.mean()        # overall light/dark
        color_variance = img.std()     # visual complexity

        width, height = image.size

        # -----------------------------
        # SEMANTIC CAPTION
        # -----------------------------
        if self.use_blip and self.blip_model is not None:
            caption = self._generate_blip_caption(image)
        else:
            # Honest fallback (no hallucination)
            if brightness < 0.45:
                tone = "very dark"
            elif brightness < 0.55:
                tone = "dark"
            elif brightness < 0.65:
                tone = "neutral"
            else:
                tone = "light"

            if color_variance < 0.05:
                complexity = "minimal"
            elif color_variance < 0.10:
                complexity = "simple"
            else:
                complexity = "visually detailed"

            caption = (
                f"{tone} toned eyewear, "
                f"{complexity} visual design, "
                f"studio product photograph"
            )

        # -----------------------------
        # EYWEAR-ADJUSTED BASELINES
        # -----------------------------
        neutral_brightness = 0.65
        neutral_variance = 0.06

        # -----------------------------
        # VISUAL MEASUREMENTS (SIGNED)
        # -----------------------------
        visual_weight = (neutral_brightness - brightness) * 6
        embellishment = (color_variance - neutral_variance) * 25
        unconventionality = (color_variance - neutral_variance) * 7

        # Reduce background bias for formality
        formality = (
            (neutral_brightness - brightness) * 2
            + (color_variance < 0.06) * 0.8
        )

        # Gender expression intentionally weak & centered
        gender_expression = (neutral_brightness - brightness) * 2

        # -----------------------------
        # CLAMP TO -5 → +5
        # -----------------------------
        def clamp(x: float) -> float:
            return max(-5.0, min(5.0, round(x, 2)))

        measurements = {
            "gender_expression": clamp(gender_expression),
            "visual_weight": clamp(visual_weight),
            "embellishment": clamp(embellishment),
            "unconventionality": clamp(unconventionality),
            "formality": clamp(formality),
        }

        # -----------------------------
        # OUTPUT
        # -----------------------------
        return {
            "caption": caption,
            "measurements": measurements,
        }
