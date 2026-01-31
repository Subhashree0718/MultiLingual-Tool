"""
Hotkey Handler - Global keyboard shortcut registration
"""
from pynput import keyboard
from PyQt5.QtCore import QObject, pyqtSignal


class HotkeyHandler(QObject):
    # Signal emitted when hotkey is pressed
    hotkey_pressed = pyqtSignal()
    
    def __init__(self, hotkey_combo="<ctrl>+<shift>+t"):
        super().__init__()
        self.hotkey_combo = hotkey_combo
        self.listener = None
        self.is_active = False
    
    def start(self):
        """Start listening for hotkey"""
        if self.is_active:
            return
        
        try:
            # Parse the hotkey combination
            self.hotkey = keyboard.HotKey(
                keyboard.HotKey.parse(self.hotkey_combo),
                self.on_activate
            )
            
            # Start the listener
            self.listener = keyboard.Listener(
                on_press=self.for_canonical(self.hotkey.press),
                on_release=self.for_canonical(self.hotkey.release)
            )
            self.listener.start()
            self.is_active = True
            print(f"Hotkey registered: {self.hotkey_combo}")
            
        except Exception as e:
            print(f"Error starting hotkey listener: {e}")
    
    def stop(self):
        """Stop listening for hotkey"""
        if self.listener:
            self.listener.stop()
            self.is_active = False
            print("Hotkey listener stopped")
    
    def for_canonical(self, f):
        """Helper to convert keys to canonical form"""
        return lambda k: f(self.listener.canonical(k))
    
    def on_activate(self):
        """Called when hotkey is pressed"""
        print("Hotkey activated!")
        self.hotkey_pressed.emit()
    
    def update_hotkey(self, new_hotkey):
        """Update the hotkey combination"""
        self.stop()
        self.hotkey_combo = new_hotkey
        self.start()
