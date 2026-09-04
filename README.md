# Steg Tool

IKB21303 (Data Hiding & Encryption) Assignment 2 - build an image steganography tool that hides
secret files inside a cover image and analyzes the result. Group project, 50 marks / 15%.

## What it does

1. Embed secret files: Hide different file types (.txt, .pdf, .doc/.docx, .png, .jpg) inside a cover image using sequential 1-bit LSB (Least Significant Bit) replacement, then save the output as a clean lossless
2. Extract hidden files: Automatically read the hidden header (magic signature, file size, original extension) and extract the exact file back out without losing its original format.
3. Analyze cover vs. stego images: Compare the original and stego images side-by-side:
	- File size on disk and size difference calculation.
	- LSB bit-plane visualizer that amplifies the lowest bits ($255 \times \text{LSB}$) to show the exact modified area versus the original image.
	- Pixel statistics showing the total number of changed pixels and percentage of capacity used.

## Tech stack

- **Language:** Python 3
- **GUI:** `tkinter` / `ttk` (built-in Python GUI library, so no extra web frameworks or complex setups needed)
- **Image processing:** [Pillow](https://python-pillow.org/) (PIL) for opening, converting, and saving images
- **Visualization:** [matplotlib](https://matplotlib.org/), embedded into Tkinter using `FigureCanvasTkAgg` to plot the analysis graphs
- **Bit & array operations:** [numpy](https://numpy.org/) for fast pixel manipulation and bit unpacking/packing

## Setup

### Windows

Tkinter is already installed with Python on Windows. Just run:

```
pip install -r requirements.txt
python main.py
```

### Linux

If Tkinter is missing on your distribution, install it first:

```
# Arch
sudo pacman -S tk

# Debian / Ubuntu
sudo apt install python3-tk
```

Then start the application:

```
pip install -r requirements.txt
python main.py
```

## Project structure

- `main.py` - Sets up the main window and splits the screen into two separate panels (left for steganography, right for analysis).
- `stego_panel.py` - Handles the Steganography Tool tab on the left:
	-> Lets users browse cover images and secret files (.txt, .pdf, .doc, .png, .jpg)
	-> Includes embed and extract buttons with clear status messages.
- `stego.py` - The core steganography logic:
	-> Reads the payload in raw bytes so any file format can be hidden.
	-> Adds a custom header (STEG signature + length + extension) before the secret data so we know what file to extract later.
	-> Uses 8-bit unsigned masks (0xFE) to avoid -2 integer overflow errors when modifying pixel bits.
- `analyzer_panel.py` - Handles the Analyzer tab on the right:
	-> Loads cover and stego images independently to compare past work.
	-> Calculates file size differences on disk.
	-> Renders the LSB plane to highlight exactly where data was written.
- `requirements.txt` - Lists the Python libraries we used (Pillow, numpy, matplotlib).

## Design notes

1. Why cover images can be anything, but stego must be PNG:
	- We allowed multiple input image types (.jpg, .png, .bmp, etc.) so the user has flexibility when picking a cover picture.
	- However, the stego image must be saved as a lossless .png. If saved as a JPEG, lossy compression modifies pixel values when writing to disk, which immediately corrupts our embedded LSB data.
2. Raw binary reading:
	- SBy reading files using "rb" and writing using "wb", the program treats text files, PDFs, Word documents, and images identically as pure binary data.
3. Saving the file extension:
	- Because we store the original extension inside our custom header, the user does not have to guess whether the extracted file was a .pdf or a .txt during recovery.
4. Capacity check:
	- The program multiplies $\text{width} \times \text{height} \times 3 \text{ channels}$ to calculate the maximum number of bits available before attempting to embed. If the file is too big for the image, it stops and displays an error message.
5. Why normal histograms look identical:
	- Changing the last bit alters a pixel value by only $+1$ or $-1$ out of 255. Because human eyes and standard histogram bins cannot easily spot a 1-value shift, the visual quality check uses an amplified LSB bit-plane to clearly show the altered pixel noise.  

## Project status

- Steg Tool Logic (stego.py): Completed (embedding, extraction, and header handling).
- Steg Tool UI (stego_panel.py): Completed (file filters added and connected to backend).
- Analyzer (analyzer_panel.py): Completed (size comparison and LSB plane visualizer working).

## Team

Najmi, Qayyum, Khalif, Nazir
