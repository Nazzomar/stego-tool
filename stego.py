import os
import struct
import numpy as np
from PIL import Image

MAGIC = b"STEG"


def _bytes_to_bits(data: bytes) -> np.ndarray:
    """Unpacks a bytes object into a 1D NumPy array of 0s and 1s."""
    arr = np.frombuffer(data, dtype=np.uint8)
    return np.unpackbits(arr)


def _bits_to_bytes(bits: np.ndarray) -> bytes:
    """Packs a 1D NumPy array of bits into bytes."""
    return np.packbits(bits).tobytes()


def embed_secret(cover_path: str, secret_path: str, output_path: str) -> None:
    # Read the secret file as raw bytes (handles .txt, .pdf, .doc, .png, .jpg, etc.)
    with open(secret_path, "rb") as f:
        secret_bytes = f.read()

    # Preserve the secret file's extension
    _, ext = os.path.splitext(secret_path)
    ext_bytes = ext.lower().encode("utf-8")

    # Header structure:
    # 4 bytes: Magic bytes ("STEG")
    # 4 bytes (uint32): Payload length in bytes
    # 1 byte  (uint8): Extension length in bytes
    # N bytes: Extension string
    header = struct.pack(">4sIB", MAGIC, len(secret_bytes), len(ext_bytes)) + ext_bytes
    full_payload = header + secret_bytes
    payload_bits = _bytes_to_bits(full_payload)

    img = Image.open(cover_path).convert("RGB")
    pixels = np.array(img, dtype=np.uint8)

    max_capacity_bits = pixels.size
    if len(payload_bits) > max_capacity_bits:
        max_bytes = max_capacity_bits // 8
        raise ValueError(
            f"Cover image is too small to embed the secret file.\n"
            f"Required: {len(full_payload):,} bytes\n"
            f"Max Capacity: {max_bytes:,} bytes"
        )

    # Flatten pixel array for sequential bit replacement
    flat_pixels = pixels.ravel()

    # Clear LSB using unsigned byte mask 0xFE and write payload bits
    flat_pixels[: len(payload_bits)] = (
        flat_pixels[: len(payload_bits)] & 0xFE
    ) | payload_bits

    # Save output as lossless PNG
    output_img = Image.fromarray(flat_pixels.reshape(pixels.shape))
    output_img.save(output_path, format="PNG")


def inspect_secret_info(stego_path: str) -> tuple[int, str]:
    """Reads the stego header and returns (file_size, extension)."""
    img = Image.open(stego_path).convert("RGB")
    flat_pixels = np.array(img, dtype=np.uint8).ravel()

    # Read minimal header size: 4 (magic) + 4 (size) + 1 (ext_len) = 9 bytes (72 bits)
    header_bits = flat_pixels[: 9 * 8] & 1
    header_bytes = _bits_to_bytes(header_bits)

    magic, data_len, ext_len = struct.unpack(">4sIB", header_bytes[:9])
    if magic != MAGIC:
        raise ValueError("No valid steganography signature detected in this image.")

    total_header_bytes = 9 + ext_len
    full_header_bits = flat_pixels[: total_header_bytes * 8] & 1
    ext = _bits_to_bytes(full_header_bits)[9:total_header_bytes].decode("utf-8", errors="ignore")

    return data_len, ext


def extract_secret(stego_path: str, output_path: str) -> None:
    img = Image.open(stego_path).convert("RGB")
    flat_pixels = np.array(img, dtype=np.uint8).ravel()

    # Read first 9 bytes
    header_bits = flat_pixels[: 9 * 8] & 1
    header_bytes = _bits_to_bytes(header_bits)

    magic, data_len, ext_len = struct.unpack(">4sIB", header_bytes[:9])
    if magic != MAGIC:
        raise ValueError("No valid hidden file found in the selected image.")

    total_header_bytes = 9 + ext_len
    total_needed_bits = (total_header_bytes + data_len) * 8

    if total_needed_bits > flat_pixels.size:
        raise ValueError("Stego image metadata is corrupted or incomplete.")

    payload_bits = flat_pixels[total_header_bytes * 8 : total_needed_bits] & 1
    secret_bytes = _bits_to_bytes(payload_bits)[:data_len]

    with open(output_path, "wb") as f:
        f.write(secret_bytes)