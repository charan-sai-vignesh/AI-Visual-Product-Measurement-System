# AI-Powered Visual Product Measurement System

A system that analyzes product images (spectacles/eyeglasses) and extracts structured visual measurements using free/open-source vision AI models.

## Overview

This system analyzes product images and produces objective, observable visual measurements across multiple dimensions:

- **Visual Dimensions** (scored -5.0 to +5.0):
  - Gender Expression (Masculine → Feminine)
  - Visual Weight (Sleek/Light → Bold/Heavy)
  - Embellishment (Simple → Ornate)
  - Unconventionality (Classic → Avant-garde)
  - Formality (Casual → Formal)

- **Visual Attributes**:
  - Visible wirecore detection
  - Frame geometry classification
  - Transparency/opacity
  - Dominant colors
  - Visible textures
  - Suitability for kids

## Architecture

### System Components

1. **Data Loader** (`src/services/data_loader.py`)
   - Loads product data from Excel file
   - Extracts image URLs per product
   - Provides product lookup functionality

2. **Image Processor** (`src/services/image_processor.py`)
   - Downloads images from URLs
   - Validates image URLs
   - Extracts basic image metadata

3. **Vision Analyzer** (`src/services/vision_analyzer.py`)
   - Integrates with Hugging Face vision models (BLIP)
   - Supports both API and local model execution
   - Generates image descriptions

4. **Measurement Extractor** (`src/services/measurement_extractor.py`)
   - Extracts dimensional scores from analysis text
   - Detects visual attributes using keyword analysis
   - Structures measurements into schema format

5. **Product Analyzer** (`src/services/product_analyzer.py`)
   - Orchestrates the complete analysis pipeline
   - Handles multiple images per product
   - Aggregates results

6. **API Layer** (`src/api/main.py`)
   - FastAPI REST API
   - Endpoints for analysis and dataset access
   - Serves frontend interface

7. **Frontend** (`frontend/index.html`)
   - Web interface for image submission
   - Visual results display
   - Dataset browser

### Data Flow

```
Excel Dataset
     ↓
Data Loader
     ↓
Image URLs
     ↓
Image Processor (download & validation)
     ↓
Vision Analyzer (BLIP – local inference)
     ↓
Semantic captions
     ↓
Measurement Extractor (rule-based mapping)
     ↓
Structured JSON output

```

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip package manager

### Installation

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Ensure the dataset file is in the root directory**:
   - `A1.0_data_product_images.xlsx` should be in the project root

### Running the Application

1. **Start the server**:
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   
   ```bash
    python -m uvicorn src.api.main:app --reload
   ```

2. **Access the web interface**:
   - Open your browser and go to: `http://localhost:8000`
   - The API documentation is available at: `http://localhost:8000/docs`

## Usage

### Web Interface

1. **Analyze Custom Images**:
   - Go to the "Analyze Images" tab
   - Enter image URLs (one per line)
   - Optionally provide a Product ID
   - Click "Analyze Product"

2. **Analyze from Dataset**:
   - Go to the "Browse Dataset" tab
   - Click "Load Products" or "Load Sample Products"
   - Click on a product card to analyze it
   - Or use "Analyze from Dataset" with a Product ID

### API Endpoints

- `POST /api/analyze` - Analyze images from URLs
  ```json
  {
    "image_urls": ["https://example.com/image1.jpg"],
    "product_id": "optional-id"
  }
  ```

- `POST /api/products/{product_id}/analyze` - Analyze a product from the dataset

- `GET /api/products` - Get all products from dataset

- `GET /api/products/{product_id}` - Get specific product details

- `GET /api/sample-products` - Get random sample products

## Key Design Decisions

### 1. Free/Open-Source Models

- **Chosen**: Hugging Face BLIP (Bootstrapping Language-Image Pre-training) model
- **Reason**: Free tier available, good image captioning capabilities, no cost barriers
- **Alternative considered**: Local LLaVA model (requires GPU and more setup)

### 2. Measurement Extraction Approach

- **Chosen**: Rule-based keyword extraction from vision model outputs
- **Reason**: Simple, interpretable, doesn't require additional model training
- **Trade-off**: Less accurate than fine-tuned models, but sufficient for prototype

### 3. Architecture Pattern

- **Chosen**: Modular service-based architecture
- **Reason**: Separation of concerns, easy to test and extend
- **Benefits**: Can swap vision models or extraction logic independently

### 4. API Design

- **Chosen**: RESTful API with FastAPI
- **Reason**: Simple, fast, auto-documentation, async support
- **Response format**: Structured JSON following Pydantic schemas

### 5. Error Handling

- Graceful degradation when images fail to download
- Partial results if some images can't be analyzed
- Confidence scores to indicate result reliability

## Limitations

1. **Vision Model Accuracy**: 
   - Free BLIP model provides basic descriptions, not fine-tuned for product analysis
   - May miss subtle visual details

2. **Measurement Extraction**:
   - Keyword-based extraction is heuristic and may not capture all nuances
   - Scores are approximations based on text analysis

3. **Processing Speed**:
   - API-based models have rate limits on free tier
   - Local models require GPU for reasonable performance

4. **Image Quality**:
   - Results depend on image quality and clarity
   - May struggle with low-resolution or poorly lit images

5. **Domain Specificity**:
   - Currently optimized for spectacles/eyeglasses
   - Would need adjustments for other product types

## Future Improvements

1. **Better Vision Models**:
   - Fine-tune a vision model specifically for product analysis
   - Use multi-modal LLMs (e.g., GPT-4V, Claude Vision) when available

2. **Improved Measurement Extraction**:
   - Train a classifier for each dimension
   - Use few-shot learning with examples
   - Implement confidence intervals

3. **Performance Optimizations**:
   - Caching for repeated analyses
   - Batch processing support
   - Background job queue for large datasets

4. **Enhanced Attributes**:
   - Object detection for frame components
   - Color palette extraction using computer vision
   - Material classification

5. **User Experience**:
   - Image upload instead of URLs
   - Batch processing interface
   - Export results to CSV/JSON
   - Comparison view for multiple products

6. **Multiple Provider Support**:
   - Abstract vision model interface
   - Support for multiple AI providers with fallback logic
   - Model performance comparison

## Sample Input/Output

### Input
```json
{
  "image_urls": [
    "https://static5.lenskart.com/media/catalog/product/.../image1.jpg",
    "https://static5.lenskart.com/media/catalog/product/.../image2.jpg"
  ],
  "product_id": "231031"
}
```

### Output
```json
{
  "product_id": "231031",
  "image_urls": [...],
  "dimensions": {
    "gender_expression": 1.5,
    "visual_weight": -2.0,
    "embellishment": -1.0,
    "unconventionality": 0.5,
    "formality": 2.0
  },
  "attributes": {
    "visible_wirecore": false,
    "frame_geometry": "rectangular",
    "transparency_opacity": "opaque",
    "dominant_colors": ["Black", "Gold"],
    "visible_textures": ["Matte"],
    "suitable_for_kids": false
  },
  "metadata": {
    "image_format": "JPEG",
    "dimensions": {"width": 1325, "height": 636}
  },
  "confidence_score": 0.85
}
```


## Testing

To test the system:

1. Start the server
2. Use the web interface or API endpoints
3. Try analyzing a product from the dataset (e.g., Product ID: 231031)
4. Check the results for dimensions and attributes


