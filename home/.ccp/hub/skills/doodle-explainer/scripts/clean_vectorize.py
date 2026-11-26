#!/usr/bin/env python3
"""Invert Nano Banana Pro bottom-right Gemini star watermark, flood-fill outer white, and vectorize to SVG.

Run via Python 3.12 (vtracer segfaults on Python 3.15):
  uv run --python 3.12 --with vtracer --with pillow --with numpy \
    python scripts/clean_vectorize.py input.webp output.svg \
    --alpha assets/gemini_star_alpha.npy [--crop 0.0,0.0,0.5,0.5] [--keep-bg]
"""
from __future__ import annotations

import argparse
from collections import deque
import pathlib
import numpy as np
from PIL import Image
import vtracer


def invert_gemini_watermark(im: Image.Image, alpha_path: pathlib.Path | None) -> Image.Image:
    if not alpha_path or not alpha_path.is_file():
        return im.convert("RGB")
    alpha = np.load(alpha_path)
    arr = np.array(im.convert("RGB"), dtype=np.float32)
    h, w, _ = arr.shape
    if alpha.shape != (h, w):
        a_im = Image.fromarray((np.clip(alpha, 0.0, 1.0) * 255).astype(np.uint8)).resize((w, h), Image.Resampling.BILINEAR)
        alpha = np.array(a_im, dtype=np.float32) / 255.0
    a3 = alpha[:, :, None]
    inv = np.where(a3 > 0.01, (arr - a3 * 255.0) / np.maximum(1.0 - a3, 0.05), arr)
    return Image.fromarray(np.clip(np.round(inv), 0, 255).astype(np.uint8), "RGB")


def remove_outer_white(im: Image.Image, thresh: int = 236) -> Image.Image:
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    visited = bytearray(w * h)
    q: deque[tuple[int, int]] = deque()

    def is_white(x: int, y: int) -> bool:
        r, g, b, _ = px[x, y]
        return r >= thresh and g >= thresh and b >= thresh

    for x in range(w):
        for y in (0, h - 1):
            if is_white(x, y):
                visited[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not visited[y * w + x] and is_white(x, y):
                visited[y * w + x] = 1
                q.append((x, y))

    while q:
        x, y = q.popleft()
        px[x, y] = (255, 255, 255, 0)
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                idx = ny * w + nx
                if not visited[idx] and is_white(nx, ny):
                    visited[idx] = 1
                    q.append((nx, ny))
    return im


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=pathlib.Path)
    ap.add_argument("output", type=pathlib.Path)
    ap.add_argument("--alpha", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parent.parent / "assets" / "gemini_star_alpha.npy")
    ap.add_argument("--crop", help="Optional fractional crop box x0,y0,x1,y1 (e.g. 0.0,0.0,0.5,0.5)")
    ap.add_argument("--keep-bg", action="store_true", help="Keep full background (for colored interior scenes)")
    ap.add_argument("--no-trim", action="store_true", help="Do not auto-trim transparent margins (for 16:9 full scenes)")
    ap.add_argument("--thresh", type=int, default=236)
    args = ap.parse_args()

    im = invert_gemini_watermark(Image.open(args.input), args.alpha)
    if args.crop:
        x0, y0, x1, y1 = [float(v) for v in args.crop.split(",")]
        w, h = im.size
        im = im.crop((int(x0 * w), int(y0 * h), int(x1 * w), int(y1 * h)))

    if args.keep_bg:
        rgba = im.convert("RGBA")
    else:
        rgba = remove_outer_white(im, thresh=args.thresh)
        if not args.no_trim:
            bbox = rgba.getbbox()
            if bbox:
                pad = 6
                rgba = rgba.crop((max(0, bbox[0] - pad), max(0, bbox[1] - pad), min(rgba.width, bbox[2] + pad), min(rgba.height, bbox[3] + pad)))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    tmp_png = args.output.with_suffix(".tmp.png")
    rgba.save(tmp_png)
    try:
        vtracer.convert_image_to_svg_py(
            str(tmp_png),
            str(args.output),
            colormode="color",
            hierarchical="stacked",
            mode="spline",
            filter_speckle=10,
            color_precision=6,
            layer_difference=18,
            corner_threshold=60,
            length_threshold=4.0,
            splice_threshold=45,
            path_precision=2,
        )
    finally:
        tmp_png.unlink(missing_ok=True)
    print(f"OK {args.output} ({rgba.width}x{rgba.height}, {args.output.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
