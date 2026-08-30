"""Left panel: the steganography tool UI. Embed/extract logic lives in stego.py (teammate's module)."""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageTk

import stego

# Cover images are restricted to PNG/BMP (lossless) - JPEG's lossy compression rewrites
# pixel bytes on save and would destroy LSB-hidden data.
COVER_FILETYPES = [("PNG/BMP images", "*.png *.bmp")]
SECRET_FILETYPES = [("Supported files", "*.txt *.pdf *.doc *.docx *.png *.jpg *.jpeg")]
THUMB_SIZE = (160, 160)


class StegPanel(ttk.LabelFrame):
    """Container for the two independent sub-workflows: embedding a new stego image, and
    extracting a payload back out of an existing one. Kept as separate sections (not shared
    cover/secret fields + two buttons) since they don't operate on the same inputs."""

    def __init__(self, parent):
        super().__init__(parent, text="Steganography Tool")

        self.columnconfigure(0, weight=1)

        EmbedSection(self).grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        ExtractSection(self).grid(row=1, column=0, sticky="ew", padx=4, pady=4)


class EmbedSection(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Embed")

        self.cover_path = None
        self.secret_path = None
        self.cover_thumb = None  # keep a reference so Tk doesn't garbage-collect it

        self.columnconfigure(0, weight=1)

        ttk.Button(self, text="Browse Cover Image...", command=self._browse_cover).grid(
            row=0, column=0, sticky="ew", padx=8, pady=(8, 2)
        )
        self.cover_label = ttk.Label(self, text="No cover image selected")
        self.cover_label.grid(row=1, column=0, sticky="w", padx=8)

        self.cover_preview = ttk.Label(self)
        self.cover_preview.grid(row=2, column=0, pady=4)

        ttk.Button(self, text="Browse Secret File...", command=self._browse_secret).grid(
            row=3, column=0, sticky="ew", padx=8, pady=(12, 2)
        )
        self.secret_label = ttk.Label(self, text="No secret file selected")
        self.secret_label.grid(row=4, column=0, sticky="w", padx=8)

        button_row = ttk.Frame(self)
        button_row.grid(row=5, column=0, pady=12)
        ttk.Button(button_row, text="Embed", command=self._embed).pack(side="left", padx=4)
        ttk.Button(button_row, text="Clear", command=self._clear).pack(side="left", padx=4)

        self.status_label = ttk.Label(self, text="", foreground="blue", wraplength=320)
        self.status_label.grid(row=6, column=0, sticky="w", padx=8, pady=(0, 8))

    def _browse_cover(self):
        path = filedialog.askopenfilename(title="Select cover image", filetypes=COVER_FILETYPES)
        if not path:
            return
        self.cover_path = path
        self.cover_label.config(text=os.path.basename(path))
        image = Image.open(path)
        image.thumbnail(THUMB_SIZE)
        self.cover_thumb = ImageTk.PhotoImage(image)
        self.cover_preview.config(image=self.cover_thumb)

    def _browse_secret(self):
        path = filedialog.askopenfilename(title="Select secret file", filetypes=SECRET_FILETYPES)
        if not path:
            return
        self.secret_path = path
        self.secret_label.config(text=os.path.basename(path))

    def _embed(self):
        if not self.cover_path or not self.secret_path:
            messagebox.showwarning("Missing input", "Select a cover image and a secret file first.")
            return
        output_path = filedialog.asksaveasfilename(
            title="Save stego image as", defaultextension=".png", initialfile="stego.png",
            filetypes=COVER_FILETYPES,
        )
        if not output_path:
            return
        try:
            stego.embed_secret(self.cover_path, self.secret_path, output_path)
            self.status_label.config(text=f"Embedded. Saved to {output_path}")
        except NotImplementedError:
            # stego.py's embed_secret() is a stub until the teammate implements it -
            # UI stays usable in the meantime instead of crashing.
            self.status_label.config(text="Embed not implemented yet.")

    def _clear(self):
        self.cover_path = None
        self.secret_path = None
        self.cover_thumb = None
        self.cover_label.config(text="No cover image selected")
        self.secret_label.config(text="No secret file selected")
        self.cover_preview.config(image="")
        self.status_label.config(text="")


class ExtractSection(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Extract")

        self.stego_path = None
        self.stego_thumb = None

        self.columnconfigure(0, weight=1)

        ttk.Button(self, text="Browse Stego Image...", command=self._browse_stego).grid(
            row=0, column=0, sticky="ew", padx=8, pady=(8, 2)
        )
        self.stego_label = ttk.Label(self, text="No stego image selected")
        self.stego_label.grid(row=1, column=0, sticky="w", padx=8)

        self.stego_preview = ttk.Label(self)
        self.stego_preview.grid(row=2, column=0, pady=4)

        button_row = ttk.Frame(self)
        button_row.grid(row=3, column=0, pady=12)
        ttk.Button(button_row, text="Extract", command=self._extract).pack(side="left", padx=4)
        ttk.Button(button_row, text="Clear", command=self._clear).pack(side="left", padx=4)

        self.status_label = ttk.Label(self, text="", foreground="blue", wraplength=320)
        self.status_label.grid(row=4, column=0, sticky="w", padx=8, pady=(0, 8))

    def _browse_stego(self):
        path = filedialog.askopenfilename(title="Select stego image", filetypes=COVER_FILETYPES)
        if not path:
            return
        self.stego_path = path
        self.stego_label.config(text=os.path.basename(path))
        image = Image.open(path)
        image.thumbnail(THUMB_SIZE)
        self.stego_thumb = ImageTk.PhotoImage(image)
        self.stego_preview.config(image=self.stego_thumb)

    def _extract(self):
        if not self.stego_path:
            messagebox.showwarning("Missing input", "Select a stego image first.")
            return
        output_path = filedialog.asksaveasfilename(title="Save extracted file as")
        if not output_path:
            return
        try:
            stego.extract_secret(self.stego_path, output_path)
            self.status_label.config(text=f"Extracted. Saved to {output_path}")
        except NotImplementedError:
            self.status_label.config(text="Extract not implemented yet.")
            # See NOTES.md for the header-format decisions extract_secret() needs to
            # agree with embed_secret() on (payload length, filename, etc).

    def _clear(self):
        self.stego_path = None
        self.stego_thumb = None
        self.stego_label.config(text="No stego image selected")
        self.stego_preview.config(image="")
        self.status_label.config(text="")
