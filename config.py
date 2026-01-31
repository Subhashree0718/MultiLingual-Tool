"""
Configuration and constants for Screen Translator
"""
import os
from pathlib import Path

# Application Info
APP_NAME = "Screen Translator"
APP_VERSION = "1.0.0"

# Paths
BASE_DIR = Path(__file__).parent
RESOURCES_DIR = BASE_DIR / "resources"
SETTINGS_FILE = RESOURCES_DIR / "settings.json"

# Default Settings
DEFAULT_SETTINGS = {
    "target_language": "ta",
    "hotkey": "ctrl+shift+t",
    "theme": "dark",
    "tesseract_path": r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    "use_ai_translation": True,  # Use AI for natural translation
    "gemini_api_key": ""  # User can add their Gemini API key (optional)
}

# Supported Languages (ISO 639-1 codes)
SUPPORTED_LANGUAGES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "te": "Telugu",
    "ml": "Malayalam",
    "kn": "Kannada",
    "mr": "Marathi",
    "bn": "Bengali",
    "gu": "Gujarati",
    "pa": "Punjabi"
}

# Tesseract Language Codes (for OCR)
TESSERACT_LANG_CODES = {
    "en": "eng",
    "ta": "tam",
    "hi": "hin",
    "te": "tel",
    "ml": "mal",
    "kn": "kan",
    "mr": "mar",
    "bn": "ben",
    "gu": "guj",
    "pa": "pan"
}

# UI Constants
OVERLAY_OPACITY = 0.3
SELECTION_COLOR = "#00ff00"
SELECTION_WIDTH = 2
POPUP_WIDTH = 400
POPUP_MIN_HEIGHT = 150

# Error Messages
ERROR_NO_TEXT = "No readable text found in the selected area."
ERROR_OCR_FAILED = "Failed to extract text. Please try again."
ERROR_TRANSLATION_FAILED = "Translation failed. Please check your internet connection."
ERROR_TESSERACT_NOT_FOUND = "Tesseract OCR not found. Please install it first."

# Tesseract Default Paths (try multiple common locations)
TESSERACT_POSSIBLE_PATHS = [
    r"C:\Program Files\Tesseract-OCR\tesseract.exe",
    r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
    r"C:\Tesseract-OCR\tesseract.exe",
]

# OCR Settings
OCR_LANGUAGES = "+".join(TESSERACT_LANG_CODES.values())  # All supported languages
OCR_CONFIG = r'--oem 3 --psm 6'  # LSTM OCR Engine, Assume uniform block of text

# Translation Settings
TRANSLATION_TIMEOUT = 10  # seconds
MAX_RETRY_ATTEMPTS = 3

# Hotkey Settings
DEFAULT_HOTKEY = "<ctrl>+<shift>+t"
