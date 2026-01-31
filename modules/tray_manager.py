"""
System Tray Manager - Handle system tray icon and menu
"""
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from PyQt5.QtCore import QObject, pyqtSignal
import os
from pathlib import Path


class TrayManager(QObject):
    # Signals
    translate_requested = pyqtSignal()
    settings_requested = pyqtSignal()
    live_captions_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.tray_icon = None
        self.setup_tray()
    
    def setup_tray(self):
        """Setup system tray icon and menu"""
        # Create tray icon
        self.tray_icon = QSystemTrayIcon(self.app)
        
        # Set icon
        icon_path = Path(__file__).parent.parent / "resources" / "icon.png"
        if icon_path.exists():
            self.tray_icon.setIcon(QIcon(str(icon_path)))
            print(f"[OK] Tray icon loaded from: {icon_path}")
        else:
            # Use a default icon if custom icon not found
            print(f"[WARN] Icon not found at {icon_path}, using default icon")
            self.tray_icon.setIcon(self.app.style().standardIcon(
                self.app.style().SP_ComputerIcon
            ))
        
        # Create menu
        menu = QMenu()
        
        # Translate action
        translate_action = QAction("Translate Screen Text", self.app)
        translate_action.triggered.connect(self.on_translate_clicked)
        menu.addAction(translate_action)
        
        # Live Captions action
        live_captions_action = QAction("Toggle Live Captions", self.app)
        live_captions_action.triggered.connect(self.on_live_captions_clicked)
        menu.addAction(live_captions_action)
        
        menu.addSeparator()
        
        # Settings action
        settings_action = QAction("Settings", self.app)
        settings_action.triggered.connect(self.on_settings_clicked)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self.app)
        exit_action.triggered.connect(self.on_exit_clicked)
        menu.addAction(exit_action)
        
        # Set menu to tray icon
        self.tray_icon.setContextMenu(menu)
        
        # Set tooltip
        self.tray_icon.setToolTip("Screen Translator")
        
        # Double-click to translate
        self.tray_icon.activated.connect(self.on_tray_activated)
        
        # Show tray icon
        self.tray_icon.show()
        self.tray_icon.setVisible(True)  # Explicitly set visible
        print("[OK] System tray icon created and displayed")
    
    def on_tray_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.translate_requested.emit()
    
    def on_translate_clicked(self):
        """Handle translate menu click"""
        self.translate_requested.emit()
    
    def on_settings_clicked(self):
        """Handle settings menu click"""
        self.settings_requested.emit()
    
    def on_live_captions_clicked(self):
        """Handle live captions menu click"""
        self.live_captions_requested.emit()
    
    def on_exit_clicked(self):
        """Handle exit menu click"""
        self.exit_requested.emit()
    
    def show_message(self, title, message, icon=QSystemTrayIcon.Information):
        """Show a tray notification"""
        self.tray_icon.showMessage(title, message, icon, 3000)
    
    def hide(self):
        """Hide the tray icon"""
        if self.tray_icon:
            self.tray_icon.hide()
