# Screen Translator

A Windows desktop tool for translating on-screen text in real-time. Similar to Grammarly in behavior, but focused on multilingual translation across all Windows applications.

![Screen Translator Icon](resources/icon.png)

## Features

- 🌍 **Universal Translation**: Works across all Windows applications (WhatsApp, Chrome, PDFs, Notepad, etc.)
- 🔍 **Screen Region Selection**: Select any visible text on your screen
- 🤖 **Automatic Language Detection**: No need to specify source language
- 🚀 **Instant Translation**: Fast OCR and translation in 2-5 seconds
- ⌨️ **Global Hotkey**: Quick access via keyboard shortcut (default: Ctrl+Shift+T)
- 🎨 **Modern Dark UI**: Beautiful, non-intrusive popup interface
- 🔒 **Privacy-First**: No data storage, only processes visible screen content
- 🌐 **Multi-Language Support**: English, Tamil, Hindi, Telugu, Malayalam, Kannada, Marathi, Bengali, Gujarati, Punjabi

## Prerequisites

### 1. Tesseract OCR (Required)

Download and install Tesseract OCR from:
**https://github.com/UB-Mannheim/tesseract/wiki**

During installation:
- Install to default location: `C:\Program Files\Tesseract-OCR\`
- Select **Additional language data** and install:
  - English (eng)
  - Hindi (hin)
  - Tamil (tam)
  - Telugu (tel)
  - Malayalam (mal)
  - Any other Indian languages you need

### 2. Python 3.9+ (For development)

If running from source, install Python 3.9 or later from python.org

## Installation

### Option 1: Run from Source

1. Clone or download this repository

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

### Option 2: Build Executable

1. Install PyInstaller:
```bash
pip install pyinstaller
```

2. Build the executable:
```bash
pyinstaller build/build_exe.spec
```

3. The executable will be in the `dist/` folder

## Configuration

On first run or from the system tray:

1. **Right-click** the tray icon (near the clock)
2. Select **Settings**
3. Configure:
   - **Target Language**: Choose your preferred translation language
   - **Keyboard Shortcut**: Customize the hotkey (default: ctrl+shift+t)
   - **Tesseract Path**: Set the path to tesseract.exe

## Usage

### Method 1: Keyboard Shortcut (Recommended)

1. Press `Ctrl+Shift+T` (or your configured hotkey)
2. Screen overlay appears
3. Draw a rectangle around the text you want to translate
4. Translation popup appears instantly

### Method 2: System Tray

1. Right-click the tray icon
2. Click "Translate Screen Text"
3. Draw a rectangle around the text
4. View translation

### Method 3: Double-Click Tray Icon

1. Double-click the tray icon (near clock)
2. Draw a rectangle around the text
3. View translation

## How It Works

```
User triggers tool (hotkey/menu)
        ↓
Screen overlay appears
        ↓
User selects text region
        ↓
Screenshot captured
        ↓
OCR extracts text (Tesseract)
        ↓
Language auto-detected
        ↓
Text translated (Google Translate)
        ↓
Popup displays result
```

## Supported Languages

- 🇬🇧 English (en)
- 🇮🇳 Tamil (ta)
- 🇮🇳 Hindi (hi)
- 🇮🇳 Telugu (te)
- 🇮🇳 Malayalam (ml)
- 🇮🇳 Kannada (kn)
- 🇮🇳 Marathi (mr)
- 🇮🇳 Bengali (bn)
- 🇮🇳 Gujarati (gu)
- 🇮🇳 Punjabi (pa)

## Privacy & Security

✅ **No data is stored** - Text is processed in memory only
✅ **No keylogging** - Only captures visible screen content when you trigger it
✅ **No automatic scanning** - Translation is user-triggered only
✅ **No application hooks** - Doesn't modify or access application memory

## Troubleshooting

### "Tesseract Not Found" Error

1. Verify Tesseract is installed
2. Check the installation path in Settings
3. Common paths:
   - `C:\Program Files\Tesseract-OCR\tesseract.exe`
   - `C:\Program Files (x86)\Tesseract-OCR\tesseract.exe`

### "No Text Detected" Error

1. Ensure the selected region contains readable text
2. Try selecting a larger area
3. Ensure text is not too small or blurry
4. Check that appropriate language packs are installed in Tesseract

### Translation Fails

1. Check internet connection (required for Google Translate)
2. Try again - may be temporary network issue
3. Check if source text is in a supported language

### Hotkey Not Working

1. Check if another application is using the same shortcut
2. Change the hotkey in Settings
3. Restart the application after changing hotkey

## Technical Details

- **Language**: Python 3.9+
- **UI Framework**: PyQt6
- **OCR Engine**: Tesseract OCR
- **Translation**: Google Translate API (via googletrans)
- **Language Detection**: langdetect
- **Hotkey**: pynput
- **Platform**: Windows 10/11

## Project Structure

```
screen-translator/
├── main.py                 # Application entry point
├── config.py               # Configuration constants
├── requirements.txt        # Python dependencies
├── modules/
│   ├── tray_manager.py    # System tray integration
│   ├── screen_capture.py  # Screen region capture
│   ├── ocr_engine.py      # OCR processing
│   ├── translator.py      # Translation service
│   ├── popup_window.py    # Result display
│   ├── settings_window.py # Settings UI
│   ├── settings_manager.py # Settings persistence
│   └── hotkey_handler.py  # Global shortcuts
├── resources/
│   ├── icon.png           # Application icon
│   └── settings.json      # User settings
└── build/
    └── build_exe.spec     # PyInstaller config
```

## Known Limitations

- Requires internet connection for translation
- OCR accuracy depends on text clarity and size
- Tesseract must be installed separately
- Does not work with DRM-protected content
- Cannot translate text in video games (protected by anti-cheat)

## Future Enhancements

- [ ] Offline translation option
- [ ] History of translations
- [ ] Custom translation APIs
- [ ] OCR accuracy improvements
- [ ] Multi-monitor support optimization

## License

This project is for educational and personal use.

## Credits

- **Tesseract OCR**: Google's open-source OCR engine
- **Google Translate**: Translation service
- **PyQt6**: Cross-platform UI framework

## Version

**v1.0.0** - Initial Release

---

Made with ❤️ for multilingual Windows users
