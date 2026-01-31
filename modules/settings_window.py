"""
Settings Window - UI for user preferences
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QComboBox, QLineEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from config import SUPPORTED_LANGUAGES
import os


class SettingsWindow(QWidget):
    settings_saved = pyqtSignal()
    
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the settings window UI"""
        self.setWindowTitle("Screen Translator - Settings")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Settings")
        title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Target Language
        lang_layout = QVBoxLayout()
        lang_label = QLabel("Target Language:")
        lang_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        lang_layout.addWidget(lang_label)
        
        self.language_combo = QComboBox()
        for code, name in SUPPORTED_LANGUAGES.items():
            self.language_combo.addItem(name, code)
        
        # Set current language
        current_lang = self.settings_manager.get_target_language()
        index = self.language_combo.findData(current_lang)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
        
        lang_layout.addWidget(self.language_combo)
        layout.addLayout(lang_layout)
        
        # Hotkey
        hotkey_layout = QVBoxLayout()
        hotkey_label = QLabel("Keyboard Shortcut:")
        hotkey_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        hotkey_layout.addWidget(hotkey_label)
        
        self.hotkey_input = QLineEdit()
        self.hotkey_input.setText(self.settings_manager.get_hotkey())
        self.hotkey_input.setPlaceholderText("e.g., ctrl+shift+t")
        hotkey_layout.addWidget(self.hotkey_input)
        
        help_label = QLabel("Format: ctrl+shift+t or ctrl+alt+t")
        help_label.setStyleSheet("color: gray; font-size: 9pt;")
        hotkey_layout.addWidget(help_label)
        layout.addLayout(hotkey_layout)
        
        # Tesseract Path
        tesseract_layout = QVBoxLayout()
        tesseract_label = QLabel("Tesseract OCR Path:")
        tesseract_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        tesseract_layout.addWidget(tesseract_label)
        
        path_layout = QHBoxLayout()
        self.tesseract_path_input = QLineEdit()
        self.tesseract_path_input.setText(self.settings_manager.get_tesseract_path())
        self.tesseract_path_input.setPlaceholderText("C:\\Program Files\\Tesseract-OCR\\tesseract.exe")
        path_layout.addWidget(self.tesseract_path_input)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_tesseract)
        path_layout.addWidget(browse_btn)
        
        tesseract_layout.addLayout(path_layout)
        
        install_label = QLabel(
            "Download Tesseract from: "
            '<a href="https://github.com/UB-Mannheim/tesseract/wiki">GitHub</a>'
        )
        install_label.setOpenExternalLinks(True)
        install_label.setStyleSheet("color: #3daee9; font-size: 9pt;")
        tesseract_layout.addWidget(install_label)
        layout.addLayout(tesseract_layout)
        
        # Spacer
        layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Save")
        save_btn.setMinimumWidth(100)
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumWidth(100)
        cancel_btn.clicked.connect(self.close)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Apply styling
        self.apply_dark_theme()
    
    def apply_dark_theme(self):
        """Apply dark theme styling"""
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QLabel {
                color: #ffffff;
            }
            QComboBox, QLineEdit {
                background-color: #1e1e1e;
                border: 1px solid #3daee9;
                border-radius: 4px;
                padding: 8px;
                color: #ffffff;
            }
            QComboBox:hover, QLineEdit:hover {
                border: 1px solid #45b8f5;
            }
            QComboBox::drop-down {
                border: none;
                padding: 5px;
            }
            QPushButton {
                background-color: #3daee9;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45b8f5;
            }
            QPushButton:pressed {
                background-color: #2a8ec4;
            }
        """)
    
    def browse_tesseract(self):
        """Browse for Tesseract executable"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Tesseract Executable",
            "C:\\Program Files",
            "Executable Files (*.exe)"
        )
        
        if file_path:
            self.tesseract_path_input.setText(file_path)
    
    def save_settings(self):
        """Save settings and close"""
        # Get values
        target_lang = self.language_combo.currentData()
        hotkey = self.hotkey_input.text().strip()
        tesseract_path = self.tesseract_path_input.text().strip()
        
        # Validate
        if not hotkey:
            QMessageBox.warning(self, "Invalid Input", "Please enter a hotkey.")
            return
        
        if not tesseract_path or not os.path.exists(tesseract_path):
            result = QMessageBox.question(
                self,
                "Tesseract Not Found",
                "Tesseract path is invalid or not found. Save anyway?",
                QMessageBox.Yes | QMessageBox.No
            )
            if result == QMessageBox.No:
                return
        
        # Save settings
        self.settings_manager.set_target_language(target_lang)
        self.settings_manager.set_hotkey(hotkey)
        self.settings_manager.set_tesseract_path(tesseract_path)
        
        # Emit signal
        self.settings_saved.emit()
        
        # Show confirmation
        QMessageBox.information(
            self,
            "Settings Saved",
            "Settings have been saved successfully!\n\nRestart the application for hotkey changes to take effect."
        )
        
        self.close()
