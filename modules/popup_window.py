"""
Popup Window - Display translation results
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QHBoxLayout, QApplication
)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QCursor
from config import POPUP_WIDTH, POPUP_MIN_HEIGHT


class TranslationPopup(QWidget):
    def __init__(self, translation_result, position=None):
        super().__init__()
        self.translation_result = translation_result
        self.position = position
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the popup window UI"""
        # Window flags - frameless, always on top
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # Set window properties
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumWidth(POPUP_WIDTH)
        self.setMinimumHeight(POPUP_MIN_HEIGHT)
        
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Container widget (for styling)
        container = QWidget()
        container.setObjectName("container")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(15, 15, 15, 15)
        container_layout.setSpacing(10)
        
        # Title with language info
        source_lang = self.translation_result.get('source_lang_name', 'Unknown')
        target_lang = self.translation_result.get('target_lang_name', 'Unknown')
        title_text = f"{source_lang} → {target_lang}"
        
        title_label = QLabel(title_text)
        title_label.setObjectName("title")
        title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        container_layout.addWidget(title_label)
        
        # Translated text
        translated_text = self.translation_result.get('translated_text', '')
        text_label = QLabel(translated_text)
        text_label.setObjectName("translatedText")
        text_label.setFont(QFont("Segoe UI", 12))
        text_label.setWordWrap(True)
        text_label.setTextInteractionFlags(
            Qt.TextSelectableByMouse
        )
        container_layout.addWidget(text_label)
        
        # Original text (smaller, dimmed)
        original_text = self.translation_result.get('original_text', '')
        if len(original_text) > 100:
            original_text = original_text[:100] + "..."
        
        original_label = QLabel(f"Original: {original_text}")
        original_label.setObjectName("originalText")
        original_label.setFont(QFont("Segoe UI", 9))
        original_label.setWordWrap(True)
        container_layout.addWidget(original_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        copy_btn = QPushButton("Copy")
        copy_btn.setObjectName("copyButton")
        copy_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        copy_btn.clicked.connect(self.copy_to_clipboard)
        button_layout.addWidget(copy_btn)
        
        close_btn = QPushButton("Close")
        close_btn.setObjectName("closeButton")
        close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        close_btn.clicked.connect(self.close)
        button_layout.addWidget(close_btn)
        
        button_layout.addStretch()
        container_layout.addLayout(button_layout)
        
        layout.addWidget(container)
        self.setLayout(layout)
        
        # Apply dark theme styling
        self.apply_dark_theme()
        
        # Position the window
        self.position_window()
        
        # Auto-close after 30 seconds
        QTimer.singleShot(30000, self.close)
    
    def apply_dark_theme(self):
        """Apply dark theme styling"""
        self.setStyleSheet("""
            #container {
                background-color: #2b2b2b;
                border: 2px solid #3daee9;
                border-radius: 8px;
            }
            #title {
                color: #3daee9;
                padding: 5px 0;
            }
            #translatedText {
                color: #ffffff;
                padding: 10px 0;
                background-color: #1e1e1e;
                border-radius: 4px;
                padding: 10px;
            }
            #originalText {
                color: #888888;
                padding: 5px 0;
            }
            QPushButton {
                background-color: #3daee9;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45b8f5;
            }
            QPushButton:pressed {
                background-color: #2a8ec4;
            }
            #closeButton {
                background-color: #444444;
            }
            #closeButton:hover {
                background-color: #555555;
            }
        """)
    
    def position_window(self):
        """Position window near cursor or specified position"""
        if self.position:
            self.move(self.position)
        else:
            # Position near cursor
            cursor_pos = QCursor.pos()
            self.move(cursor_pos.x() + 20, cursor_pos.y() + 20)
        
        # Ensure window is visible on screen
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        
        # Adjust if off-screen
        if window_geometry.right() > screen_geometry.right():
            self.move(screen_geometry.right() - window_geometry.width(), self.y())
        if window_geometry.bottom() > screen_geometry.bottom():
            self.move(self.x(), screen_geometry.bottom() - window_geometry.height())
    
    def copy_to_clipboard(self):
        """Copy translated text to clipboard"""
        clipboard = QApplication.clipboard()
        translated_text = self.translation_result.get('translated_text', '')
        clipboard.setText(translated_text)
        
        # Visual feedback
        sender = self.sender()
        if sender:
            original_text = sender.text()
            sender.setText("Copied!")
            QTimer.singleShot(1000, lambda: sender.setText(original_text))
    
    def mousePressEvent(self, event):
        """Allow dragging the window"""
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
    
    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)
