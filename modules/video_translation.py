"""
Video Translation Service - Coordinates audio capture, speech recognition, and caption display
"""
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from modules.audio_capture import AudioCapture
from modules.speech_recognition import RealtimeSpeechRecognizer


class VideoTranslationService(QObject):
    # Signals
    caption_ready = pyqtSignal(str, str)  # (original_text, translated_text)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, translator, target_language='ta'):
        super().__init__()
        self.translator = translator
        self.target_language = target_language
        self.is_active = False
        
        # Components
        self.audio_capture = None
        self.speech_recognizer = None
        self.worker_thread = None
        
    def start(self):
        """Start video translation service"""
        if self.is_active:
            print("[WARN] Video translation already active")
            return False
        
        try:
            print("[INFO] Starting video translation service...")
            
            # Initialize audio capture
            self.audio_capture = AudioCapture(sample_rate=16000, channels=1)
            
            # Initialize speech recognizer
            self.speech_recognizer = RealtimeSpeechRecognizer(
                model_size='tiny',  # Use tiny for speed
                language=None  # Auto-detect
            )
            
            # Load Whisper model in separate thread to avoid blocking
            self.worker_thread = QThread()
            
            # Load model
            print("[INFO] Loading Whisper model (this may take a moment)...")
            if not self.speech_recognizer.load_model():
                self.error_occurred.emit("Failed to load speech recognition model")
                return False
            
            # Start audio capture with callback
            if not self.audio_capture.start_recording(self._on_audio_chunk):
                self.error_occurred.emit("Failed to start audio capture")
                return False
            
            self.is_active = True
            print("[OK] Video translation service started")
            return True
            
        except Exception as e:
            error_msg = f"Failed to start video translation: {e}"
            print(f"[ERROR] {error_msg}")
            self.error_occurred.emit(error_msg)
            return False
    
    def stop(self):
        """Stop video translation service"""
        if not self.is_active:
            return
        
        print("[INFO] Stopping video translation service...")
        
        # Stop audio capture
        if self.audio_capture:
            self.audio_capture.stop_recording()
        
        # Clear speech recognizer buffer
        if self.speech_recognizer:
            self.speech_recognizer.clear_buffer()
        
        self.is_active = False
        print("[OK] Video translation service stopped")
    
    def _on_audio_chunk(self, audio_data):
        """
        Callback when new audio chunk is available
        
        Args:
            audio_data: numpy array of audio samples
        """
        if not self.is_active:
            return
        
        try:
            # Add audio to recognizer
            result = self.speech_recognizer.add_audio(audio_data)
            
            # If we have a transcription
            if result and result.get('text'):
                original_text = result['text']
                detected_lang = result.get('language', 'unknown')
                
                print(f"[STT] Detected ({detected_lang}): {original_text}")
                
                # Translate the text
                success, translation_result = self.translator.translate_with_detection(
                    original_text,
                    self.target_language
                )
                
                if success:
                    translated_text = translation_result.get('translated_text', '')
                    print(f"[TRANS] Translated: {translated_text}")
                    
                    # Emit caption signal
                    self.caption_ready.emit(original_text, translated_text)
                else:
                    print(f"[WARN] Translation failed: {translation_result}")
                    
        except Exception as e:
            print(f"[ERROR] Audio processing error: {e}")
    
    def set_target_language(self, language_code):
        """Change target translation language"""
        self.target_language = language_code
        print(f"[INFO] Target language changed to: {language_code}")

    def start_browser_mode(self):
        """Start browser audio translation"""
        if self.is_active:
            print("[WARN] Translation already active")
            return False

        try:
            print("[INFO] Starting browser audio translation...")

            # Initialize recognizer
            self.speech_recognizer = RealtimeSpeechRecognizer(
                model_size="tiny",
                language=None
            )

            if not self.speech_recognizer.load_model():
                self.error_occurred.emit("Failed to load speech model")
                return False

            from modules.browser_audio_server import BrowserAudioServer
            import uvicorn
            import threading

            self.browser_server = BrowserAudioServer(
                self.speech_recognizer,
                self._on_browser_text
            )

            self.browser_thread = threading.Thread(
                target=lambda: uvicorn.run(
                    self.browser_server.app,
                    host="127.0.0.1",
                    port=8000,
                    log_level="warning"
                ),
                daemon=True
            )

            self.browser_thread.start()

            self.is_active = True
            print("[OK] Browser audio translation started")
            return True

        except Exception as e:
            self.error_occurred.emit(str(e))
            return False
    def _on_browser_text(self, result):
        """Handle transcription from browser audio"""
        original_text = result["text"]
        detected_lang = result.get("language", "unknown")

        print(f"[BROWSER STT] ({detected_lang}): {original_text}")

        success, translation_result = self.translator.translate_with_detection(
            original_text,
            self.target_language
        )

        if success:
            translated_text = translation_result.get("translated_text", "")
            self.caption_ready.emit(original_text, translated_text)
    def stop(self):
        if not self.is_active:
            return

        if self.audio_capture:
            self.audio_capture.stop_recording()

        if self.speech_recognizer:
            self.speech_recognizer.clear_buffer()

        self.is_active = False
        print("[OK] Translation stopped")
