# PrivaForm

A simple, free, and fully offline desktop tool to convert TIFF files (including multi-page TIFFs) into a single PDF — with a clean GUI, no subscriptions, and no data leaving your machine.

---

## Why choose this over online tools?

Online converters like Smallpdf, ILovePDF, and similar tools work by **uploading your file to their servers**. For most casual use that's fine — but if your document is:

- A legal or court document
- A property or land record
- A medical or financial file
- Any personally identifiable or sensitive document

...then uploading it to a random third-party server is a real risk. You have no way of knowing how long they store it, who has access to it, or whether it is truly deleted after conversion.

**This tool runs 100% on your own machine.** Your file never leaves your PC. No internet connection is used during conversion. No accounts, no uploads, no servers — just a simple local tool that does one job cleanly and privately.
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

1. Download `PrivaForm.exe` from the `dist` folder
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
python convert.py
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

Custom MIT + Commons Clause — free for personal, academic, and non-commercial use.
Commercial use by companies requires written permission from the author.
See [LICENSE](LICENSE) for full details.
