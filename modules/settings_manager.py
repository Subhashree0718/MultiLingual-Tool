"""
Settings Manager - Handle user preferences persistence
"""
import json
import os
from pathlib import Path
from config import SETTINGS_FILE, DEFAULT_SETTINGS, SUPPORTED_LANGUAGES


class SettingsManager:
    def __init__(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.load_settings()
    
    def load_settings(self):
        """Load settings from JSON file"""
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
        except Exception as e:
            print(f"Error loading settings: {e}")
            # Use default settings if load fails
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            # Ensure resources directory exists
            SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
            
            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set a setting value and save"""
        self.settings[key] = value
        self.save_settings()
    
    def get_target_language(self):
        """Get the target language code"""
        return self.settings.get('target_language', 'en')
    
    def set_target_language(self, lang_code):
        """Set the target language"""
        if lang_code in SUPPORTED_LANGUAGES:
            self.set('target_language', lang_code)
            return True
        return False
    
    def get_hotkey(self):
        """Get the keyboard shortcut"""
        return self.settings.get('hotkey', 'ctrl+shift+t')
    
    def set_hotkey(self, hotkey):
        """Set the keyboard shortcut"""
        self.set('hotkey', hotkey)
    
    def get_tesseract_path(self):
        """Get the Tesseract executable path"""
        return self.settings.get('tesseract_path', '')
    
    def set_tesseract_path(self, path):
        """Set the Tesseract executable path"""
        self.set('tesseract_path', path)
    
    def get_theme(self):
        """Get the UI theme"""
        return self.settings.get('theme', 'dark')
    
    def set_theme(self, theme):
        """Set the UI theme"""
        if theme in ['light', 'dark']:
            self.set('theme', theme)
