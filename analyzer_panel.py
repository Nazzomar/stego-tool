"""Right panel: the analyzer UI. Cover and stego images are loaded independently."""
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

IMAGE_FILETYPES = [
    ("All Images", "*.png *.jpg *.jpeg *.bmp *.webp *.tiff *.tif"),
    ("PNG images (*.png)", "*.png"),
    ("JPEG images (*.jpg, *.jpeg)", "*.jpg *.jpeg"),
    ("All files", "*.*"),
]
THUMB_SIZE = (150, 150)


class AnalyzerPanel(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Analyzer")

        self.cover_path = None
        self.stego_path = None
        self.cover_thumb = None
        self.stego_thumb = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ttk.Button(self, text="Load Cover Image...", command=self._load_cover).grid(
            row=0, column=0, sticky="ew", padx=8, pady=(8, 2)
        )
        ttk.Button(self, text="Load Stego Image...", command=self._load_stego).grid(
            row=0, column=1, sticky="ew", padx=8, pady=(8, 2)
        )

        self.cover_label = ttk.Label(self, text="No cover image loaded")
        self.cover_label.grid(row=1, column=0, sticky="w", padx=8)
        self.stego_label = ttk.Label(self, text="No stego image loaded")
        self.stego_label.grid(row=1, column=1, sticky="w", padx=8)

        self.cover_preview = ttk.Label(self)
        self.cover_preview.grid(row=2, column=0, pady=4)
        self.stego_preview = ttk.Label(self)
        self.stego_preview.grid(row=2, column=1, pady=4)

        button_row = ttk.Frame(self)
        button_row.grid(row=3, column=0, columnspan=2, pady=12)
        ttk.Button(button_row, text="Compare", command=self._compare).pack(side="left", padx=4)
        ttk.Button(button_row, text="Clear", command=self._clear).pack(side="left", padx=4)

        size_box = ttk.Frame(self, relief="groove", borderwidth=2)
        size_box.grid(row=4, column=0, columnspan=2, sticky="ew", padx=8, pady=(4, 8))
        self.size_label = ttk.Label(
            size_box, text="", justify="left", font=("TkDefaultFont", 12, "bold"), padding=8
        )
        self.size_label.pack(fill="x")

        self.figure = Figure(figsize=(7.5, 4.2), dpi=95)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=2, pady=8)

    def _load_cover(self):
        path = filedialog.askopenfilename(title="Select cover image", filetypes=IMAGE_FILETYPES)
        if not path:
            return
        self.cover_path = path
        self.cover_label.config(text=os.path.basename(path))
        self.cover_thumb = self._make_thumb(path)
        self.cover_preview.config(image=self.cover_thumb)

    def _load_stego(self):
        path = filedialog.askopenfilename(title="Select stego image", filetypes=IMAGE_FILETYPES)
        if not path:
            return
        self.stego_path = path
        self.stego_label.config(text=os.path.basename(path))
        self.stego_thumb = self._make_thumb(path)
        self.stego_preview.config(image=self.stego_thumb)

    @staticmethod
    def _make_thumb(path):
        image = Image.open(path)
        image.thumbnail(THUMB_SIZE)
        return ImageTk.PhotoImage(image)

    def _compare(self):
        if not self.cover_path or not self.stego_path:
            messagebox.showwarning("Missing input", "Load both a cover image and a stego image first.")
            return

        cover_size = os.path.getsize(self.cover_path)
        stego_size = os.path.getsize(self.stego_path)
        diff = stego_size - cover_size
        self.size_label.config(
            text=(
                f"Cover size: {cover_size:,} bytes\n"
                f"Stego size: {stego_size:,} bytes\n"
                f"Difference: {diff:+,} bytes"
            )
        )
        self._plot_histograms()

    def _plot_histograms(self):
        from scipy.stats import gaussian_kde

        cover = np.array(Image.open(self.cover_path).convert("RGB"))
        stego = np.array(Image.open(self.stego_path).convert("RGB"))

        self.figure.clear()
        ax1 = self.figure.add_subplot(1, 2, 1)
        ax2 = self.figure.add_subplot(1, 2, 2)

        channel_styles = [
            {"label": "Red",   "bar_face": "#7ea6e0", "bar_edge": "#2b4c7e", "line": "#0018d6"},  
            {"label": "Green", "bar_face": "#e5a19b", "bar_edge": "#80332c", "line": "#b31a1a"}, 
            {"label": "Blue",  "bar_face": "#94c7b8", "bar_edge": "#295b4e", "line": "#00634f"}, 
        ]

        x_eval = np.linspace(0, 255, 300)

        for ax, img, title in ((ax1, cover, "Cover Image"), (ax2, stego, "Stego Image")):
            for c, style in enumerate(channel_styles):
                data = img[:, :, c].ravel()

                sample_data = np.random.choice(data, size=min(15000, len(data)), replace=False)

                weights = np.ones_like(sample_data) * 100.0 / len(sample_data)
                counts, bin_edges, _ = ax.hist(
                    sample_data,
                    bins=32,
                    range=(0, 255),
                    weights=weights,
                    facecolor=style["bar_face"],
                    edgecolor=style["bar_edge"],
                    linewidth=0.9,
                    alpha=0.45,
                    label=style["label"],
                )

                kde = gaussian_kde(sample_data)
                bin_width = bin_edges[1] - bin_edges[0]
                kde_curve = kde(x_eval) * 100.0 * bin_width
                ax.plot(x_eval, kde_curve, color=style["line"], linewidth=2.0)

            ax.set_title(f" ({title})", fontsize=11, fontweight="bold", pad=8)
            ax.set_ylabel("Percent", fontsize=10)
            ax.set_xlim(0, 255)
            ax.set_ylim(bottom=0)
            
            ax.yaxis.grid(True, linestyle="-", alpha=0.5, color="#d3d9de")
            ax.xaxis.grid(False)
            ax.set_axisbelow(True)

            for spine in ax.spines.values():
                spine.set_edgecolor("#333333")
                spine.set_linewidth(0.8)

            ax.legend(loc="upper right", frameon=True, edgecolor="#555555", facecolor="#f8f9fa", fontsize=9)

        self.figure.tight_layout()
        self.canvas.draw()

    def _clear(self):
        self.cover_path = None
        self.stego_path = None
        self.cover_thumb = None
        self.stego_thumb = None
        self.cover_label.config(text="No cover image loaded")
        self.stego_label.config(text="No stego image loaded")
        self.cover_preview.config(image="")
        self.stego_preview.config(image="")
        self.size_label.config(text="")
        self.figure.clear()
        self.canvas.draw()
