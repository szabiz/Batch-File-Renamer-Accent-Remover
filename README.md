# Batch File Renamer & Accent Remover

### Fájlok Csoportos átnevezése és ékezettelenítése

<p align="center">

![Platform](https://img.shields.io/badge/Platform-Windows%2010%20%7C%2011-blue)
![Architecture](https://img.shields.io/badge/Architecture-64--bit-blue)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

</p>

A lightweight and portable Windows application for batch renaming files and folders.

The program removes accented characters, replaces spaces, performs custom text replacements, previews every change before execution, and safely renames multiple files or folders in a single operation.

No installation is required when using the released executable.

---

The main interface provides all renaming options in one place. You can load files or folders, configure rename rules, preview the results, and execute batch operations safely.

---

# Features

- Batch rename files and folders
- Remove accented characters
- Replace spaces with underscores (`_`)
- Custom character and text replacements
- Delete characters by position
- Live preview before renaming
- Undo the last batch rename operation
- Hungarian and English user interface
- Supports both files and folders
- No external dependencies
- Portable executable

### New in v1.5
- Added support for prefix/suffix text insertion when position field is empty.
- UI adjustments for easier file handling.
### New in v1.6
### Dedicated Accent Removal & Exception Handling
Accent removal is no longer executed automatically; it is now managed via its own dedicated menu and dialog window[cite: 4]:
* **Dedicated Menu Option:** Accessible under **Settings > Accent removal...** (`Beállítások > Ékezetmentesítés...`)[cite: 4].
* **Custom Character Exceptions:** Define specific characters (or spaces) that must be preserved without modification[cite: 4].
* **Accent & Space Processing:** Strips diacritics and replaces standard spaces with underscores (`_`)[cite: 4].
* **Flexible Toggle Controls:** Click **Apply** to save settings and enable accent removal (`"aktiv": True`), or **Clear / Disable** to turn it off (`"aktiv": False`)[cite: 4].

### Auto-Numbering Window
A dedicated dialog for configuring automatic sequential file numbering[cite: 4]:
* **Customization Options:** Set custom prefix, suffix, start index, and digit padding[cite: 4].
* **Smart Action Buttons:**
  * **Apply:** Saves configuration and activates auto-numbering (`"aktiv": True`)[cite: 4].
  * **Clear / Disable:** Deactivates auto-numbering (`"aktiv": False`)[cite: 4].
* **Optimized UI:** Compact and clean layout (`450x280`) designed for an efficient user experience[cite: 4].

---

# Selection

The file list supports familiar Windows selection methods.

### Mouse

- Left Click – Select a single item
- **Ctrl + Left Click** – Add or remove individual items from the selection
- **Shift + Left Click** – Select a continuous range of items
- Right Click – Preserves the current selection and opens the context menu

### Keyboard

- **Ctrl + A** – Select all items
- **Esc** – Clear the current selection

---

# Main Window

<p align="center">
    <img src="Atnevezo1.jpg" width="950">
</p>

# Preview

<p align="center">
    <img src="Atnevezo2.jpg" width="900">
</p>

Preview all filename changes before renaming. This helps prevent mistakes and gives full control over the final result.

---

# Batch Rename

<p align="center">
    <img src="Atnevezo3.jpg" width="900">
</p>

Rename multiple files and folders quickly and safely with a single click.

---

# System Requirements

## Operating System

- Windows 10 (64-bit)
- Windows 11 (64-bit)

## Minimum Hardware

- 1 GHz 64-bit processor
- 2 GB RAM
- 30 MB free disk space

## Recommended

- Dual-core processor
- 4 GB RAM or more
- Full HD (1920×1080) display

---

# Portable Executable

The released executable is completely portable.

- No installation required
- No administrator privileges required
- Python is not required
- Single executable file

---

# Running from Source

```bash
python atnevezo.py
```

---

# Building the Executable

```bash
python -m PyInstaller --onefile --windowed --clean --name Atnevezo atnevezo.py
```

The executable will be created inside the `dist` folder.

---

# License

This project is licensed under the **MIT License**.

See the **LICENSE** file for details.

---

# Author

Created and designed by **szabiz**.

## Credits & Dependencies

- Python / Tkinter**: [PSF License](https://docs.python.org/3/license.html)

- This project was developed with the assistance of AI tools, including **Claude** and **OpenAI ChatGPT**.
