"""Runner entry news-image-20261119 v3 (stdlib saja).

Memvalidasi entry.png (magic PNG + batas 1 MiB), menyalinnya ke
direktori output ($MAKEFUN_OUTPUT_DIR, default /output), lalu
memverifikasi salinan byte-per-byte dan mencetak sha256-nya.
"""
import hashlib
import os
import shutil
import sys

LIMIT = 1048576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("entry.png not found", file=sys.stderr)
        return 1
    with open(src, "rb") as fh:
        head = fh.read(8)
    if head != PNG_MAGIC:
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    size = os.path.getsize(src)
    if size > LIMIT:
        print(f"entry.png too big: {size} > {LIMIT}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    src_hash, dst_hash = digest(src), digest(dst)
    if src_hash != dst_hash:
        print("copy mismatch", file=sys.stderr)
        return 1
    print(f"entry.png {size} bytes sha256 {dst_hash}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
