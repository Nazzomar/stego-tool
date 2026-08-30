# Steg Tool

IKB21303 (Data Hiding & Encryption) Assignment 2 - build an image steganography tool that hides
secret files inside a cover image and analyzes the result. Group project, 50 marks / 15%.

## What it does

- **Embed:** hide a secret file (`.txt`, `.pdf`, `.doc`, `.png`, `.jpg`) inside a cover image using
  LSB (least significant bit) substitution, save the result as a stego image.
- **Extract:** recover the hidden file back out of a stego image.
- **Analyze:** compare a cover/stego image pair - RGB channel histograms and file size, with an
  explanation of why the size stayed the same or changed.

## Tech stack

- **Language:** Python 3
- **GUI:** `tkinter` / `ttk` (stdlib - no separate frontend, no web server, no deployment needed)
- **Image I/O + pixel access:** [Pillow](https://python-pillow.org/) (PIL)
- **Histogram plotting:** [matplotlib](https://matplotlib.org/), embedded in the Tk window via
  `FigureCanvasTkAgg`
- **Array/bit manipulation:** [numpy](https://numpy.org/)
- **Packaging (optional, for the demo):** [PyInstaller](https://pyinstaller.org/) to build a
  standalone `.exe`

It's a local desktop app, not a website - no backend, database, or hosting involved. Built and
tested on Windows; runs unmodified on Linux/macOS as long as Tk is available (see Setup).

## Setup

### Windows

Tk is bundled with the standard Python installer, so no extra steps.

```
pip install -r requirements.txt
python main.py
```

### Linux

Tk is usually not bundled - install it via your distro's package manager first.

```
# Arch
sudo pacman -S tk

# Debian / Ubuntu
sudo apt install python3-tk
```

Then the same as Windows:

```
pip install -r requirements.txt
python main.py
```

## Project layout

- `main.py` - window setup, splits the app into the two panels below.
- `stego_panel.py` - **left panel** UI: pick a cover image (PNG only - JPG's lossy compression
  would corrupt LSB data) and a secret file, Embed/Extract buttons. Calls into `stego.py`.
- `stego.py` - the actual LSB embed/extract logic. **Not implemented yet** - `embed_secret()` and
  `extract_secret()` are stubs (`raise NotImplementedError`) ready to be filled in.
- `analyzer_panel.py` - **right panel** UI: manually load a cover and a stego image (independent of
  the left panel, so any past pair can be re-analyzed), compare file size, plot histograms. Fully
  working already.
- `requirements.txt` - pinned dependencies.

## Design notes

- **Project scope is PNG only.** LSB embedding depends on exact pixel byte values; JPEG's lossy
  compression rewrites those bytes on save and would destroy the hidden data. BMP would also work
  losslessly, but PNG alone keeps the tool and the report's format-specific explanations simpler.
- **Capacity is checked before embedding**, not discovered mid-write: the tool compares the secret
  file's size against the cover image's max capacity (width x height x channels, 1 bit each) and
  refuses with a clear error if it won't fit.
- **Analyzer is decoupled from the Steg Tool panel** - it doesn't auto-load whatever the left panel
  just produced. You load cover/stego images into it manually, which also makes it useful for
  re-checking older results.

## Status

- Analyzer: done.
- Steg tool UI: done, wired to `stego.py`'s stubs.
- Steg tool logic (`stego.py`): TODO.

## Team

Najmi, Qayyum, Khalif, Nazir
