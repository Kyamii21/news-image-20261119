#!/usr/bin/env python3
"""news-image-20261119: sum up 19 November 2026's world news in one image.

The entry image is shipped in this repository as entry.png (a 1024x1024
PNG drawn with PIL from facts verified against Reuters, NYT, BBC, NASA,
AP and CNN on 19 November 2026). This program copies those exact bytes
to /output/entry.png. It uses only the Python standard library, makes no
network access, and writes identical bytes on every run.

For local testing, DEST_DIR (or MAKEFUN_OUTPUT_DIR) may override the
output directory; the default is /output.
"""

import hashlib
import os
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1
    data = source.read_bytes()
    if not data.startswith(PNG_MAGIC):
        print("error: entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) > 1_048_576:
        print("error: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    # The competition requires exactly 1024x1024: read the PNG IHDR chunk
    # (8-byte signature, 4-byte length, 4-byte type "IHDR", then width and
    # height as big-endian uint32) and refuse anything else.
    if len(data) < 29 or data[12:16] != b"IHDR":
        print("error: entry.png has no IHDR chunk", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        print(f"error: entry.png is {width}x{height}, expected 1024x1024",
              file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("DEST_DIR")
                   or os.environ.get("MAKEFUN_OUTPUT_DIR")
                   or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    dest.write_bytes(data)
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")
    print(f"sha256 {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
