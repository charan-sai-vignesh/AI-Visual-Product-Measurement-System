"""Configuration settings for the application."""
import os
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------
# ENV LOADING
# --------------------------------------------------

project_root = Path(__file__).parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# --------------------------------------------------
# API CONFIG
# --------------------------------------------------

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# --------------------------------------------------
# HUGGING FACE CONFIG (STABLE SETUP)
# --------------------------------------------------

HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# ✅ Use ONE model consistently (API + Local)
HUGGINGFACE_MODEL = os.getenv(
    "HUGGINGFACE_MODEL",
    "Salesforce/blip-image-captioning-base"
)

# --------------------------------------------------
# LOCAL MODEL CONFIG
# --------------------------------------------------

USE_LOCAL_MODEL = os.getenv("USE_LOCAL_MODEL", "false").lower() == "true"

LOCAL_MODEL_NAME = os.getenv(
    "LOCAL_MODEL_NAME",
    "Salesforce/blip-image-captioning-base"
)

# --------------------------------------------------
# IMAGE PROCESSING LIMITS
# --------------------------------------------------

MAX_IMAGES_PER_PRODUCT = int(os.getenv("MAX_IMAGES_PER_PRODUCT", "10"))
MAX_IMAGE_SIZE_MB = int(os.getenv("MAX_IMAGE_SIZE_MB", "10"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))

# --------------------------------------------------
# CACHE
# --------------------------------------------------

ENABLE_CACHE = os.getenv("ENABLE_CACHE", "false").lower() == "true"


# --------------------------------------------------
# Optional BLIP captioning
# --------------------------------------------------

USE_BLIP = True
BLIP_MODEL_NAME = "Salesforce/blip-image-captioning-base"