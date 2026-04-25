# PrivaForm

A simple, free, and fully offline desktop tool to convert **TIFF, PNG, and JPG files** into a single PDF — with a clean GUI, no subscriptions, and no data leaving your machine.

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

- ✅ Multi-format support: TIFF, PNG, JPG, WEBP, BMP, GIF → PDF
- ✅ PDF Merger: Combine multiple PDFs into one
- ✅ Single and multi-page conversions
- ✅ Auto-detect input format or manual selection
- ✅ Clean GUI — no command line needed
- ✅ Custom output file name and save location
- ✅ Page-by-page progress log
- ✅ Completely offline
- ✅ No installation required (just run the `.exe`)

---

## How to use

### Option A — Just use the exe (recommended)

1. Download `PrivaForm.exe` from the latest [Release](https://github.com/Mohammad-Omar-Siddiq/PrivaForm/releases)
2. Double-click to launch
3. **Select input file** — Browse and choose your TIFF, PNG, or JPG file
4. **Choose format** — Auto-detect (recommended) or manually select
5. **Enter output name** — Name for your PDF (extension added automatically)
6. **Set save location** — Defaults to Downloads folder; change if needed
7. Click **Convert to PDF**
8. Done! Your PDF is ready

### Option B — Run from source

**Requirements:**
```bash
pip install Pillow img2pdf pypdf
```

**Run:**
```bash
python convert.py
```

---

## Security & Privacy

- ✅ **Zero-knowledge:** No data collection, no telemetry, no tracking
- ✅ **Offline-first:** Works without internet
- ✅ **Open-source:** Code auditable on GitHub
- ✅ **VirusTotal scanned:** Every release is scanned and verified

See [SECURITY.md](SECURITY.md) for full details.

---

## Built with

- [Python 3.13](https://www.python.org/)
- [Pillow](https://python-pillow.org/)
- [img2pdf](https://gitlab.mister-muffin.de/josch/img2pdf)
- [pypdf](https://pypdf.readthedocs.io/en/stable/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html) (built into Python)

---

## Platform

> **Windows only** for the `.exe` (via GitHub Releases). Mac/Linux users can run directly from source.

---

## License

Custom MIT + Commons Clause — free for personal, academic, and non-commercial use.
Commercial use by companies requires written permission from the author.
See [LICENSE](LICENSE) for full details.

---

## Roadmap

- [ ] Code signing via SignPath Foundation (in progress)
- [ ] PNG/JPG multi-page batch conversion
- [ ] OCR support
- [ ] macOS/Linux executables

---

## Support

Found an issue? Have a suggestion? Open an [Issue](https://github.com/Mohammad-Omar-Siddiq/PrivaForm/issues) on GitHub.