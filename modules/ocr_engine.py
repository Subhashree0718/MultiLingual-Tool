"""
OCR Engine - Tesseract integration for text extraction
"""
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
from config import (
    OCR_LANGUAGES, OCR_CONFIG, ERROR_OCR_FAILED, 
    ERROR_TESSERACT_NOT_FOUND, TESSERACT_POSSIBLE_PATHS
)


class OCREngine:
    def __init__(self, tesseract_path=None):
        """Initialize OCR engine with Tesseract path"""
        self.setup_tesseract(tesseract_path)
    
    def setup_tesseract(self, tesseract_path=None):
        """Configure Tesseract executable path"""
        if tesseract_path and os.path.exists(tesseract_path):
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            return True
        
        # Try to find Tesseract in common locations
        for path in TESSERACT_POSSIBLE_PATHS:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return True
        
        return False
    
    def preprocess_image(self, image):
        """Enhance image for better OCR accuracy"""
        try:
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to grayscale
            image = image.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Apply slight blur to reduce noise
            image = image.filter(ImageFilter.MedianFilter(size=1))
            
            return image
        except Exception as e:
            print(f"Error preprocessing image: {e}")
            return image
    
    def extract_text(self, image):
        """
        Extract text from image using Tesseract OCR
        
        Args:
            image: PIL Image object
        
        Returns:
            tuple: (success: bool, text: str or error_message: str)
        """
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image)
            
            # Perform OCR with multiple language support
            text = pytesseract.image_to_string(
                processed_image,
                lang=OCR_LANGUAGES,
                config=OCR_CONFIG
            )
            
            # Clean up extracted text
            text = text.strip()
            
            if not text:
                return False, "No text detected in the selected area."
            
            return True, text
            
        except pytesseract.TesseractNotFoundError:
            return False, ERROR_TESSERACT_NOT_FOUND
        except Exception as e:
            print(f"OCR Error: {e}")
            return False, ERROR_OCR_FAILED
    
    def test_installation(self):
        """Test if Tesseract is properly installed"""
        try:
            version = pytesseract.get_tesseract_version()
            return True, f"Tesseract {version} found"
        except pytesseract.TesseractNotFoundError:
            return False, ERROR_TESSERACT_NOT_FOUND
        except Exception as e:
            return False, f"Error: {e}"
