"""Image processing utilities."""

import io
import requests
from PIL import Image
from typing import Optional
import logging

logger = logging.getLogger(__name__)

MAX_IMAGE_SIDE = 1024  # 🔥 safety resize for vision models


async def download_image(url: str, timeout: int = 30) -> Optional[Image.Image]:
    """
    Download an image from a URL and return as PIL Image.
    """
    try:
        import aiohttp

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, timeout=aiohttp.ClientTimeout(total=timeout)
            ) as response:

                if response.status != 200:
                    logger.warning(f"Failed to download image {url}: HTTP {response.status}")
                    return None

                image_data = await response.read()
                image = Image.open(io.BytesIO(image_data))

                # Convert to RGB (required by vision models)
                if image.mode != "RGB":
                    image = image.convert("RGB")

                # 🔥 Resize large images safely
                if max(image.size) > MAX_IMAGE_SIDE:
                    image.thumbnail((MAX_IMAGE_SIDE, MAX_IMAGE_SIDE))

                return image

    except Exception as e:
        logger.error(f"Error downloading image {url}: {e}")
        return None
