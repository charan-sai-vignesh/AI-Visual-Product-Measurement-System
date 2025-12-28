"""Main FastAPI application."""
import logging
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from src.models.schemas import AnalysisRequest, MeasurementResult, ErrorResponse
from src.services.product_analyzer import ProductAnalyzer
from src.services.data_loader import ProductDataLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Visual Product Measurement System",
    description="Analyze product images and extract structured visual measurements",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
analyzer = ProductAnalyzer()
data_loader = ProductDataLoader()

# Serve static files (frontend)
static_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
async def root():
    """Root endpoint - serve frontend."""
    frontend_path = os.path.join(static_dir, "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "AI-Powered Visual Product Measurement System API", "status": "running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/api/analyze", response_model=MeasurementResult)
async def analyze_images(request: AnalysisRequest):
    """
    Analyze product images and return measurements.
    
    Args:
        request: AnalysisRequest with image URLs
        
    Returns:
        MeasurementResult with all measurements
    """
    try:
        if not request.image_urls or len(request.image_urls) == 0:
            raise HTTPException(status_code=400, detail="At least one image URL is required")
        
        result = await analyzer.analyze_product(
            image_urls=request.image_urls,
            product_id=request.product_id
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error in analyze endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/products")
async def get_products():
    """Get all products from the dataset."""
    try:
        products = data_loader.get_all_products()
        return {"products": products, "count": len(products)}
    except Exception as e:
        logger.error(f"Error getting products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/products/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID."""
    try:
        product = data_loader.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        return product
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/products/{product_id}/analyze", response_model=MeasurementResult)
async def analyze_product_by_id(product_id: int):
    """
    Analyze a product from the dataset by its ID.
    
    Args:
        product_id: Product ID from the dataset
        
    Returns:
        MeasurementResult with all measurements
    """
    try:
        product = data_loader.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
        
        result = await analyzer.analyze_product(
            image_urls=product['image_urls'],
            product_id=str(product['product_id'])
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing product: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sample-products")
async def get_sample_products():
    """Get random sample products for testing."""
    try:
        samples = data_loader.get_random_products(n=5)
        return {"products": samples, "count": len(samples)}
    except Exception as e:
        logger.error(f"Error getting sample products: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))




