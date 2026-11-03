import urllib.request
import json
import base64
import uuid
from pathlib import Path
from http.cookiejar import CookieJar

BASE_URL = "http://localhost:8001/api"
plant_dir = Path("/Users/amrutachari/Desktop/floraAI/frontend/public/plants")

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def post_json(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with opener.open(req) as response:
        return json.loads(response.read().decode("utf-8"))

def get_json(url):
    req = urllib.request.Request(url)
    with opener.open(req) as response:
        return json.loads(response.read().decode("utf-8"))

def test_live_api():
    print("Testing live API at", BASE_URL)
    # 1. Test /api/spices
    spices_res = get_json(f"{BASE_URL}/spices")
    spices = spices_res.get("spices", [])
    print(f"1. /api/spices returned {len(spices)} plants:")
    for s in spices[:5]:
        print(f"   - {s['name']} -> Kannada: {s.get('kannada_name')}")
    assert len(spices) >= 40, f"Expected at least 40 species, found {len(spices)}"

    # 2. Register test user (sets auth cookies in opener)
    test_email = f"kannada_tester_{uuid.uuid4().hex[:6]}@example.com"
    reg = post_json(f"{BASE_URL}/auth/register", {
        "name": "Kannada Tester",
        "email": test_email,
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    print("2. Registered user and received auth session cookies.")

    # 3. Test scanning all requested plants
    test_suite = [
        ("coconut.jpg", "Coconut", "ತೆಂಗಿನ"),
        ("rose.jpg", "Rose", "ಗುಲಾಬಿ"),
        ("bismarck_palm.jpg", "Bismarck", "ಬೆಳ್ಳಿ"),
        ("lipstick_palm.jpg", "Lipstick", "ಕೆಂಪು"),
        ("badam.jpg", "Badam", "ಬಾದಾಮಿ"),
        ("tulsi.jpg", "Tulsi", "ತುಳಸಿ"),
        ("neem.jpg", "Neem", "ಬೇವಿನ"),
        ("mango.jpg", "Mango", "ಮಾವಿನ"),
        ("snake_plant.jpg", "Snake", "ಹಾವು"),
        ("rice.jpg", "Rice", "ಭತ್ತದ"),
        ("aloe_vera.jpg", "Aloe", "ಲೋಳೆಸರ"),
        ("curry_leaf.jpg", "Curry", "ಕರಿಬೇವು"),
    ]

    print("\n3. Testing live scans for all requested species:")
    for filename, expected_en, expected_kn in test_suite:
        img_bytes = (plant_dir / filename).read_bytes()
        img_b64 = f"data:image/jpeg;base64,{base64.b64encode(img_bytes).decode('utf-8')}"
        scan_res = post_json(f"{BASE_URL}/scans", {
            "image_base64": img_b64,
            "plant_name": ""  # auto-detect
        })
        scan_data = scan_res.get("scan", {})
        p_name = scan_data.get("plant_name", "")
        kn_name = scan_data.get("kannada_name", "")
        status = scan_data.get("status", "")
        score = scan_data.get("health_score", 0)

        assert expected_en.lower() in p_name.lower(), f"Expected {expected_en} in {p_name}"
        assert expected_kn in kn_name, f"Expected {expected_kn} in {kn_name}"
        print(f"   [PASS] {filename:18} -> {p_name[:30]:30} | {kn_name} | Status: {status} | Health: {score}/100")

    # 4. Test non-plant rejection on live server
    # 64x64 solid gray image
    from PIL import Image
    import io
    gray = Image.new("RGB", (64, 64), color=(128, 128, 128))
    b = io.BytesIO()
    gray.save(b, format="JPEG")
    gray_b64 = f"data:image/jpeg;base64,{base64.b64encode(b.getvalue()).decode('utf-8')}"

    scan_res_reject = post_json(f"{BASE_URL}/scans", {
        "image_base64": gray_b64,
        "plant_name": ""
    })
    rej_data = scan_res_reject.get("scan", {})
    print("\n4. Non-plant rejection test on live server:")
    print("   Plant:", rej_data.get("plant_name"))
    print("   Kannada:", rej_data.get("kannada_name"))
    print("   Status:", rej_data.get("status"))
    print("   Confidence:", rej_data.get("confidence"))
    assert rej_data.get("status") == "Unknown"
    assert rej_data.get("health_score") == 0
    print("   [PASS] Non-plant rejection verified on live server!")

    print("\n=================================================================")
    print("ALL LIVE API VERIFICATION TESTS PASSED (100% SUITE OK)")
    print("=================================================================")

if __name__ == "__main__":
    test_live_api()
