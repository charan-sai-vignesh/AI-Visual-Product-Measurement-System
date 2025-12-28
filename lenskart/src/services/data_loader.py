"""Data loader for product images dataset."""
import pandas as pd
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ProductDataLoader:
    """Loads product data from Excel file."""
    
    def __init__(self, excel_path: str = "A1.0_data_product_images.xlsx"):
        """
        Initialize the data loader.
        
        Args:
            excel_path: Path to the Excel file
        """
        self.excel_path = excel_path
        self.df: Optional[pd.DataFrame] = None
        self._load_data()
    
    def _load_data(self):
        """Load data from Excel file."""
        try:
            # Try to read the file
            self.df = pd.read_excel(self.excel_path)
            logger.info(f"Loaded {len(self.df)} products from {self.excel_path}")
        except PermissionError as e:
            logger.error(f"Permission denied: The Excel file is likely open in another program (Excel). Please close it and restart the server.")
            logger.error(f"File path: {self.excel_path}")
            # Don't raise - allow server to start but dataset won't be available
            self.df = None
        except FileNotFoundError as e:
            logger.error(f"File not found: {self.excel_path}. Please ensure the file exists in the project root.")
            self.df = None
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            self.df = None
    
    def get_product_images(self, product_id: int) -> List[str]:
        """
        Get all image URLs for a product.
        
        Args:
            product_id: Product ID
            
        Returns:
            List of image URLs (non-null)
        """
        if self.df is None:
            logger.warning("Dataset not loaded. Please close the Excel file if it's open and restart the server.")
            return []
        
        product_row = self.df[self.df['Product Id'] == product_id]
        if product_row.empty:
            return []
        
        image_urls = []
        # Get all image columns (Image1, Image2, ...)
        for col in self.df.columns:
            if col.startswith('Image') and col != 'Image Count':
                url = product_row[col].iloc[0]
                if pd.notna(url) and url:
                    image_urls.append(str(url).strip())
        
        return image_urls
    
    def get_all_products(self) -> List[Dict]:
        """
        Get all products with their image URLs.
        
        Returns:
            List of dictionaries with product info and image URLs
        """
        if self.df is None:
            return []
        
        products = []
        for _, row in self.df.iterrows():
            product_id = int(row['Product Id'])
            category = str(row['Category'])
            image_count = int(row['Image Count'])
            
            image_urls = []
            for col in self.df.columns:
                if col.startswith('Image') and col != 'Image Count':
                    url = row[col]
                    if pd.notna(url) and url:
                        image_urls.append(str(url).strip())
            
            products.append({
                'product_id': product_id,
                'category': category,
                'image_count': image_count,
                'image_urls': image_urls
            })
        
        return products
    
    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        """
        Get a single product by ID.
        
        Args:
            product_id: Product ID
            
        Returns:
            Product dictionary or None if not found
        """
        products = self.get_all_products()
        for product in products:
            if product['product_id'] == product_id:
                return product
        return None
    
    def get_random_products(self, n: int = 5) -> List[Dict]:
        """
        Get random products for testing.
        
        Args:
            n: Number of products to return
            
        Returns:
            List of product dictionaries
        """
        products = self.get_all_products()
        import random
        return random.sample(products, min(n, len(products)))

