"""LSB steganography embed/extract logic.

TODO (teammate): implement embed_secret() and extract_secret() below.
The UI in stego_panel.py already calls these and handles NotImplementedError,
so the app runs end-to-end as soon as these are filled in.
"""


def embed_secret(cover_path: str, secret_path: str, output_path: str) -> None:
    """Hide the file at secret_path inside the image at cover_path, save result to output_path."""
    raise NotImplementedError("embed_secret not implemented yet")


def extract_secret(stego_path: str, output_path: str) -> None:
    """Recover the hidden file from stego_path, save it to output_path."""
    raise NotImplementedError("extract_secret not implemented yet")
