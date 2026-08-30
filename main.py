import tkinter as tk
from tkinter import ttk

from stego_panel import StegPanel
from analyzer_panel import AnalyzerPanel

TEAM_NAMES = ("Najmi", "Qayyum", "Khalif", "Nazir")


def main():
    root = tk.Tk()
    root.title("IKB21303 Assignment 2 - Steganography and Analyzer Tool")
    root.geometry("1000x680")

    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.rowconfigure(0, weight=1)

    StegPanel(root).grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
    AnalyzerPanel(root).grid(row=0, column=1, sticky="nsew", padx=8, pady=8)

    footer = ttk.Label(
        root,
        text="Steg Tool - " + ", ".join(TEAM_NAMES),
        foreground="gray40",
        anchor="center",
        justify="center",
        wraplength=980,
    )
    footer.grid(row=1, column=0, columnspan=2, pady=(0, 6))

    root.mainloop()


if __name__ == "__main__":
    main()
