# TIFF to PDF Converter

A simple, free, and fully offline desktop tool to convert TIFF files (including multi-page TIFFs) into a single PDF — with a clean GUI, no subscriptions, and no data leaving your machine.

---

## Why this exists

Most online TIFF to PDF converters upload your file to a server. For confidential or sensitive documents, that's a risk. This tool runs **100% locally** on your PC — nothing is sent anywhere.

---

## Features

- ✅ Supports single and multi-page TIFF files
- ✅ Clean GUI — no command line needed
- ✅ Custom output file name
- ✅ Page-by-page progress log
- ✅ Completely offline
- ✅ No installation required (just run the `.exe`)

---

## How to use

### Option A — Just use the exe (recommended)

1. Download `TIFF to PDF Converter.exe` from the `dist` folder
2. Double click it
3. Browse and select your TIFF file
4. Enter your desired output PDF name
5. Click **Convert to PDF**
6. The PDF will be saved in the same folder as your TIFF

### Option B — Run from source

**Requirements:**
```bash
pip install Pillow img2pdf
```

**Run:**
```bash
python newconvert.py
```

---

## Built with

- [Python 3.13](https://www.python.org/)
- [Pillow](https://python-pillow.org/)
- [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (built into Python)

---

## Platform

> **Windows only** for the `.exe`. Mac/Linux users can run directly from source.

---

## License

MIT License — free to use, modify, and distribute.
