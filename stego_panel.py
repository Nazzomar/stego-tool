"""Left panel: the steganography tool UI. Embed/extract logic lives in stego.py (teammate's module)."""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageTk

import stego

COVER_FILETYPES = [("PNG/BMP images", "*.png *.bmp")]
SECRET_FILETYPES = [("Supported files", "*.txt *.pdf *.doc *.docx *.png *.jpg *.jpeg")]
THUMB_SIZE = (200, 200)


class StegPanel(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Steganography Tool")

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
        ttk.Button(button_row, text="Extract", command=self._extract).pack(side="left", padx=4)

        self.status_label = ttk.Label(self, text="", foreground="blue", wraplength=320)
        self.status_label.grid(row=6, column=0, sticky="w", padx=8, pady=(4, 8))

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
            self.status_label.config(text="Embed not implemented yet.")

    def _extract(self):
        stego_path = filedialog.askopenfilename(title="Select stego image", filetypes=COVER_FILETYPES)
        if not stego_path:
            return
        output_path = filedialog.asksaveasfilename(title="Save extracted file as")
        if not output_path:
            return
        try:
            stego.extract_secret(stego_path, output_path)
            self.status_label.config(text=f"Extracted. Saved to {output_path}")
        except NotImplementedError:
            self.status_label.config(text="Extract not implemented yet.")
