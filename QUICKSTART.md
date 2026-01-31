# Quick Start Guide - Screen Translator

## ⚡ Fast Installation

### Step 1: Install Tesseract OCR (Required!)

1. Download installer: https://github.com/UB-Mannheim/tesseract/wiki
2. Run installer
3. **Important**: During installation, select "Additional language data":
   - ✅ English (eng)
   - ✅ Hindi (hin)
   - ✅ Tamil (tam)
   - ✅ Telugu (tel)
   - ✅ Malayalam (mal)
   - ✅ Any other languages you need

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python main.py
```

## 🎯 Quick Usage

1. **Look for the tray icon** (bottom-right corner, near clock)
2. **Press `Ctrl+Shift+T`** anywhere in Windows
3. **Draw a rectangle** around text you want to translate
4. **View translation** in the popup window!

## ⚙️ First-Time Setup

1. Right-click tray icon → **Settings**
2. Select your **target language** (e.g., Tamil, Hindi, English)
3. Verify **Tesseract path** is correct
4. Click **Save**

## 🧪 Quick Test

1. Open Notepad
2. Type: "Hello, how are you?"
3. Press `Ctrl+Shift+T`
4. Select the text
5. See the translation!

## 🔧 Troubleshooting

**"Tesseract Not Found"**
→ Make sure Tesseract is installed to `C:\Program Files\Tesseract-OCR\`

**"No Text Detected"**
→ Select a larger area or ensure text is clear and readable

**"Translation Failed"**
→ Check your internet connection

## 📦 Build Executable (Optional)

```bash
pip install pyinstaller
pyinstaller build/build_exe.spec
```

Executable will be in: `dist/ScreenTranslator.exe`

---

**Need help?** Check README.md for detailed documentation!
