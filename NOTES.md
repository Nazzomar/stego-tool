# stego.py - things to agree on before implementing

`embed_secret(cover_path, secret_path, output_path)` and `extract_secret(stego_path, output_path)`
are stubs in `stego.py`. Signatures are fixed (the UI already calls them), but the internals need
these decisions locked in first:

1. **Payload framing** - embed a fixed-size length header (e.g. first 32 bits = payload byte count)
   right before the payload bits, so extraction knows how many bits to read back.
2. **Filename/extension recovery** - store the original filename+extension in the header too (length
   + name + payload length + payload), so extraction can reconstruct `secret.pdf` etc. automatically
   instead of the user having to know/type the extension.
3. **Which bits/channels** - 1 LSB per color channel (R, G, B), sequential across pixels. Must match
   exactly between embed and extract or extraction returns garbage with no error.
4. **Image mode normalization** - always `.convert("RGB")` the cover before touching pixel bytes
   (drops alpha), same on both embed and extract, regardless of the source PNG's mode.
5. **Capacity error type** - if the secret doesn't fit the cover's capacity, agree on one exception
   type (e.g. `ValueError` with a message) so `stego_panel.py` can catch and display it specifically,
   not just crash. `stego_panel.py` currently only catches `NotImplementedError`.
6. **Output is always PNG** - regardless of the extension typed in the save dialog, write lossless
   PNG so the hidden data can't be silently destroyed by re-encoding to JPG.
