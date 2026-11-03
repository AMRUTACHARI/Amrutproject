import sys
import os
import base64
import json
from pathlib import Path
from PIL import Image, ImageDraw
import numpy as np

backend_path = Path("/Users/amrutachari/Desktop/floraAI/backend")
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "venv/lib/python3.9/site-packages"))

import plant_ai

print(f"Loaded {len(plant_ai.EXPANDED_BOTANICAL_KNOWLEDGE)} botanical species.")
for i, p in enumerate(plant_ai.EXPANDED_BOTANICAL_KNOWLEDGE, 1):
    print(f" {i}. {p['name']} | Tamil: {p.get('tamil_name')} | Scientific: {p['scientific_name']}")

# Test 1: Real Coconut Palm photo from frontend/public/plants/coconut.jpg
coconut_path = Path("/Users/amrutachari/Desktop/floraAI/frontend/public/plants/coconut.jpg")
b64_coconut = base64.b64encode(coconut_path.read_bytes()).decode("utf-8")
res_coconut = plant_ai._fallback_result("Coconut Palm (Nariyal / Thennai)", b64_coconut)
print("\n--- Test 1: Real Coconut Palm ---")
print(f"Identified: {res_coconut['plant_name']}")
print(f"Tamil Name: {res_coconut.get('tamil_name')}")
print(f"Status: {res_coconut['status']} (Health Score: {res_coconut['health_score']}/100, Confidence: {res_coconut['confidence']}%)")
assert res_coconut['status'] == "Healthy", f"Expected Healthy, got {res_coconut['status']}"
assert res_coconut['health_score'] >= 90

# Test 2: Problem Coconut Palm (simulate fungal brown leaf spots on fronds)
im_spot = Image.open(coconut_path).convert("RGB")
draw = ImageDraw.Draw(im_spot)
# Draw realistic necrotic brown spots with yellow margins
w, h = im_spot.size
for x, y, r in [(w*0.3, h*0.4, w*0.06), (w*0.45, h*0.5, w*0.08), (w*0.6, h*0.35, w*0.07), (w*0.35, h*0.65, w*0.08), (w*0.55, h*0.7, w*0.07)]:
    draw.ellipse([x-r-4, y-r-4, x+r+4, y+r+4], fill=(160, 140, 40)) # yellow halo
    draw.ellipse([x-r, y-r, x+r, y+r], fill=(125, 65, 30)) # brown necrotic center

import io
buf = io.BytesIO()
im_spot.save(buf, format="JPEG")
b64_spot = base64.b64encode(buf.getvalue()).decode("utf-8")
res_spot = plant_ai._fallback_result("Coconut Palm (Nariyal / Thennai)", b64_spot)
print("\n--- Test 2: Problem Coconut Palm (Brown Leaf Spots / Blight) ---")
print(f"Identified: {res_spot['plant_name']}")
print(f"Status: {res_spot['status']} (Health Score: {res_spot['health_score']}/100)")
print(f"Diagnosis: {res_spot['diagnosis']}")
print(f"Issues: {res_spot['issues']}")
print(f"Remedies: {res_spot['remedies'][:2]}")
assert res_spot['status'] in ("Leaf Spot", "Blight"), f"Expected Leaf Spot or Blight, got {res_spot['status']}"
assert res_spot['health_score'] < 70, f"Expected health score < 70 for problem plant, got {res_spot['health_score']}"

# Test 3: Bismarck Palm with verified generated artwork
bismarck_path = Path("/Users/amrutachari/Desktop/floraAI/frontend/public/plants/bismarck_palm.jpg")
b64_bismarck = base64.b64encode(bismarck_path.read_bytes()).decode("utf-8")
res_bismarck = plant_ai._fallback_result("Bismarck Palm (Silver Fan Palm)", b64_bismarck)
print("\n--- Test 3: Bismarck Palm ---")
print(f"Identified: {res_bismarck['plant_name']}")
print(f"Tamil Name: {res_bismarck.get('tamil_name')}")
print(f"Status: {res_bismarck['status']} (Health Score: {res_bismarck['health_score']}/100)")

# Test 4: Rejection of Non-Plant Object (e.g. solid grey wall / non-botanical noise)
non_plant = Image.new("RGB", (200, 200), color=(140, 140, 145))
buf_non = io.BytesIO()
non_plant.save(buf_non, format="JPEG")
b64_non = base64.b64encode(buf_non.getvalue()).decode("utf-8")
res_non = plant_ai._fallback_result("Other / Auto-detect", b64_non)
print("\n--- Test 4: Rejection of Non-Plant / Wall ---")
print(f"Identified: {res_non['plant_name']}")
print(f"Status: {res_non['status']} (Health Score: {res_non['health_score']}/100, Confidence: {res_non['confidence']}%)")
print(f"Diagnosis: {res_non['diagnosis']}")
assert res_non['status'] == "Unknown", f"Expected Unknown, got {res_non['status']}"
assert res_non['health_score'] == 0, f"Expected 0 health score, got {res_non['health_score']}"

# Test 5: Rejection of Pure Black Image
black_im = Image.new("RGB", (150, 150), color=(5, 5, 5))
buf_blk = io.BytesIO()
black_im.save(buf_blk, format="JPEG")
b64_blk = base64.b64encode(buf_blk.getvalue()).decode("utf-8")
res_blk = plant_ai._fallback_result("Other / Auto-detect", b64_blk)
print("\n--- Test 5: Rejection of Black / Corrupt Photo ---")
print(f"Identified: {res_blk['plant_name']}")
print(f"Status: {res_blk['status']} (Health Score: {res_blk['health_score']}/100)")
assert res_blk['status'] == "Unknown"
assert res_blk['health_score'] == 0

print("\nALL 5 BOTANICAL & REJECTION TESTS PASSED PERFECTLY!")
