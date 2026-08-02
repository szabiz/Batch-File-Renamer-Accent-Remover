# Batch-Renamer
File & Folder Name Accent Remover / Batch Renamer

A lightweight and portable Windows application for batch renaming files and folders.

The program automatically removes accented characters from filenames, replaces spaces with underscores, supports custom character replacements, deletes characters by position, and provides a live preview before any changes are made.

The application is written in **Python** using the standard **Tkinter** GUI library and can be distributed as a single portable executable with no installation required.

---

# Features

* Batch rename files and folders.
* Remove accented characters (á, é, í, ó, ö, ő, ú, ü, ű → a, e, i, o, o, o, u, u, u).
* Replace spaces with underscores (`_`).
* Apply custom character and text replacements.
* Delete characters by position.
* Live preview before renaming.
* Rename confirmation dialog.
* Undo the last batch rename operation.
* Hungarian and English user interface.
* Supports both files and folders.
* No external dependencies.

---

# File Selection

The file list supports familiar Windows selection methods.

## Mouse

* Left Click – Select a single item.
* **Ctrl + Left Click** – Add or remove individual items from the selection.
* **Shift + Left Click** – Select a continuous range of items.
* Right Click – Preserves the current selection and can be used for context menu operations.

## Keyboard

* **Ctrl + A** – Select all items.
* **Esc** – Clear the current selection.

---

# System Requirements

## Operating System

* Windows 10 (64-bit)
* Windows 11 (64-bit)

## Hardware

Minimum:

* 1 GHz 64-bit processor
* 2 GB RAM
* 30 MB free disk space
* 1024 × 768 display

Recommended:

* Dual-core processor or faster
* 4 GB RAM or more
* Full HD (1920 × 1080) display

---

# Portable Executable

The released executable is a **64-bit portable application**.

* No installation required.
* No administrator privileges required.
* Python does not need to be installed.
* Simply download and run the executable.

---

# Running from Source

Requirements:

* Python 3.10 or newer

Run:

```bash
python atnevezo.py
```

---

# Building the Executable

Build a portable executable using PyInstaller:

```bash
python -m PyInstaller --onefile --windowed --clean --name Atnevezo atnevezo.py
```

The executable will be generated in the **dist** folder.

---

# License

This project is licensed under the **MIT License**.

See the **LICENSE** file for details.

---

# Author

Created and designed by **Szabiz**.

Developed with the assistance of **OpenAI ChatGPT**.


## Author

Created and designed by **Szabiz**.

Developed with the assistance of **OpenAI ChatGPT**.
