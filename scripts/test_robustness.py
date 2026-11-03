from PIL import Image, ImageEnhance
import numpy as np
import io
import base64
from pathlib import Path
import sys

backend_path = Path("/Users/amrutachari/Desktop/floraAI/backend")
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "venv/lib/python3.9/site-packages"))

import plant_ai

plant_dir = Path("/Users/amrutachari/Desktop/floraAI/frontend/public/plants")
plants = [
    "coconut", "rose", "bismarck_palm", "lipstick_palm", "badam",
    "tulsi", "neem", "mango", "snake_plant", "rice", "aloe_vera", "curry_leaf"
]

def to_b64(im):
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode()

def check_match(target, res_name):
    clean = target.replace("_palm", "").replace("_plant", "").replace("_leaf", "").replace("_vera", "").lower()
    return clean in res_name.lower()

print("Testing robustness of visual auto-detection on transformations:")
for p in plants:
    im = Image.open(plant_dir / f"{p}.jpg").convert("RGB")
    w, h = im.size

    # 1. Zoom 15%
    im_zoom = im.crop((int(w * 0.08), int(h * 0.08), int(w * 0.92), int(h * 0.92)))
    res_zoom = plant_ai._fallback_result("", to_b64(im_zoom))

    # 2. Brightness 1.2
    im_bright = ImageEnhance.Brightness(im).enhance(1.2)
    res_bright = plant_ai._fallback_result("", to_b64(im_bright))

    # 3. Rotate 10 deg
    im_rot = im.rotate(10, expand=False)
    res_rot = plant_ai._fallback_result("", to_b64(im_rot))

    mz = check_match(p, res_zoom.get("plant_name", ""))
    mb = check_match(p, res_bright.get("plant_name", ""))
    mr = check_match(p, res_rot.get("plant_name", ""))

    print(f"{p:15} | Zoom: {res_zoom.get('plant_name', '')[:22]:22} ({mz}) | Bright: {res_bright.get('plant_name', '')[:22]:22} ({mb}) | Rot: {res_rot.get('plant_name', '')[:22]:22} ({mr})")
