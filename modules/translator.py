"""
Translator - Language detection and translation service
"""
from googletrans import Translator
from langdetect import detect, LangDetectException
import time
from config import (
    SUPPORTED_LANGUAGES, ERROR_TRANSLATION_FAILED,
    TRANSLATION_TIMEOUT, MAX_RETRY_ATTEMPTS
)

try:
    from modules.ai_translator import AITranslator
    AI_TRANSLATION_AVAILABLE = True
except ImportError:
    AI_TRANSLATION_AVAILABLE = False
    print("[WARN] AI translation not available")


class TranslationService:
    def __init__(self, use_ai=False, api_key=None):
        self.translator = Translator()
        self.use_ai = use_ai and AI_TRANSLATION_AVAILABLE
        self.ai_translator = None
        
        if self.use_ai:
            self.ai_translator = AITranslator(api_key)
            if not self.ai_translator.model:
                print("[INFO] AI translation disabled, using basic translation")
                self.use_ai = False
    
    def detect_language(self, text):
        """
        Detect the language of the input text
        
        Args:
            text: String to detect language from
        
        Returns:
            tuple: (success: bool, lang_code: str or error: str)
        """
        try:
            # Use langdetect for more accurate detection
            lang_code = detect(text)
            
            # Get language name if supported
            lang_name = SUPPORTED_LANGUAGES.get(lang_code, "Unknown")
            
            return True, lang_code, lang_name
        except LangDetectException as e:
            print(f"Language detection error: {e}")
            # Default to English if detection fails
            return True, 'en', 'English (default)'
        except Exception as e:
            print(f"Error detecting language: {e}")
            return False, None, str(e)
    
    def translate_text(self, text, target_lang='en', source_lang='auto'):
        """
        Translate text to target language
        
        Args:
            text: Text to translate
            target_lang: Target language code (ISO 639-1)
            source_lang: Source language code (default: 'auto')
        
        Returns:
            tuple: (success: bool, result: dict or error: str)
            result dict contains: {
                'translated_text': str,
                'source_lang': str,
                'source_lang_name': str,
                'target_lang': str,
                'target_lang_name': str
            }
        """
        # Try multiple times in case of network issues
        for attempt in range(MAX_RETRY_ATTEMPTS):
            try:
                # Perform translation
                translation = self.translator.translate(
                    text,
                    dest=target_lang,
                    src=source_lang
                )
                
                # Get language names
                source_lang_code = translation.src
                source_lang_name = SUPPORTED_LANGUAGES.get(
                    source_lang_code, 
                    source_lang_code.upper()
                )
                target_lang_name = SUPPORTED_LANGUAGES.get(
                    target_lang,
                    target_lang.upper()
                )
                
                result = {
                    'translated_text': translation.text,
                    'original_text': text,
                    'source_lang': source_lang_code,
                    'source_lang_name': source_lang_name,
                    'target_lang': target_lang,
                    'target_lang_name': target_lang_name,
                    'method': 'Basic'
                }
                
                return True, result
                
            except Exception as e:
                print(f"Translation attempt {attempt + 1} failed: {e}")
                if attempt < MAX_RETRY_ATTEMPTS - 1:
                    time.sleep(1)  # Wait before retry
                continue
        
        # All attempts failed
        return False, ERROR_TRANSLATION_FAILED
    
    def translate_with_detection(self, text, target_lang='en'):
        """
        Detect language and translate in one call
        Uses AI translation if enabled, otherwise basic translation
        Falls back to basic translation if AI fails
        
        Args:
            text: Text to translate
            target_lang: Target language code
        
        Returns:
            tuple: (success: bool, result: dict or error: str)
        """
        # Try AI translation if enabled
        if self.use_ai and self.ai_translator:
            print("[INFO] Attempting AI translation (context-aware)")
            success, result = self.ai_translator.translate_with_context(text, target_lang)
            
            # If AI succeeds, return it
            if success:
                return success, result
            
            # If AI fails, log it and fall back to basic translation
            print(f"[WARN] AI translation failed, falling back to basic translation")
            print(f"[WARN] Reason: {result}")
        
        # Use basic translation (either by choice or as fallback)
        print("[INFO] Using basic translation")
        
        # First detect the language
        detect_success, source_lang, source_name = self.detect_language(text)
        
        if not detect_success:
            # Even if detection fails, try translation with auto-detect
            source_lang = 'auto'
        
        # Check if source and target are the same
        if source_lang == target_lang:
            return True, {
                'translated_text': text,
                'original_text': text,
                'source_lang': source_lang,
                'source_lang_name': SUPPORTED_LANGUAGES.get(source_lang, source_lang),
                'target_lang': target_lang,
                'target_lang_name': SUPPORTED_LANGUAGES.get(target_lang, target_lang),
                'note': 'Source and target languages are the same'
            }
        
        # Perform translation
        return self.translate_text(text, target_lang, source_lang)
