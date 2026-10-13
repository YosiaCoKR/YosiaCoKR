"""Prep a portrait for ASCII conversion: remove bg, boost local contrast, put on white.

usage: python scripts/prep_photo.py source-photo.jpg   -> source-prepped.png
"""
import sys

import cv2
import numpy as np
from PIL import Image
from rembg import remove

src = Image.open(sys.argv[1]).convert("RGB")
cut = remove(src)  # RGBA, background transparent

gray = cv2.cvtColor(np.array(cut.convert("RGB")), cv2.COLOR_RGB2GRAY)
gray = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8)).apply(gray)

alpha = np.array(cut)[:, :, 3].astype(np.float32) / 255
out = gray * alpha + 255 * (1 - alpha)  # composite onto white -> blank in ASCII
Image.fromarray(out.astype(np.uint8)).save("source-prepped.png")
print("wrote source-prepped.png")
