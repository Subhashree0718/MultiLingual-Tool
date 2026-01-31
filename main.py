"""
Screen Translator - Main Application
A Windows desktop tool for translating on-screen text
"""
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon
from PyQt5.QtCore import QObject, pyqtSlot
from modules.tray_manager import TrayManager
from modules.settings_manager import SettingsManager
from modules.settings_window import SettingsWindow
from modules.screen_capture import ScreenCapture
from modules.ocr_engine import OCREngine
from modules.translator import TranslationService
from modules.popup_window import TranslationPopup
from modules.hotkey_handler import HotkeyHandler
from modules.caption_window import LiveCaptionWindow
from modules.video_translation import VideoTranslationService
from config import APP_NAME, APP_VERSION


class ScreenTranslatorApp(QObject):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.app.setQuitOnLastWindowClosed(False)  # Keep running when windows close
        
        # Initialize components
        self.settings_manager = SettingsManager()
        self.tray_manager = TrayManager(app)
        print(f"[OK] {APP_NAME} initialized")
        self.ocr_engine = None
        
        # Initialize translator with AI if enabled
        use_ai = self.settings_manager.get('use_ai_translation', True)
        api_key = self.settings_manager.get('gemini_api_key', None)
        self.translator = TranslationService(use_ai=use_ai, api_key=api_key)
        
        self.hotkey_handler = None
        self.settings_window = None
        self.capture_overlay = None
        self.popup = None
        
        # Video translation components
        self.caption_window = None
        self.video_translation = None
        
        # Setup
        self.setup_ocr()
        self.setup_video_translation()
        self.setup_connections()
        self.setup_hotkey()
        
        # Show startup message
        self.tray_manager.show_message(
            APP_NAME,
            f"{APP_NAME} v{APP_VERSION} is running.\nPress {self.settings_manager.get_hotkey()} to translate."
        )
    
    def setup_ocr(self):
        """Initialize OCR engine"""
        tesseract_path = self.settings_manager.get_tesseract_path()
        self.ocr_engine = OCREngine(tesseract_path)
        
        # Test Tesseract installation
        success, message = self.ocr_engine.test_installation()
        if not success:
            self.tray_manager.show_message(
                "Tesseract Not Found",
                "Please install Tesseract OCR and configure the path in Settings.",
                self.tray_manager.tray_icon.MessageIcon.Warning
            )
    
    
    def setup_video_translation(self):
        """Initialize video translation components"""
        try:
            # Create caption window
            self.caption_window = LiveCaptionWindow()
            
            # Create video translation service
            target_lang = self.settings_manager.get_target_language()
            self.video_translation = VideoTranslationService(
                translator=self.translator,
                target_language=target_lang
            )
            
            # Connect signals
            self.video_translation.caption_ready.connect(self.on_caption_ready)
            self.video_translation.error_occurred.connect(self.on_video_error)
            
            print("[OK] Video translation initialized")
        except Exception as e:
            print(f"[WARN] Video translation not available: {e}")
            self.video_translation = None
    
    def setup_connections(self):
        """Setup signal-slot connections"""
        self.tray_manager.translate_requested.connect(self.start_translation)
        self.tray_manager.settings_requested.connect(self.show_settings)
        self.tray_manager.exit_requested.connect(self.exit_app)
        self.tray_manager.live_captions_requested.connect(self.toggle_live_captions)
    
    def setup_hotkey(self):
        """Setup global hotkey"""
        hotkey = self.settings_manager.get_hotkey()
        # Convert hotkey format (ctrl+shift+t -> <ctrl>+<shift>+t)
        formatted_hotkey = self.format_hotkey(hotkey)
        
        self.hotkey_handler = HotkeyHandler(formatted_hotkey)
        self.hotkey_handler.hotkey_pressed.connect(self.start_translation)
        self.hotkey_handler.start()
    
    def format_hotkey(self, hotkey):
        """Format hotkey for pynput"""
        # Only wrap modifier keys in angle brackets
        modifiers = {'ctrl', 'alt', 'shift', 'win', 'cmd'}
        parts = hotkey.lower().split('+')
        formatted_parts = []
        for part in parts:
            if part in modifiers:
                formatted_parts.append(f"<{part}>")
            else:
                formatted_parts.append(part)
        return '+'.join(formatted_parts)
    
    @pyqtSlot()
    def start_translation(self):
        """Start the translation process"""
        print("Starting translation...")
        
        # Check if OCR is available
        success, message = self.ocr_engine.test_installation()
        if not success:
            self.tray_manager.show_message(
                "Error",
                "Tesseract OCR is not configured. Please check Settings.",
                self.tray_manager.tray_icon.Critical
            )
            return
        
        # Show screen capture overlay
        self.capture_overlay = ScreenCapture.capture_region(self.on_region_captured)
    
    def on_region_captured(self, image):
        """Handle captured screen region"""
        print("Region captured, extracting text...")
        
        # Extract text using OCR
        success, result = self.ocr_engine.extract_text(image)
        
        if not success:
            self.tray_manager.show_message(
                "OCR Error",
                result,  # Error message
                self.tray_manager.tray_icon.MessageIcon.Warning
            )
            return
        
        # Get extracted text
        extracted_text = result
        print(f"Extracted text: {extracted_text[:100]}...")
        
        # Translate text
        self.translate_and_display(extracted_text)
    
    def translate_and_display(self, text):
        """Translate text and display result"""
        print("Translating...")
        
        # Get target language
        target_lang = self.settings_manager.get_target_language()
        
        # Perform translation
        success, result = self.translator.translate_with_detection(text, target_lang)
        
        if not success:
            self.tray_manager.show_message(
                "Translation Error",
                result,  # Error message
                self.tray_manager.tray_icon.MessageIcon.Warning
            )
            return
        
        # Display translation popup
        print("Displaying translation...")
        self.popup = TranslationPopup(result)
        self.popup.show()
    
    @pyqtSlot()
    def show_settings(self):
        """Show settings window"""
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = SettingsWindow(self.settings_manager)
            self.settings_window.settings_saved.connect(self.on_settings_saved)
        
        self.settings_window.show()
        self.settings_window.activateWindow()
    
    @pyqtSlot()
    def on_settings_saved(self):
        """Handle settings saved"""
        # Reinitialize OCR with new Tesseract path
        tesseract_path = self.settings_manager.get_tesseract_path()
        self.ocr_engine = OCREngine(tesseract_path)
        
        # Update hotkey
        hotkey = self.settings_manager.get_hotkey()
        formatted_hotkey = self.format_hotkey(hotkey)
        if self.hotkey_handler:
            self.hotkey_handler.update_hotkey(formatted_hotkey)
    
    
    @pyqtSlot(str, str)
    def on_caption_ready(self, original_text, translated_text):
        """Handle new caption from video translation"""
        # Show translated caption
        if self.caption_window:
            self.caption_window.update_caption(translated_text)
            if not self.caption_window.isVisible():
                self.caption_window.show_caption(translated_text, duration=0)  # 0 = stay visible
    
    @pyqtSlot(str)
    def on_video_error(self, error_message):
        """Handle video translation error"""
        print(f"[ERROR] Video translation: {error_message}")
        self.tray_manager.show_message(
            "Video Translation Error",
            error_message,
            self.tray_manager.tray_icon.Critical
        )
    
    @pyqtSlot()
    def toggle_live_captions(self):
        """Toggle live caption mode on/off"""
        if not self.video_translation:
            self.tray_manager.show_message(
                "Not Available",
                "Video translation is not available. Please install required dependencies.",
                self.tray_manager.tray_icon.Warning
            )
            return
        
        if self.video_translation.is_active:
            # Stop live captions
            self.video_translation.stop()
            if self.caption_window:
                self.caption_window.hide_caption()
            self.tray_manager.show_message(
                "Live Captions",
                "Live captions stopped"
            )
        else:
            # Start live captions
            if self.video_translation.start():
                self.tray_manager.show_message(
                    "Live Captions",
                    "Live captions started! Audio will be translated in real-time."
                )
            else:
                self.tray_manager.show_message(
                    "Error",
                    "Failed to start live captions",
                    self.tray_manager.tray_icon.Critical
                )
    
    @pyqtSlot()
    def exit_app(self):
        """Exit the application"""
        # Stop video translation if active
        if self.video_translation and self.video_translation.is_active:
            self.video_translation.stop()
        
        # Stop hotkey listener
        if self.hotkey_handler:
            self.hotkey_handler.stop()
        
        # Hide tray icon
        self.tray_manager.hide()
        
        # Quit application
        self.app.quit()


def main():
    """Main entry point"""
    print("[INFO] Starting Screen Translator...")
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(APP_VERSION)
    
    print("[INFO] Qt Application created")
    
    # Check if system tray is available
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("[ERROR] System tray is not available on this system!")
        QMessageBox.critical(
            None,
            "System Tray Error",
            "System tray is not available on this system."
        )
        sys.exit(1)
    
    print("[INFO] System tray is available")
    
    # Create and run application
    print("[INFO] Initializing Screen Translator App...")
    translator_app = ScreenTranslatorApp(app)
    
    print("[INFO] Application initialized successfully!")
    print("[INFO] Look for the tray icon near the clock in your taskbar")
    print("[INFO] Press Ctrl+C here to exit")
    
    # Run event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
