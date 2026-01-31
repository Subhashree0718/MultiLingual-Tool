# Quick Language Change Guide

## Current Issue
The app is translating "English → English" because the default target language is set to English.

## Solution: Change Target Language

### Method 1: Via Settings Window (Easiest)
1. **Find the tray icon** (near the clock in taskbar)
2. **Right-click** the tray icon
3. Click **"Settings"**
4. In the **"Target Language"** dropdown, select your preferred language:
   - Tamil (தமிழ்)
   - Hindi (हिंदी)
   - Telugu (తెలుగు)
   - Malayalam (മലയാളം)
   - Or any other supported language
5. Click **"Save"**

### Method 2: Restart the Application
After changing settings.json, restart the app:
1. Right-click tray icon → Exit
2. Run: `python main.py`

## Default Language Changed
I've temporarily set the default to **Tamil** in `settings.json`. 

You can change it to any language you prefer using the Settings window!

## Available Languages
- English (en)
- Tamil (ta) ← Currently set as default
- Hindi (hi)
- Telugu (te)
- Malayalam (ml)
- Kannada (kn)
- Marathi (mr)
- Bengali (bn)
- Gujarati (gu)
- Punjabi (pa)

## Test It
1. Open Notepad
2. Type: "Hello, how are you?"
3. Press `Ctrl+Shift+T`
4. Select the text
5. You should see translation to Tamil (or your selected language)!
