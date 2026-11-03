import httpx
import base64
import uuid
from pathlib import Path
from PIL import Image
import io

client = httpx.Client(base_url="http://localhost:8001", timeout=20.0)

# 1. Test /api/spices
res_spices = client.get("/api/spices")
assert res_spices.status_code == 200, f"Expected 200, got {res_spices.status_code}"
spices_data = res_spices.json().get("spices", [])
print(f"API /api/spices returned {len(spices_data)} species:")
for i, s in enumerate(spices_data, 1):
    print(f"  {i}. {s['name']} | Tamil: {s.get('tamil_name')}")
assert len(spices_data) == 10, f"Expected 10 species, got {len(spices_data)}"

# 2. Register unique user
test_email = f"tester_{uuid.uuid4().hex[:8]}@example.com"
reg_res = client.post(
    "/api/auth/register",
    json={
        "name": "Botanical Tester",
        "email": test_email,
        "password": "Password123!",
        "confirm_password": "Password123!",
        "location": "Chennai, Tamil Nadu",
        "experience": "Farmer / Enthusiast",
        "spice_interest": "Coconut Palm, Bismarck Palm"
    }
)
assert reg_res.status_code == 200, f"Registration failed ({reg_res.status_code}): {reg_res.text}"
print(f"\nUser registered & authenticated: {test_email}")

# 3. Test /api/scans with Coconut Palm photo
coconut_bytes = Path("/Users/amrutachari/Desktop/floraAI/frontend/public/plants/coconut.jpg").read_bytes()
b64_img = base64.b64encode(coconut_bytes).decode("utf-8")

scan_res = client.post(
    "/api/scans",
    json={
        "image_base64": f"data:image/jpeg;base64,{b64_img}",
        "plant_name": "Coconut Palm (Nariyal / Thennai)"
    }
)
assert scan_res.status_code == 200, f"Scan failed ({scan_res.status_code}): {scan_res.text}"
scan_data = scan_res.json().get("scan", {})
print("\n--- Live API Scan: Coconut Palm ---")
print(f"  Plant Name: {scan_data.get('plant_name')}")
print(f"  Tamil Name: {scan_data.get('tamil_name')}")
print(f"  Status: {scan_data.get('status')} [Health Score: {scan_data.get('health_score')}/100, Accuracy: {scan_data.get('confidence')}%]")
print(f"  Diagnosis: {scan_data.get('diagnosis')[:100]}...")
assert scan_data.get("status") == "Healthy"
assert scan_data.get("health_score") >= 90
assert scan_data.get("tamil_name") == "தென்னை (Thennai)"

# 4. Test /api/scans with Bismarck Palm photo
im_bis = Image.open("/Users/amrutachari/Desktop/floraAI/frontend/public/plants/bismarck_palm.jpg").convert("RGB").resize((256, 256))
buf_bis = io.BytesIO()
im_bis.save(buf_bis, format="JPEG", quality=85)
b64_bis = base64.b64encode(buf_bis.getvalue()).decode("utf-8")
bis_res = client.post(
    "/api/scans",
    json={
        "image_base64": f"data:image/jpeg;base64,{b64_bis}",
        "plant_name": "Bismarck Palm (Silver Fan Palm)"
    }
)
assert bis_res.status_code == 200, f"Scan failed: {bis_res.text}"
bis_data = bis_res.json().get("scan", {})
print("\n--- Live API Scan: Bismarck Palm ---")
print(f"  Plant Name: {bis_data.get('plant_name')}")
print(f"  Tamil Name: {bis_data.get('tamil_name')}")
print(f"  Status: {bis_data.get('status')} [Health Score: {bis_data.get('health_score')}/100]")
assert bis_data.get("status") == "Healthy"
assert "வெள்ளி விசிறி" in bis_data.get("tamil_name", "")

# 5. Test Non-Plant Rejection via Live API
dummy_non_plant = Image.new("RGB", (128, 128), (140, 140, 145))
buf = io.BytesIO()
dummy_non_plant.save(buf, format="JPEG")
b64_dummy = base64.b64encode(buf.getvalue()).decode("utf-8")

reject_res = client.post(
    "/api/scans",
    json={
        "image_base64": f"data:image/jpeg;base64,{b64_dummy}",
        "plant_name": "Other / Auto-detect"
    }
)
assert reject_res.status_code == 200, f"Rejection test failed ({reject_res.status_code}): {reject_res.text}"
reject_data = reject_res.json().get("scan", {})
print("\n--- Live API Scan: Non-Plant Rejection ---")
print(f"  Plant Name: {reject_data.get('plant_name')}")
print(f"  Status: {reject_data.get('status')} [Health Score: {reject_data.get('health_score')}/100, Confidence: {reject_data.get('confidence')}%]")
print(f"  Diagnosis: {reject_data.get('diagnosis')}")
assert reject_data.get("status") == "Unknown"
assert reject_data.get("health_score") == 0
assert reject_data.get("confidence") == 0

print("\nALL LIVE API ENDPOINTS AND DIAGNOSTIC BEHAVIORS VERIFIED 100% OPERATIONAL!")
