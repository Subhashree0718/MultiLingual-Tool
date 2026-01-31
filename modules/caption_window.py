"""
Live Caption Window - Overlay for displaying translated captions
"""
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont


class LiveCaptionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.auto_hide_timer = QTimer()
        self.auto_hide_timer.timeout.connect(self.hide_caption)
        
    def setup_ui(self):
        """Setup the caption window UI"""
        # Window flags - always on top, frameless, transparent
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # Make background transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Caption label
        self.caption_label = QLabel()
        self.caption_label.setAlignment(Qt.AlignCenter)
        self.caption_label.setWordWrap(True)
        self.caption_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        # Styling - subtitle style
        self.caption_label.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                border: 2px solid rgba(255, 255, 255, 100);
            }
        """)
        
        layout.addWidget(self.caption_label)
        self.setLayout(layout)
        
        # Position at bottom center of screen
        self.position_window()
        
    def position_window(self):
        """Position the window at bottom center of screen"""
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        
        # Set size (80% of screen width, auto height)
        width = int(screen.width() * 0.8)
        self.setFixedWidth(width)
        
        # Position at bottom center
        x = (screen.width() - width) // 2
        y = int(screen.height() * 0.85)  # 85% down the screen
        
        self.move(x, y)
    
    def show_caption(self, text, duration=5000):
        """
        Show caption text
        
        Args:
            text: Caption text to display
            duration: How long to show caption in milliseconds (0 = indefinite)
        """
        self.caption_label.setText(text)
        self.caption_label.adjustSize()
        self.adjustSize()
        self.show()
        
        # Auto-hide after duration
        if duration > 0:
            self.auto_hide_timer.start(duration)
    
    def hide_caption(self):
        """Hide the caption"""
        self.auto_hide_timer.stop()
        self.hide()
    
    def update_caption(self, text):
        """
        Update caption text without hiding
        
        Args:
            text: New caption text
        """
        self.caption_label.setText(text)
        self.caption_label.adjustSize()
        self.adjustSize()
        
        # Reset auto-hide timer
        if self.auto_hide_timer.isActive():
            self.auto_hide_timer.stop()
            self.auto_hide_timer.start(5000)
