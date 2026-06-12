# -*- coding: utf-8 -*-
"""Mirror generated assets horizontally.
Usage:
  python flip.py name.png            -> overwrites name.png mirrored
  python flip.py name.png new.png    -> saves mirrored copy as new.png
"""
import os
import sys
from PIL import Image

IMG = os.path.join(os.path.dirname(__file__), "..", "assets", "img")

src = os.path.join(IMG, sys.argv[1])
dst = os.path.join(IMG, sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
img = Image.open(src).transpose(Image.FLIP_LEFT_RIGHT)
img.save(dst, optimize=True)
print(f"flipped {sys.argv[1]} -> {os.path.basename(dst)}")
