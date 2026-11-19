#!/usr/bin/env python3
"""Entry point for the news-image-20261119 entry.

Copies entry.png (next to this file) to the output directory:
$MAKEFUN_OUTPUT_DIR if set, otherwise /output.
Validates the PNG magic bytes and the 1 MiB size limit, then prints
the sha256 of the copied file. Standard library only.
"""
import hashlib
import os
import shutil
import sys

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1048576  # 1 MiB


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst = os.path.join(out_dir, "entry.png")

    if not os.path.isfile(src):
        print(f"error: source file not found: {src}", file=sys.stderr)
        return 1

    with open(src, "rb") as f:
        data = f.read()

    if len(data) < len(PNG_MAGIC) or not data.startswith(PNG_MAGIC):
        print("error: entry.png is not a PNG file (bad magic bytes)", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print(f"error: entry.png is {len(data)} bytes, exceeds 1 MiB limit ({MAX_BYTES})",
              file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)

    # Verify the copy is byte-identical to the source.
    with open(dst, "rb") as f:
        copied = f.read()
    digest = hashlib.sha256(data).hexdigest()
    if hashlib.sha256(copied).hexdigest() != digest:
        print("error: copied file does not match source", file=sys.stderr)
        return 1

    print(f"copied {src} -> {dst} ({len(data)} bytes)")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
