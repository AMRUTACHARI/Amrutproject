# Generate frontend/src/lib/indianPlants.js from plant_ai.py
import sys
import json
from pathlib import Path

# Add backend directory to path
backend_path = Path("/Users/amrutachari/Desktop/floraAI/backend")
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "venv/lib/python3.9/site-packages"))

import plant_ai

plants = plant_ai.EXPANDED_BOTANICAL_KNOWLEDGE

photo_mapping = {
    "Coconut Palm": "/plants/coconut.jpg",
    "Areca Palm": "/plants/areca.jpg",
    "Palmyra Palm": "/plants/palmyra.jpg",
    "Bamboo": "/plants/bamboo.jpg",
    "Banana": "/plants/banana.jpg",
    "Rice (Paddy)": "/plants/rice.jpg",
    "Wheat": "/plants/wheat.jpg",
    "Sugarcane": "/plants/sugarcane.jpg",
    "Cotton": "/plants/cotton.jpg",
    "Tea": "/plants/tea.jpg",
    "Coffee": "/plants/coffee.jpg",
    "Mustard": "/plants/mustard.jpg",
    "Mango": "/plants/mango.jpg",
    "Guava": "/plants/guava.jpg",
    "Papaya": "/plants/papaya.jpg",
    "Lemon": "/plants/lemon.jpg",
    "Pomegranate": "/plants/pomegranate.jpg",
    "Jackfruit": "/plants/jackfruit.jpg",
    "Amla": "/plants/amla.jpg",
    "Tomato": "/plants/tomato.jpg",
    "Brinjal": "/plants/brinjal.jpg",
    "Green Chilli": "/plants/chilli.jpg",
    "Coriander": "/plants/coriander.jpg",
    "Fenugreek": "/plants/fenugreek.jpg",
    "Drumstick (Moringa)": "/plants/moringa.jpg",
    "Hibiscus": "/plants/hibiscus.jpg",
    "Jasmine": "/plants/jasmine.jpg",
    "Rose": "/plants/rose.jpg",
    "Marigold": "/plants/marigold.jpg",
    "Plumeria": "/plants/champa.jpg",
    "Lotus": "/plants/lotus.jpg",
    "Curry Leaf": "/plants/curry_leaf.jpg",
    "Cardamom": "/plants/cardamom.jpg",
    "Turmeric": "/plants/turmeric.jpg",
    "Black Pepper": "/plants/black_pepper.jpg",
    "Cinnamon": "/plants/cinnamon.jpg",
    "Clove": "/plants/clove.jpg",
    "Ginger": "/plants/ginger.jpg",
    "Tulsi": "/plants/tulsi.jpg",
    "Neem": "/plants/neem.jpg",
    "Aloe Vera": "/plants/aloe_vera.jpg",
    "Giloy": "/plants/giloy.jpg",
    "Ashwagandha": "/plants/ashwagandha.jpg",
    "Betel Leaf": "/plants/betel_leaf.jpg",
}

alias_map = [
    [["coconut", "nariyal", "thengu"], "Coconut Palm"],
    [["areca", "betel nut palm", "supari", "kamugu"], "Areca Palm"],
    [["palmyra", "borassus", "tadgola", "taad", "nungu", "pana"], "Palmyra Palm"],
    [["bamboo", "baans", "moongil"], "Bamboo"],
    [["banana", "plantain", "kela", "musa", "vazhai"], "Banana"],
    [["rice", "paddy", "dhan", "chawal", "oryza", "nel"], "Rice (Paddy)"],
    [["wheat", "gehun", "kanak", "godhumai", "triticum"], "Wheat"],
    [["sugarcane", "ganna", "karumbu", "saccharum"], "Sugarcane"],
    [["cotton", "kapas", "paruthi", "gossypium"], "Cotton"],
    [["tea", "chai", "theeyilai", "camellia"], "Tea"],
    [["coffee", "kaapi", "coffea"], "Coffee"],
    [["mustard", "sarson", "rai", "kadugu", "brassica"], "Mustard"],
    [["mango", "aam", "mangifera", "maanga"], "Mango"],
    [["guava", "amrood", "psidium", "koyya"], "Guava"],
    [["papaya", "papita", "carica", "pappali"], "Papaya"],
    [["lemon", "lime", "nimbu", "citrus", "elumichai"], "Lemon"],
    [["pomegranate", "anaar", "anar", "punica", "mathulai"], "Pomegranate"],
    [["jackfruit", "kathal", "artocarpus", "chakka", "palaa"], "Jackfruit"],
    [["amla", "gooseberry", "phyllanthus", "amalaki", "nelli"], "Amla"],
    [["tomato", "tamatar", "solanum lycopersicum", "thakkali"], "Tomato"],
    [["brinjal", "eggplant", "baingan", "kathirikai", "vankaya"], "Brinjal"],
    [["chilli", "chili", "mirch", "hari mirch", "capsicum", "milagai"], "Green Chilli"],
    [["coriander", "cilantro", "dhania", "kothamalli", "coriandrum"], "Coriander"],
    [["fenugreek", "methi", "vendhayam", "trigonella"], "Fenugreek"],
    [["moringa", "drumstick", "sahjan", "murungai"], "Drumstick (Moringa)"],
    [["hibiscus", "gudhal", "jaswand", "chembarathi", "sembaruthi"], "Hibiscus"],
    [["jasmine", "mogra", "chameli", "malligai"], "Jasmine"],
    [["rose", "gulab", "rosa", "roja"], "Rose"],
    [["marigold", "genda", "tagetes", "samandhi"], "Marigold"],
    [["plumeria", "champa", "frangipani", "arali"], "Plumeria"],
    [["lotus", "kamal", "nelumbo", "thamarai"], "Lotus"],
    [["curry", "kadi patta", "murraya", "karivepaku", "kariveppila"], "Curry Leaf"],
    [["cardamom", "elaichi", "elettaria", "elakkai"], "Cardamom"],
    [["turmeric", "haldi", "curcuma", "manjal"], "Turmeric"],
    [["black pepper", "pepper", "kali mirch", "kurumilaku"], "Black Pepper"],
    [["cinnamon", "dalchini", "cinnamomum", "karuvapattai"], "Cinnamon"],
    [["clove", "laung", "syzygium", "kirambu", "lavang"], "Clove"],
    [["ginger", "adrak", "zingiber", "inji"], "Ginger"],
    [["tulsi", "holy basil", "ocimum", "thulasi"], "Tulsi"],
    [["neem", "azadirachta", "veppam"], "Neem"],
    [["aloe", "ghritkumari", "kattralai"], "Aloe Vera"],
    [["giloy", "guduchi", "tinospora", "amrita", "seenthil"], "Giloy"],
    [["ashwagandha", "withania", "asgandh", "amukkara"], "Ashwagandha"],
    [["betel", "paan", "piper betle", "vetrilai", "tamalapaku"], "Betel Leaf"],
]

lines = [
    "// High quality, verified real-life photographs of LIVING plants",
    "// Stored locally in frontend/public/plants/ to ensure guaranteed, realistic living plant visuals",
    "export const REAL_PLANT_PHOTOS = " + json.dumps(photo_mapping, indent=2) + ";",
    "",
    "const ALIAS_MAP = " + json.dumps(alias_map, indent=2) + ";",
    "",
    "export function getPlantImage(name = '') {",
    "  const n = (name || '').toLowerCase();",
    "  const match = ALIAS_MAP.find(([keys]) => keys.some((k) => n.includes(k)));",
    "  return match ? REAL_PLANT_PHOTOS[match[1]] : null;",
    "}",
    "",
    "// Complete 44-species dataset of plants grown across India, written in simple everyday English",
    "export const INDIAN_SUBCONTINENT_PLANTS = " + json.dumps(plants, indent=2) + ";",
    "",
]

out_file = Path("/Users/amrutachari/Desktop/floraAI/frontend/src/lib/indianPlants.js")
out_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Successfully generated {out_file} with {len(plants)} plants")
