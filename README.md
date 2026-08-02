# Batch-Renamer
File &amp; Folder Name Accent Remover / Batch Renamer
# File & Folder Name Accent Remover / Batch Renamer

A lightweight, portable Python application for batch renaming files and folders.

The program automatically removes accented characters from file and folder names, replaces spaces with underscores, applies custom character replacements, and provides a live preview before any changes are made.

The graphical user interface is built with **Python** and **Tkinter**, and the application has **no external dependencies**.

---

## Features

* Batch rename files and folders.
* Remove accented characters (á, é, í, ó, ö, ő, ú, ü, ű → a, e, i, o, o, o, u, u, u).
* Replace spaces with underscores (`_`).
* Custom character and text replacements (for example `&` → `es`).
* Delete characters by position.
* Preview every new filename before renaming.
* Rename confirmation dialog.
* Undo the last batch rename operation.
* Hungarian and English user interface.
* Supports both files and folders.
* No external libraries required.

---

## Selection

The file list supports standard Windows multi-selection.

### Mouse

* Left Click – Select a single item.
* **Ctrl + Left Click** – Add or remove individual items from the selection.
* **Shift + Left Click** – Select a continuous range of items.
* Right Click – Keeps the current selection and can be used for context menu operations.

### Keyboard

* **Ctrl + A** – Select all items.
* **Esc** – Clear the current selection.

---

## Requirements

* Windows
* Python 3.10 or newer

No additional Python packages are required to run the source code.

---

## Running from Source

```bash
python atnevezo.py
```

---

## Building a Portable EXE

The application can be compiled into a single portable executable using PyInstaller.

```bash
python -m PyInstaller --onefile --windowed --name Atnevezo atnevezo.py
```

The generated executable will be located in the `dist` folder.

---

## License

This project is licensed under the MIT License.

See the **LICENSE** file for details.

---

## Author

Created and designed by **Szabiz**.

Developed with the assistance of **OpenAI ChatGPT**.
