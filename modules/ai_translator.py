"""
AI Translator - Context-aware natural translation using Google Gemini
"""
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("[WARN] Google Gemini AI not available. Install: pip install google-generativeai")

from langdetect import detect, LangDetectException
from config import SUPPORTED_LANGUAGES


class AITranslator:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.model = None
        
        if GEMINI_AVAILABLE and api_key:
            try:
                genai.configure(api_key=api_key)
                # Try multiple model names for compatibility
                try:
                    self.model = genai.GenerativeModel('gemini-1.5-pro')
                    print("[OK] Gemini AI translator initialized with gemini-1.5-pro")
                except:
                    try:
                        self.model = genai.GenerativeModel('gemini-pro')
                        print("[OK] Gemini AI translator initialized with gemini-pro")
                    except:
                        print("[WARN] No compatible Gemini model found")
                        self.model = None
            except Exception as e:
                print(f"[WARN] Failed to initialize Gemini: {e}")
                self.model = None
    
    def detect_language(self, text):
        """Detect the language of the input text"""
        try:
            lang_code = detect(text)
            lang_name = SUPPORTED_LANGUAGES.get(lang_code, "Unknown")
            return True, lang_code, lang_name
        except LangDetectException:
            return True, 'en', 'English (default)'
        except Exception as e:
            return False, None, str(e)
    
    def translate_with_context(self, text, target_lang='en'):
        """
        AI-powered translation that understands context and rewrites naturally
        
        Args:
            text: Text to translate
            target_lang: Target language code
        
        Returns:
            tuple: (success: bool, result: dict or error: str)
        """
        # Detect source language
        detect_success, source_lang, source_name = self.detect_language(text)
        
        if not detect_success:
            source_lang = 'auto'
            source_name = 'Auto-detected'
        
        target_lang_name = SUPPORTED_LANGUAGES.get(target_lang, target_lang.upper())
        
        # Check if AI is available
        if not self.model:
            return False, "Gemini AI not configured. Using basic translation."
        
        # Check if source and target are the same
        if source_lang == target_lang:
            return True, {
                'translated_text': text,
                'original_text': text,
                'source_lang': source_lang,
                'source_lang_name': source_name,
                'target_lang': target_lang,
                'target_lang_name': target_lang_name,
                'note': 'Source and target languages are the same'
            }
        
        try:
            # Detect if it's a single word or a sentence
            word_count = len(text.strip().split())
            is_single_word = word_count == 1
            
            # Create AI prompt based on input type
            if is_single_word:
                # For single words: Direct translation or transliteration
                prompt = f"""Translate this single word to {target_lang_name}.

Instructions:
- If it's a common word: provide the {target_lang_name} translation
- If it's a proper noun (name, place, food): transliterate it (write in {target_lang_name} script)
- Provide ONLY the translated/transliterated word, nothing else

Word: {text}

{target_lang_name}:"""
            else:
                # For sentences: Contextual understanding and natural rewriting
                prompt = f"""You are an expert translator. Understand the meaning of this text and rewrite it naturally in {target_lang_name}.

INSTRUCTIONS:
1. Understand the full meaning and context
2. Rewrite it naturally as a native {target_lang_name} speaker would say it
3. Don't translate word-for-word
4. Preserve the tone and intent
5. For proper nouns (names, places, food items): transliterate them
6. Provide ONLY the natural translation, no explanations

Text: {text}

Natural {target_lang_name} translation:"""

            # Generate translation
            response = self.model.generate_content(prompt)
            translated_text = response.text.strip()
            
            result = {
                'translated_text': translated_text,
                'original_text': text,
                'source_lang': source_lang,
                'source_lang_name': source_name,
                'target_lang': target_lang,
                'target_lang_name': target_lang_name,
                'method': f'AI ({"Word" if is_single_word else "Sentence"})'
            }
            
            return True, result
            
        except Exception as e:
            print(f"[ERROR] AI translation failed: {e}")
            return False, f"AI translation failed: {str(e)}"
