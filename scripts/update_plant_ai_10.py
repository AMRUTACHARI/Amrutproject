# Script to update backend/plant_ai.py with exactly 10 Indian plant species, Tamil metadata,
# robust non-plant rejection, and accurate problem-plant disease diagnosis.

from pathlib import Path

target_file = Path("/Users/amrutachari/Desktop/floraAI/backend/plant_ai.py")
content = target_file.read_text(encoding="utf-8")

# Define the exact 10 species dataset
NEW_10_PLANTS_CODE = '''# ==============================================================================
# CURATED 10 INDIAN BOTANICAL SPECIES (WITH TAMIL & HINDI TAXONOMY)
# Includes requested Coconut, Bismarck Palm, Lipstick Palm, Paddy/Rice, Mango,
# Aloe Vera, Tulsi, Curry Leaf, Neem, and Snake Plant.
# Written in simple everyday English for growers, farmers, and plant lovers.
# ==============================================================================
EXPANDED_BOTANICAL_KNOWLEDGE = [
    {
        "name": "Coconut Palm (Nariyal / Thennai)",
        "tamil_name": "தென்னை (Thennai)",
        "scientific_name": "Cocos nucifera",
        "family": "Palm Family (Arecaceae)",
        "category": "Palms & Plantation",
        "role": "Revered as 'Kalpavriksha' across India and 'Thennai' in Tamil Nadu. Every single part is cherished: sweet tender coconut water (Elaneer), pure cooking oil, nutritious kernel copra, coir fiber ropes, and strong fronds for eco-friendly thatch roofs.",
        "description": "A magnificent tall palm growing 20 to 30 meters high with a slender ringed trunk and arching feather fronds. Thrives under bright tropical sunshine, coastal sea breezes, and well-draining sandy loam.",
        "common_issues": ["Brown leaf spots (Bipolaris leaf blight)", "Bud rot from stagnant rain", "Rhinoceros beetle holes", "Yellowing fronds from potassium deficiency"],
        "problem_cause": "Damp monsoon humidity allows fungal spores to form brown necrotic leaf spots, while standing rainwater pooling at the central spindle can rot soft young heart leaves.",
        "remedies": [
            "Spray 1% organic Bordeaux mixture or copper oxychloride solution across lower fronds showing leaf spots.",
            "Apply 1 to 2 kg of wood ash or organic potash around the palm basin to strengthen frond cell walls.",
            "Place neem seed cake mixed with coarse river sand inside outer leaf bases to repel boring beetles.",
            "Prune off severely dried, diseased lower fronds and dispose of them far from the grove.",
        ],
        "precautions": [
            "Ensure the ground slopes gently away from the trunk base so rainwater never ponds around roots.",
            "Space palms at least 25 feet apart so every frond receives unobstructed natural sunlight.",
            "Feed palms twice a year with compost, vermicompost, and organic micronutrients before monsoon.",
        ],
    },
    {
        "name": "Bismarck Palm (Silver Fan Palm)",
        "tamil_name": "வெள்ளி விசிறி பனை (Velli Visiri Panai)",
        "scientific_name": "Bismarckia nobilis",
        "family": "Palm Family (Arecaceae)",
        "category": "Landscape & Specimen Palm",
        "role": "The crowning jewel of tropical architectural landscapes and grand gardens across India. Prized for its enormous, shimmering silver-blue fan fronds that create dramatic visual impact in hot sunny courtyards.",
        "description": "A grand solitary palm featuring a stout marble-grey trunk and a symmetrical crown of massive, rigid fan-shaped leaves coated in an intense powdery silver-blue wax.",
        "common_issues": ["Leaf spot fungus from overhead sprinkler splash", "Leaf edge browning from dry winds", "Potassium deficiency speckling"],
        "problem_cause": "Frequent overhead watering leaves wet droplets on the silver fronds, encouraging circular brown fungal spots with yellow halos to develop.",
        "remedies": [
            "Switch to ground drip irrigation and strictly avoid wetting the silver fan leaves with garden sprinklers.",
            "Apply mild copper bio-fungicide if brown circular spots appear on lower silver fronds.",
            "Top-dress soil with slow-release potassium and organic compost to prevent frond edge scorch.",
        ],
        "precautions": [
            "Plant in wide open spaces with full glaring sunlight to let the 10-foot-wide silver canopy expand.",
            "Provides exceptional heat and drought tolerance once established in well-drained soil.",
            "Never disturb the sensitive root ball during transplanting.",
        ],
    },
    {
        "name": "Lipstick Palm (Sealing Wax Palm)",
        "tamil_name": "சிவப்பு பனை (Sivappu Panai)",
        "scientific_name": "Cyrtostachys renda",
        "family": "Palm Family (Arecaceae)",
        "category": "Palms & Plantation",
        "role": "One of the world's most breathtaking ornamental palms, famous for its brilliant scarlet-red to crimson crownshafts and stems. Grown in luxury gardens, botanical collections, and humid coastal verandas as a living tropical sculpture.",
        "description": "A graceful clustering feather palm with glossy emerald-green fronds and unmistakable, intensely vivid lacquer-red crownshafts and petioles. Demands warm tropical temperatures and generous humidity.",
        "common_issues": ["Brown leaf tips from low humidity", "Loss of red color from underwatering", "Spider mites in dry indoor air"],
        "problem_cause": "Dry air or underwatering causes leaf tips to turn crisp and brown, while lack of moisture fades the vivid crimson red coloration of the stems.",
        "remedies": [
            "Mist fronds daily with soft water and place the container over a wide pebble water humidity tray.",
            "Keep potting soil consistently moist; never let the root zone dry out completely.",
            "Spray mild neem oil or insecticidal soap on frond undersides if spider mites appear.",
        ],
        "precautions": [
            "Requires warm temperatures above 18°C; shield from cold AC drafts and dry winter winds.",
            "Provide bright dappled sunlight or gentle morning sun rather than harsh scorching noon heat.",
            "Feed monthly during monsoon and spring with diluted organic seaweed extract.",
        ],
    },
    {
        "name": "Rice / Paddy (Dhan / Nel)",
        "tamil_name": "நெல் (Nel)",
        "scientific_name": "Oryza sativa",
        "family": "Grass Family (Poaceae)",
        "category": "Staple Crop",
        "role": "The foundational staple food of over a billion people in India and the soul of Tamil culture (celebrated during Pongal). Provides white rice, brown rice, nourishing rice bran oil, and straw for cattle and eco-thatching.",
        "description": "An annual wetland grass growing 1 to 1.5 meters tall with slender hollow culms, flat ribbon-like leaves, and arching panicles laden with golden grain spikelets. Cultivated in flooded alluvial paddies.",
        "common_issues": ["Paddy blast fungal lesions", "Bacterial leaf blight", "Stem borer caterpillars", "Brown planthopper"],
        "problem_cause": "Excessive chemical nitrogen fertilizer combined with humid overcast monsoon weather encourages spindle-shaped blast lesions and yellowing leaf blight.",
        "remedies": [
            "Spray bio-fungicide (Pseudomonas fluorescens 10g/L) or neem seed kernel extract (NSKE 5%) across crop canopy.",
            "Maintain balanced fertilization: incorporate organic vermicompost and reduce excess synthetic nitrogen.",
            "Drain standing paddy water for 24-48 hours to aerate soil and break pest reproduction cycles.",
        ],
        "precautions": [
            "Treat seeds with Trichoderma viride or cow urine slurry before nursery sowing.",
            "Maintain optimal floodwater depth (2 to 5 cm) during tillering; avoid water stagnation during ripening.",
            "Leave field bunds clean of wild weeds that harbor planthoppers.",
        ],
    },
    {
        "name": "Mango Tree (Aam / Maamaram)",
        "tamil_name": "மாமரம் (Maamaram)",
        "scientific_name": "Mangifera indica",
        "family": "Cashew Family (Anacardiaceae)",
        "category": "Fruit Tree",
        "role": "The King of Fruits and National Fruit of India. Produces heavenly sweet varieties like Alphonso, Banganapalli, Kesar, and Neelam. Mango leaves (Maavilai) are tied at home entrances as auspicious blessings of prosperity.",
        "description": "A magnificent, long-lived evergreen canopy tree reaching 15 to 30 meters with dense dark-green leathery leaves, copper-red new flush foliage, and fragrant flower panicles yielding golden succulent stone fruits.",
        "common_issues": ["Anthracnose leaf blight", "Powdery mildew on blossom sprays", "Mango hopper bugs", "Fruit fly maggots"],
        "problem_cause": "Cloudy unseasonal rains during flowering spread powdery mold onto blossom panicles, while fungal spores cause dark necrotic spots on wet young leaves.",
        "remedies": [
            "Spray 3g/L copper oxychloride or 5% neem extract to suppress leaf blight and anthracnose lesions.",
            "Dust organic sulfur powder or spray wettable sulfur on flower panicles if whitish powdery mildew appears.",
            "Hang pheromone traps in the orchard canopy to monitor and catch fruit flies naturally.",
        ],
        "precautions": [
            "Prune crowded interior dead branches after harvest to let sunlight penetrate the inner canopy.",
            "Collect and compost fallen diseased leaves and rotten fruit to stop spore over-wintering.",
            "Withhold irrigation 2 months prior to flowering to stimulate abundant blossom formation.",
        ],
    },
    {
        "name": "Aloe Vera (Ghritkumari / Katralai)",
        "tamil_name": "சோற்றுக்கற்றாழை (Sothu Katralai)",
        "scientific_name": "Aloe barbadensis",
        "family": "Asphodelaceae",
        "category": "Medicinal & Succulent",
        "role": "Renowned across Ayurvedic and Siddha medicine as 'Sothu Katralai' or 'Ghritkumari'. Its soothing inner gel heals burns, moisturizes skin, promotes glossy hair, and aids digestive wellness.",
        "description": "A stemless clustering succulent with thick, fleshy grey-green upright leaves armed with soft white serrated teeth. Leaves contain rich clear gel that stores moisture for months.",
        "common_issues": ["Soft root rot from overwatering", "Fungal leaf spot", "Sunburn reddening", "Mealybugs at leaf rosette bases"],
        "problem_cause": "Frequent watering in soggy, poorly draining clay suffocates fleshy roots, causing leaf bases to turn translucent, mushy, and foul-smelling.",
        "remedies": [
            "Immediately stop watering and allow potting soil to completely dry out for 10 to 14 days.",
            "Prune off mushy, rotted outer leaves using a clean blade and dust cut surfaces with natural turmeric powder.",
            "Repot into a gritty cactus mix containing 50% coarse sand, perlite, and red soil.",
        ],
        "precautions": [
            "Water only when the top 2 inches of soil are bone dry; once every 2-3 weeks in winter.",
            "Ensure the container has large unobstructed bottom drainage holes.",
            "Provide 4 to 6 hours of bright indirect sunlight daily; avoid harsh scorching noon glare.",
        ],
    },
    {
        "name": "Tulsi (Holy Basil / Thulasi)",
        "tamil_name": "துளசி (Thulasi)",
        "scientific_name": "Ocimum sanctum",
        "family": "Mint Family (Lamiaceae)",
        "category": "Sacred & Medicinal",
        "role": "Venerated as the Sacred Goddess in Indian households and planted in courtyards (Thulasi Madam). Its highly aromatic medicinal leaves strengthen immunity, relieve coughs and colds, and purify ambient air.",
        "description": "A fragrant, bushy branching shrub growing 30 to 75 cm tall with soft hairy green or purple-tinted leaves, square purple stems, and delicate upright spikes of tiny purple flowers.",
        "common_issues": ["Leaf spot fungus from damp leaves", "Root rot from waterlogged soil", "Lace bugs and whiteflies", "Premature flower spike exhaustion"],
        "problem_cause": "Sprinkling water on leaves during damp evenings causes fungal brown speckles, while letting flower seeds mature drains energy from fresh leaf production.",
        "remedies": [
            "Pinch off dry seed heads (Manjari) regularly to stimulate dense, bushy new leafy growth.",
            "Water directly at the base of the soil in the morning; keep the fragrant foliage dry.",
            "Spray mild sour buttermilk spray (diluted 1:10) or neem seed oil to control fungal spots and small insects.",
        ],
        "precautions": [
            "Plant in porous terracotta pots with fast drainage so roots never sit in soggy wet soil.",
            "Place in a sacred, airy spot receiving at least 4 to 6 hours of morning sunlight.",
            "Feed monthly with a handful of organic vermicompost and neem cake powder.",
        ],
    },
    {
        "name": "Curry Leaf (Kadi Patta / Kariveppilai)",
        "tamil_name": "கறிவேப்பிலை (Kariveppilai)",
        "scientific_name": "Murraya koenigii",
        "family": "Citrus Family (Rutaceae)",
        "category": "Kitchen Spice & Herb",
        "role": "The quintessential aromatic tempering herb of Indian and South Indian cuisine (Kariveppilai / Kadi Patta). Rich in iron, antioxidants, and essential oils that nourish hair vitality and aid digestive health.",
        "description": "A small aromatic evergreen shrub or tree growing 2 to 4 meters tall with pinnate fronds bearing 11 to 21 intensely fragrant, glossy dark-green pointed leaflets.",
        "common_issues": ["Curry leaf psyllids causing leaf curl", "Black sooty mold", "Leaf spot mold", "Iron deficiency yellowing"],
        "problem_cause": "Tiny sap-sucking psyllid bugs excrete sticky honeydew on young leaf tips, causing black sooty powder to cover leaves and block sunlight.",
        "remedies": [
            "Spray 5 ml cold-pressed neem oil mixed with 2 ml mild shampoo in 1 liter of water thoroughly under leaves.",
            "Prune back distorted, curled shoot tips to encourage a fresh flush of healthy fragrant foliage.",
            "Apply a weekly spray of diluted sour buttermilk or wood ash around the soil basin to cure yellowing.",
        ],
        "precautions": [
            "Thrives in warm, sunny locations with at least 5 to 6 hours of direct sunlight.",
            "Water regularly during hot months, but allow topsoil to dry between waterings.",
            "Feed quarterly with seasoned cow manure or vermicompost for lush dark-green leaflets.",
        ],
    },
    {
        "name": "Neem Tree (Veppamaram)",
        "tamil_name": "வேப்பமரம் (Veppamaram)",
        "scientific_name": "Azadirachta indica",
        "family": "Mahogany Family (Meliaceae)",
        "category": "Traditional Medicine",
        "role": "Celebrated as the 'Village Pharmacy' and 'Veppamaram' in Tamil Nadu. Every component—leaves, twigs, seeds, and bark—provides natural antimicrobial, antiviral, and organic pest-repelling solutions.",
        "description": "A hardy, fast-growing evergreen tree growing 15 to 20 meters tall with a broad rounded canopy of dark-green serrated feather leaves and fragrant white starry blossoms.",
        "common_issues": ["Tea mosquito bug shoot blight", "Fungal leaf spot in cloudy monsoon", "Root grubs in young saplings"],
        "problem_cause": "Mirid bugs pierce young shoot flushes and suck sap, leaving brown necrotic drying tips during humid weather breaks.",
        "remedies": [
            "Neem naturally produces its own potent defensive azadirachtin; healthy mature trees heal on their own.",
            "For young saplings, spray mild copper oxychloride if extensive leaf spot lesions occur during heavy monsoon.",
            "Loosen soil around tree base and add compost mixed with Trichoderma.",
        ],
        "precautions": [
            "Extremely drought hardy and adaptable to poor dry soils once deep taproot establishes.",
            "Requires full direct sunshine all day long; avoid planting in shaded or swampy areas.",
            "Prune lower branches during dry season to develop a clean, sturdy main trunk.",
        ],
    },
    {
        "name": "Snake Plant (Mother-in-Law's Tongue / Marul)",
        "tamil_name": "மரூள் / பாம்பு கற்றாழை (Marul)",
        "scientific_name": "Dracaena trifasciata",
        "family": "Asparagaceae",
        "category": "Indoor & Air Purifier",
        "role": "One of NASA's premier air-purifying houseplants, converting CO2 into clean oxygen at night. Loved in Indian apartments for its indestructible hardiness, architectural elegance, and low-maintenance grace.",
        "description": "An upright evergreen perennial with stiff, sword-like succulent leaves growing vertically 60 to 120 cm tall. Leaves feature deep green horizontal banding with luminous golden-yellow margins.",
        "common_issues": ["Rhizome soft rot from overwatering", "Wrinkled leaves from dehydration", "Fungal leaf spot from water in rosette"],
        "problem_cause": "Pouring water into the central leaf rosette or watering too frequently causes underground rhizomes to rot, turning leaves mushy, yellow, and floppy.",
        "remedies": [
            "Immediately stop watering and move plant to a well-ventilated, bright spot.",
            "Remove rotted mushy leaves at the rhizome base using sterilized scissors.",
            "Repot into coarse, free-draining succulent potting mix containing perlite and sand.",
        ],
        "precautions": [
            "Water sparingly: once every 2 to 3 weeks in summer, once a month in winter.",
            "Thrives in everything from low indirect light to bright sun; never let water sit in the saucer.",
            "Wipe glossy leaf blades with a soft dry cloth occasionally to remove dust.",
        ],
    },
]
'''

# Find start of EXPANDED_BOTANICAL_KNOWLEDGE and replace until SPICE_KNOWLEDGE
start_idx = content.find("EXPANDED_BOTANICAL_KNOWLEDGE = [")
end_idx = content.find("SPICE_KNOWLEDGE = EXPANDED_BOTANICAL_KNOWLEDGE")

if start_idx == -1 or end_idx == -1:
    print(f"Error: could not locate markers: start={start_idx}, end={end_idx}")
    exit(1)

content = content[:start_idx] + NEW_10_PLANTS_CODE + "\n" + content[end_idx:]

target_file.write_text(content, encoding="utf-8")
print(f"Successfully replaced EXPANDED_BOTANICAL_KNOWLEDGE with 10 curated species in {target_file}")
