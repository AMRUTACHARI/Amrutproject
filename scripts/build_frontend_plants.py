# Generate frontend/src/lib/indianPlants.js with curated Indian plants
# and authentic verified photography from frontend/public/plants/
import sys
import json
from pathlib import Path

backend_path = Path("/Users/amrutachari/Desktop/floraAI/backend")
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "venv/lib/python3.9/site-packages"))

import plant_ai

plants = plant_ai.EXPANDED_BOTANICAL_KNOWLEDGE

photo_mapping = {
    "Coconut Palm": "/plants/coconut.jpg",
    "Rose": "/plants/rose.jpg",
    "Bismarck Palm": "/plants/bismarck_palm.jpg",
    "Lipstick Palm": "/plants/lipstick_palm.jpg",
    "Badam Plant": "/plants/badam.jpg",
    "Tulsi": "/plants/tulsi.jpg",
    "Neem Tree": "/plants/neem.jpg",
    "Mango Tree": "/plants/mango.jpg",
    "Snake Plant": "/plants/snake_plant.jpg",
    "Rice / Paddy": "/plants/rice.jpg",
    "Aloe Vera": "/plants/aloe_vera.jpg",
    "Curry Leaf": "/plants/curry_leaf.jpg",
}

alias_map = [
    [["coconut", "tengu", "tengina mara", "nariyal", "thennai", "cocos", "ತೆಂಗಿನ ಮರ", "ತೆಂಗು"], "Coconut Palm"],
    [["rose", "gulabi", "gulabi gida", "rosa", "ಗುಲಾಬಿ", "ಗುಲಾಬಿ ಗಿಡ", "gulab"], "Rose"],
    [["bismarck", "bismarque", "bismarckia", "silver fan palm", "belli bisanige", "belli taale", "ಬೆಳ್ಳಿ ಬೀಸಣಿಗೆ ತಾಳೆ", "ಬೆಳ್ಳಿ ತಾಳೆ"], "Bismarck Palm"],
    [["lipstick", "sealing wax palm", "kempu taale", "ಕೆಂಪು ತಾಳೆ", "ಲಿಪ್‌ಸ್ಟಿಕ್", "cyrtostachys", "red palm"], "Lipstick Palm"],
    [["badam", "badami", "badami gida", "indian almond", "sea almond", "ಬಾದಾಮಿ", "ಬಾದಾಮಿ ಗಿಡ", "terminalia"], "Badam Plant"],
    [["tulsi", "holy basil", "thulasi", "tulasi", "ತುಳಸಿ", "ocimum"], "Tulsi"],
    [["neem", "bevu", "bevina mara", "ಬೇವಿನ ಮರ", "ಬೇವು", "azadirachta", "margosa"], "Neem Tree"],
    [["mango", "maavu", "mavina mara", "ಮಾವಿನ ಮರ", "ಮಾವು", "aam", "mangifera", "badami mango"], "Mango Tree"],
    [["snake plant", "haavu gida", "ಹಾವು ಗಿಡ", "sansevieria", "mother in law", "dracaena"], "Snake Plant"],
    [["rice", "paddy", "bhatta", "bhattada gadde", "ಭತ್ತ", "ಭತ್ತದ ಗದ್ದೆ", "dhan", "nel", "oryza"], "Rice / Paddy"],
    [["aloe", "lolesara", "ಲೋಳೆಸರ", "ghritkumari", "katralai"], "Aloe Vera"],
    [["curry", "karibevu", "ಕರಿಬೇವು", "kadi patta", "murraya"], "Curry Leaf"],
]

lines = [
    "// Verified, authentic local photographs of LIVING plant species",
    "// Stored locally in frontend/public/plants/ for guaranteed thumbnail presentation",
    "export const REAL_PLANT_PHOTOS = " + json.dumps(photo_mapping, indent=2) + ";",
    "",
    "const ALIAS_MAP = " + json.dumps(alias_map, indent=2) + ";",
    "",
    "export function getPlantImage(name = '') {",
    "  const n = (name || '').toLowerCase();",
    "  const match = ALIAS_MAP.find(([keys]) => keys.some((k) => n.includes(k)));",
    "  return match ? (REAL_PLANT_PHOTOS[match[1]] || '/plants/coconut.jpg') : '/plants/coconut.jpg';",
    "}",
    "",
    "// Curated Indian botanical species with authentic Kannada (ಕನ್ನಡ) taxonomy",
    "export const INDIAN_SUBCONTINENT_PLANTS = " + json.dumps(plants, indent=2) + ";",
    "",
    "// Signature gallery plants - 10 curated species for minimalist display",
    "export const SIGNATURE_GALLERY_STEMS = [",
    '  "coconut",',
    '  "bismarck_palm",',
    '  "lipstick_palm",',
    '  "rice",',
    '  "mango",',
    '  "neem",',
    '  "tulsi",',
    '  "aloe_vera",',
    '  "curry_leaf",',
    '  "snake_plant",',
    "];",
    "",
    "export const SIGNATURE_GALLERY_PLANTS = SIGNATURE_GALLERY_STEMS.map((stem) =>",
    "  INDIAN_SUBCONTINENT_PLANTS.find((p) => p.stem === stem)",
    ").filter(Boolean);",
    "",
]

out_file = Path("/Users/amrutachari/Desktop/floraAI/frontend/src/lib/indianPlants.js")
out_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Successfully generated {out_file} with {len(plants)} synchronized plants in Kannada taxonomy")
