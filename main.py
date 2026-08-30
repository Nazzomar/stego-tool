import tkinter as tk

from stego_panel import StegPanel
from analyzer_panel import AnalyzerPanel


def main():
    root = tk.Tk()
    root.title("Image Steganography Tool")
    root.geometry("1000x650")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    StegPanel(root).grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    AnalyzerPanel(root).grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

    root.mainloop()


if __name__ == "__main__":
    main()
