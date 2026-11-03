import sys
import base64
import io
import asyncio
from pathlib import Path
from PIL import Image, ImageDraw

backend_path = Path("/Users/amrutachari/Desktop/floraAI/backend")
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "venv/lib/python3.9/site-packages"))

import plant_ai

plant_dir = Path("/Users/amrutachari/Desktop/floraAI/frontend/public/plants")

def img_to_b64(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

async def test_all():
    print("=================================================================")
    print("FLORAai VERIFICATION: 12 PLANTS IN KANNADA & DISEASE DIAGNOSTICS")
    print("=================================================================")

    target_plants = [
        ("coconut.jpg", "Coconut Palm"),
        ("rose.jpg", "Rose"),
        ("bismarck_palm.jpg", "Bismarck Palm"),
        ("lipstick_palm.jpg", "Lipstick Palm"),
        ("badam.jpg", "Badam Plant"),
        ("tulsi.jpg", "Tulsi"),
        ("neem.jpg", "Neem Tree"),
        ("mango.jpg", "Mango Tree"),
        ("snake_plant.jpg", "Snake Plant"),
        ("rice.jpg", "Rice / Paddy"),
        ("aloe_vera.jpg", "Aloe Vera"),
        ("curry_leaf.jpg", "Curry Leaf"),
    ]

    all_passed = True

    print("\n--- TEST 1: AUTO-DETECTION & KANNADA TAXONOMY ACROSS ALL 12 PLANTS ---")
    for filename, expected_substr in target_plants:
        img_path = plant_dir / filename
        im = Image.open(img_path).convert("RGB")
        b64 = img_to_b64(im)

        # Call local diagnostic analyzer with Auto-detect (empty plant_name)
        res = plant_ai._fallback_result("", b64)

        name = res.get("plant_name", "")
        kannada = res.get("kannada_name", "")
        status = res.get("status", "")
        score = res.get("health_score", 0)

        match = expected_substr.lower() in name.lower()
        has_kannada = len(kannada) > 0 and any(ord(c) >= 0x0C80 and ord(c) <= 0x0CFF for c in kannada)

        if match and has_kannada and status == "Healthy":
            print(f"  [PASS] {filename:18} -> {name} | Kannada: {kannada} (Score: {score})")
        else:
            print(f"  [FAIL] {filename:18} -> {name} | Kannada: {kannada} (Status: {status}, Match: {match}, Kannada: {has_kannada})")
            all_passed = False

    print("\n--- TEST 2: PROBLEM PLANT (COCONUT WITH BROWN NECROTIC LEAF SPOTS) ---")
    coco_im = Image.open(plant_dir / "coconut.jpg").convert("RGB").resize((128, 128))
    draw = ImageDraw.Draw(coco_im)
    for cx, cy in [(40, 50), (60, 75), (85, 45), (70, 95), (50, 80), (90, 80), (35, 65)]:
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(130, 45, 20))
    b64_prob = img_to_b64(coco_im)
    res_prob = plant_ai._fallback_result("Coconut Palm (Tengina Mara / Nariyal)", b64_prob)

    print(f"  Plant: {res_prob.get('plant_name')}")
    print(f"  Kannada: {res_prob.get('kannada_name')}")
    print(f"  Status: {res_prob.get('status')}")
    print(f"  Health Score: {res_prob.get('health_score')}/100")
    print(f"  Diagnosis: {res_prob.get('diagnosis')[:75]}...")

    if res_prob.get("status") in ("Leaf Spot", "Blight") and res_prob.get("health_score") < 70:
        print("  [PASS] Problem plant accurately diagnosed with reduced health score and disease status!")
    else:
        print("  [FAIL] Problem coconut was not diagnosed as diseased!")
        all_passed = False

    print("\n--- TEST 3: NON-PLANT REJECTION (SOLID GRAY / BLANK NOISE) ---")
    gray_im = Image.new("RGB", (128, 128), color=(128, 128, 128))
    b64_gray = img_to_b64(gray_im)
    res_gray = plant_ai._fallback_result("", b64_gray)

    print(f"  Plant Name: {res_gray.get('plant_name')}")
    print(f"  Kannada: {res_gray.get('kannada_name')}")
    print(f"  Status: {res_gray.get('status')}")
    print(f"  Health Score: {res_gray.get('health_score')}")
    print(f"  Confidence: {res_gray.get('confidence')}")

    if res_gray.get("status") == "Unknown" and res_gray.get("health_score") == 0:
        print("  [PASS] Non-plant successfully rejected with health_score=0 and status=Unknown!")
    else:
        print("  [FAIL] Non-plant was not rejected!")
        all_passed = False

    print("\n=================================================================")
    print(f"FINAL RESULT: {'ALL TESTS PASSED (100% OK)' if all_passed else 'SOME TESTS FAILED'}")
    print("=================================================================")

if __name__ == "__main__":
    asyncio.run(test_all())
