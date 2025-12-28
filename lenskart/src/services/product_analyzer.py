# src/services/product_analyzer.py

import logging
from typing import List, Optional

from PIL import Image

from src.services.image_processor import download_image
from src.services.vision_analyzer import VisionAnalyzer
from src.services.measurement_extractor import MeasurementExtractor

from src.models.schemas import (
    MeasurementResult,
    VisualDimension,
    VisualAttributes,
    VisualMetadata,
)

logger = logging.getLogger(__name__)


class ProductAnalyzer:
    """
    ProductAnalyzer orchestrates:
    - image downloading
    - vision-based analysis
    - aggregation of visual measurements
    - metadata & attribute extraction

    This file is SAFE to import and contains no FastAPI or runtime side effects.
    """

    def __init__(self):
        self.vision_analyzer = VisionAnalyzer()
        self.measurement_extractor = MeasurementExtractor()

    async def analyze_product(
        self,
        image_urls: List[str],
        product_id: Optional[str] = None,
    ) -> MeasurementResult:

        images: List[Image.Image] = []
        captions: List[str] = []
        measurements: List[dict] = []
        notes: List[str] = []

        # --------------------------------------------------
        # 1. Download images
        # --------------------------------------------------
        for url in image_urls:
            try:
                image = await download_image(url)
                if image:
                    images.append(image)
                else:
                    notes.append(f"Failed to download image: {url}")
            except Exception as e:
                logger.error(e)
                notes.append(str(e))

        if not images:
            raise ValueError("No images could be downloaded")

        # --------------------------------------------------
        # 2. Vision analysis (ONE ARGUMENT ONLY)
        # --------------------------------------------------
        for image in images:
            try:
                result = self.vision_analyzer.analyze_image(image)
                captions.append(result["caption"])
                measurements.append(result["measurements"])
            except Exception as e:
                logger.error(e)
                notes.append(str(e))

        # --------------------------------------------------
        # 3. Aggregate visual dimensions
        # --------------------------------------------------
        def avg(key: str) -> float:
            values = [m[key] for m in measurements if key in m]
            return round(sum(values) / len(values), 2) if values else 0.0

        dimensions = VisualDimension(
            visual_weight=avg("visual_weight"),
            embellishment=avg("ornateness"),
            formality=avg("formality"),
            unconventionality=avg("unconventionality"),
            gender_expression=0.0,
        )

        # --------------------------------------------------
        # 4. Attributes & metadata
        # --------------------------------------------------
        try:
            attributes = self.measurement_extractor.extract_attributes(
                " ".join(captions), captions
            )
        except Exception:
            attributes = VisualAttributes()

        try:
            metadata = self.measurement_extractor.extract_metadata(images)
        except Exception:
            metadata = VisualMetadata()

        # --------------------------------------------------
        # 5. Confidence score
        # --------------------------------------------------
        confidence_score = round(len(measurements) / len(image_urls), 2)

        # --------------------------------------------------
        # 6. Final result
        # --------------------------------------------------
        return MeasurementResult(
            product_id=product_id,
            image_urls=image_urls,
            dimensions=dimensions,
            attributes=attributes,
            metadata=metadata,
            confidence_score=confidence_score,
            processing_notes=notes or None,
        )
