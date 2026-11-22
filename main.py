#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261122.

Copies the front-page image (entry.png, built by build_image.py) from this
repository to the grader's output directory as entry.png.
"""

import os
import shutil
from pathlib import Path


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1024 * 1024  # the bounty's 1 MiB cap


def check_source(src: Path) -> None:
    """Fail loudly rather than hand the grader a bad file."""
    if not src.is_file():
        raise SystemExit(f"missing image: {src}")
    data = src.read_bytes()
    if not data.startswith(PNG_MAGIC):
        raise SystemExit(f"not a PNG file: {src}")
    if len(data) > MAX_BYTES:
        raise SystemExit(f"image is {len(data)} bytes, over the 1 MiB cap: {src}")


def main() -> None:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    check_source(src)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
