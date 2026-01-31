"""
Screen Capture - Region selection and screenshot capture
"""
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QCursor
from PIL import Image
import io


class ScreenCaptureOverlay(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.start_pos = None
        self.end_pos = None
        self.is_selecting = False
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the overlay window"""
        # Make it fullscreen and frameless
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        
        # Set semi-transparent background
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.3)
        
        # Make it cover all screens
        screen_geometry = QApplication.primaryScreen().virtualGeometry()
        self.setGeometry(screen_geometry)
        
        # Set crosshair cursor
        self.setCursor(QCursor(Qt.CrossCursor))
        
        # Show fullscreen
        self.showFullScreen()
    
    def paintEvent(self, event):
        """Draw the overlay and selection rectangle"""
        painter = QPainter(self)
        
        # Draw semi-transparent background
        painter.fillRect(self.rect(), QColor(0, 0, 0, 100))
        
        # Draw selection rectangle if selecting
        if self.start_pos and self.end_pos:
            selection_rect = self.get_selection_rect()
            
            # Clear the selected area (make it transparent)
            painter.setCompositionMode(QPainter.CompositionMode_Clear)
            painter.fillRect(selection_rect, Qt.transparent)
            
            # Draw border around selection
            painter.setCompositionMode(QPainter.CompositionMode_SourceOver)
            pen = QPen(QColor(0, 255, 0), 2, Qt.SolidLine)
            painter.setPen(pen)
            painter.drawRect(selection_rect)
    
    def get_selection_rect(self):
        """Get the normalized selection rectangle"""
        if not self.start_pos or not self.end_pos:
            return QRect()
        
        x1, y1 = self.start_pos.x(), self.start_pos.y()
        x2, y2 = self.end_pos.x(), self.end_pos.y()
        
        # Normalize coordinates
        x = min(x1, x2)
        y = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        
        return QRect(x, y, w, h)
    
    def mousePressEvent(self, event):
        """Handle mouse press - start selection"""
        if event.button() == Qt.LeftButton:
            self.start_pos = event.pos()
            self.end_pos = event.pos()
            self.is_selecting = True
            self.update()
    
    def mouseMoveEvent(self, event):
        """Handle mouse move - update selection"""
        if self.is_selecting:
            self.end_pos = event.pos()
            self.update()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release - capture the selected region"""
        if event.button() == Qt.MouseButton.LeftButton and self.is_selecting:
            self.end_pos = event.pos()
            self.is_selecting = False
            
            # Get selection rectangle
            selection_rect = self.get_selection_rect()
            
            # Only capture if selection is meaningful (at least 10x10 pixels)
            if selection_rect.width() > 10 and selection_rect.height() > 10:
                self.capture_region(selection_rect)
            
            # Close the overlay
            self.close()
    
    def keyPressEvent(self, event):
        """Handle key press - ESC to cancel"""
        if event.key() == Qt.Key_Escape:
            self.close()
    
    def capture_region(self, rect):
        """Capture the selected screen region"""
        try:
            # Get the screen
            screen = QApplication.primaryScreen()
            
            # Capture the region
            pixmap = screen.grabWindow(
                0,
                rect.x(),
                rect.y(),
                rect.width(),
                rect.height()
            )
            
            # Convert QPixmap to PIL Image
            image = self.qpixmap_to_pil(pixmap)
            
            # Call the callback with the captured image
            if self.callback:
                self.callback(image)
                
        except Exception as e:
            print(f"Error capturing region: {e}")
    
    def qpixmap_to_pil(self, pixmap):
        """Convert QPixmap to PIL Image"""
        # Convert to QImage
        qimage = pixmap.toImage()
        
        # Convert to bytes
        buffer = qimage.bits().asstring(qimage.sizeInBytes())
        
        # Create PIL Image
        image = Image.frombytes(
            "RGBA",
            (qimage.width(), qimage.height()),
            buffer,
            "raw",
            "BGRA"
        )
        
        # Convert to RGB
        return image.convert("RGB")


class ScreenCapture:
    """Simple interface for screen capture"""
    
    @staticmethod
    def capture_region(callback):
        """Show overlay and capture region"""
        overlay = ScreenCaptureOverlay(callback)
        return overlay
