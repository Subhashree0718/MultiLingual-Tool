# Tray Icon Not Showing? Here's How to Fix It

## Steps to Make Tray Icon Visible

### 1. Check if App is Running
The terminal should show:
```
✓ Screen Translator initialized
✓ System tray icon created and displayed
Hotkey registered: <ctrl>+<shift>+t
```

If you don't see these messages, restart the app.

### 2. Check Windows System Tray Overflow

Windows often hides tray icons in the **overflow area**:

1. Look for the **^** (up arrow) icon in your taskbar (bottom-right, near clock)
2. Click it to see hidden icons
3. You should see the **Screen Translator** icon there
4. To make it always visible:
   - Click the **^** arrow
   - Right-click on the Screen Translator icon
   - Or drag it to the main taskbar area

### 3. Windows 11: Show All Tray Icons

**For Windows 11:**
1. Right-click taskbar → **Taskbar settings**
2. Scroll to **Other system tray icons**
3. Find **Screen Translator** or **python** and toggle it **ON**

**For Windows 10:**
1. Right-click taskbar → **Taskbar settings**
2. Click **Select which icons appear on the taskbar**
3. Find **Screen Translator** or **python** and toggle it **ON**

### 4. Restart the Application

If still not showing:
1. In the terminal, press `Ctrl+C` to stop the app
2. Run again: `python main.py`
3. Look for the success messages

### 5. Verify Icon File Exists

Check if the icon file is present:
```bash
ls resources/icon.png
```

If it's missing, the app will use a default Windows icon instead.

## Quick Test

Once you see the tray icon:
1. **Right-click** the icon
2. You should see a menu with:
   - Translate Screen Text
   - Settings
   - Exit

If the menu appears, the tray icon is working! ✅
