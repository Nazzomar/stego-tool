"""Left panel: the steganography tool UI. Embed/extract logic lives in stego.py."""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from PIL import Image, ImageTk

import stego

COVER_FILETYPES = [
    ("All Images", "*.png *.jpg *.jpeg *.bmp *.webp *.tiff *.tif"),
    ("PNG images", "*.png"),
    ("JPEG images", "*.jpg *.jpeg"),
    ("BMP images", "*.bmp"),
    ("WebP images", "*.webp"),
    ("TIFF images", "*.tiff *.tif"),
    ("All files", "*.*"),
]

SECRET_FILETYPES = [
    ("All Supported Files", "*.txt *.pdf *.doc *.docx *.png *.jpg *.jpeg"),
    ("Text Files (*.txt)", "*.txt"),
    ("Document Files (*.pdf, *.doc, *.docx)", "*.pdf *.doc *.docx"),
    ("Image Files (*.png, *.jpg, *.jpeg)", "*.png *.jpg *.jpeg"),
    ("All Files", "*.*"),
]
THUMB_SIZE = (160, 160)


class StegPanel(ttk.LabelFrame):
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
        self.cover_thumb = None

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
        size = os.path.getsize(path)
        self.secret_label.config(text=f"{os.path.basename(path)} ({size:,} bytes)")

    def _embed(self):
        if not self.cover_path or not self.secret_path:
            messagebox.showwarning("Missing input", "Select a cover image and a secret file first.")
            return
        output_path = filedialog.asksaveasfilename(
            title="Save stego image as",
            defaultextension=".png",
            initialfile="stego.png",
            filetypes=[("PNG images (*.png)", "*.png")],
        )
        if not output_path:
            return
        try:
            stego.embed_secret(self.cover_path, self.secret_path, output_path)
            self.status_label.config(text=f"Embedded successfully.\nSaved: {output_path}")
            messagebox.showinfo("Success", "Secret file successfully embedded!")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")
            messagebox.showerror("Embedding Error", str(e))

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

        try:
            # Check secret info to auto-suggest original extension
            _, ext = stego.inspect_secret_info(self.stego_path)
            default_ext = ext if ext else ""
            default_name = f"extracted_secret{default_ext}"
            filter_spec = [(f"{default_ext} file", f"*{default_ext}")] if default_ext else []
            filter_spec.append(("All files", "*.*"))

            output_path = filedialog.asksaveasfilename(
                title="Save extracted file as",
                initialfile=default_name,
                defaultextension=default_ext,
                filetypes=filter_spec,
            )
            if not output_path:
                return

            stego.extract_secret(self.stego_path, output_path)
            self.status_label.config(text=f"Extracted successfully.\nSaved: {output_path}")
            messagebox.showinfo("Success", f"Secret file saved to:\n{output_path}")
        except Exception as e:
            self.status_label.config(text=f"Extraction failed: {e}")
            messagebox.showerror("Extraction Error", str(e))

    def _clear(self):
        self.stego_path = None
        self.stego_thumb = None
        self.stego_label.config(text="No stego image selected")
        self.stego_preview.config(image="")
        self.status_label.config(text="")