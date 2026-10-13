// Curated verified photographs and botanical datasets for Indian subcontinent species
export const REAL_PLANT_PHOTOS = {
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
  "Money Plant": "/plants/money_plant.jpg",
  "Bougainvillea": "/plants/bougainvillea.jpg",
  "Lipstick Palm": "/plants/lipstick_palm.jpg",
};

const ALIAS_MAP = [
  [["lipstick palm", "lipstick", "sealing wax palm", "cyrtostachys", "lipstick bomb", "lipstick bomb tree", "lipstick tree", "red palm"], "Lipstick Palm"],
  [["date palm", "khajoor", "khajur", "pind khajoor"], "Coconut Palm"],
  [["wild date palm", "silver date palm", "khajuri", "nolen gur", "sendhi"], "Palmyra Palm"],
  [["fish tail palm", "fishtail palm", "kitul", "mari palm"], "Areca Palm"],
  [["golden cane palm", "yellow palm", "butterfly palm", "dypsis"], "Areca Palm"],
  [["royal palm", "cuban royal palm", "raj taad", "roystonea"], "Palmyra Palm"],
  [["foxtail palm", "wodyetia"], "Areca Palm"],
  [["bottle palm", "champagne palm", "hyophorbe"], "Coconut Palm"],
  [["bismarck palm", "bismarckia", "silver fan palm"], "Palmyra Palm"],
  [["coconut", "nariyal", "thengu"], "Coconut Palm"],
  [["areca", "supari", "betel nut palm"], "Areca Palm"],
  [["palmyra", "tadgola", "taad", "nungu"], "Palmyra Palm"],
  [["bamboo", "baans"], "Bamboo"],
  [["banana", "kela", "plantain"], "Banana"],
  [["rice", "paddy", "dhan"], "Rice (Paddy)"],
  [["wheat", "gehun", "kanak"], "Wheat"],
  [["sugarcane", "ganna"], "Sugarcane"],
  [["cotton", "kapas"], "Cotton"],
  [["tea", "chai"], "Tea"],
  [["coffee", "kaapi"], "Coffee"],
  [["mustard", "sarson", "rai"], "Mustard"],
  [["mango", "aam", "alphonso", "kesar"], "Mango"],
  [["guava", "amrood", "koyya"], "Guava"],
  [["papaya", "papita"], "Papaya"],
  [["lemon", "lime", "nimbu"], "Lemon"],
  [["pomegranate", "anar", "anaar"], "Pomegranate"],
  [["jackfruit", "kathal", "chakka"], "Jackfruit"],
  [["amla", "gooseberry", "amalaki"], "Amla"],
  [["tomato", "tamatar"], "Tomato"],
  [["brinjal", "eggplant", "baingan"], "Brinjal"],
  [["chilli", "chili", "mirch"], "Green Chilli"],
  [["coriander", "cilantro", "dhania"], "Coriander"],
  [["fenugreek", "methi"], "Fenugreek"],
  [["moringa", "drumstick", "sahjan"], "Drumstick (Moringa)"],
  [["hibiscus", "gudhal", "jaswand"], "Hibiscus"],
  [["jasmine", "mogra", "chameli"], "Jasmine"],
  [["rose", "gulab"], "Rose"],
  [["marigold", "genda"], "Marigold"],
  [["plumeria", "champa", "frangipani"], "Plumeria"],
  [["lotus", "kamal"], "Lotus"],
  [["curry leaf", "kadi patta", "karivepaku"], "Curry Leaf"],
  [["cardamom", "elaichi"], "Cardamom"],
  [["turmeric", "haldi"], "Turmeric"],
  [["pepper", "kali mirch"], "Black Pepper"],
  [["cinnamon", "dalchini"], "Cinnamon"],
  [["clove", "laung", "lavang"], "Clove"],
  [["ginger", "adrak"], "Ginger"],
  [["tulsi", "holy basil"], "Tulsi"],
  [["neem"], "Neem"],
  [["aloe vera", "ghritkumari", "aloe"], "Aloe Vera"],
  [["giloy", "guduchi"], "Giloy"],
  [["ashwagandha"], "Ashwagandha"],
  [["betel", "paan"], "Betel Leaf"],
  [["money plant", "pothos"], "Money Plant"],
  [["bougainvillea", "kagaz phool"], "Bougainvillea"],
];

export function getPlantImage(name = "") {
  if (!name) return null;
  const n = name.toLowerCase();
  const match = ALIAS_MAP.find(([keys]) => keys.some((k) => n.includes(k)));
  return match ? REAL_PLANT_PHOTOS[match[1]] : REAL_PLANT_PHOTOS[name] || null;
}

// Curated Top 12 Signature Plants for the Homepage Showcase Gallery
export const SIGNATURE_GALLERY_PLANTS = [
  {
    name: "Curry Leaf (Kadi Patta)",
    scientific_name: "Murraya koenigii",
    family: "Citrus Family (Rutaceae)",
    category: "Spices & Kitchen",
    role: "The soul of South Indian and West Indian seasoning. Fresh leaves release an invigorating aroma in hot oil tempering (tadka) and are rich in natural iron, antioxidants, and digestive essential oils.",
    description: "A small, bushy tropical tree with glossy, dark-green aromatic leaflets growing in pairs. Flourishes in warm sunny courtyards, terraces, and garden borders.",
    common_issues: ["Tiny sap bugs (Psyllids)", "Leaf curling and sticky residue", "Black sooty coating on leaves", "Iron yellowing"],
    problem_cause: "Tiny sap-sucking psyllid insects colonize tender shoot tips and excrete sticky sap that attracts black mold during warm humid spells.",
    remedies: [
      "Spray 5 ml organic cold-pressed neem oil mixed with 2 drops mild soap in 1 liter water in late evening.",
      "Prune heavily curled stem tips so vigorous, pest-free fresh fragrant leaves sprout quickly.",
      "Add 2 cups sour buttermilk diluted in water around roots once a month to boost chlorophyll."
    ],
    precautions: [
      "Place where it receives at least 5 to 6 hours of warm sunlight daily.",
      "Allow surface soil to dry slightly before watering; avoid waterlogged roots.",
      "Feed twice a year with well-composted cow manure and wood ash."
    ]
  },
  {
    name: "Tulsi (Holy Basil)",
    scientific_name: "Ocimum sanctum",
    family: "Mint Family (Lamiaceae)",
    category: "Medicinal & Herbs",
    role: "Venerated across India as the sacred Queen of Herbs. Planted in courtyard Tulsi Vrindavans, boiled in daily healing kadha tea, and revered for boosting immunity and relieving seasonal respiratory ailments.",
    description: "An aromatic, erect perennial sub-shrub with softly hairy green or purple-tinged toothed leaves and spikes of fragrant purple-pink blossoms.",
    common_issues: ["Leaf browning from winter chill", "Powdery white leaf mold", "Aphid and mite webbing", "Stem rot from overwatering"],
    problem_cause: "Excessive daily religious watering into pots without adequate drainage causes root suffocation, while cool winter nights stress tropical leaves.",
    remedies: [
      "Ensure pots have clear drainage holes; water moderately only when topsoil feels dry.",
      "Pinch off spent flower spikes (manjari) regularly to keep the plant bushy and prevent seeding dieback.",
      "Dust fresh wood ash or spray light neem water to protect leaves from tiny garden bugs."
    ],
    precautions: [
      "Keep in bright open morning sun with gentle breezes.",
      "Shelter from cold winter drafts and heavy non-stop monsoon downpours.",
      "Add vermicompost and a handful of neem cake around roots every two months."
    ]
  },
  {
    name: "Neem (Margosa Tree)",
    scientific_name: "Azadirachta indica",
    family: "Mahogany Family (Meliaceae)",
    category: "Trees & Palms",
    role: "Revered across India as the 'Village Pharmacy' (Natures Drugstore). Its bitter leaves, twigs, bark, and seed oil possess legendary antibacterial, antifungal, and insecticidal properties.",
    description: "A large, hardy evergreen shade tree with deeply furrowed grey bark, dense rounded crown, and serrated curved emerald-green compound leaves.",
    common_issues: ["Tea mosquito bug punctures", "Leaf webber caterpillars", "Mildew during heavy rains", "Root waterlogging when young"],
    problem_cause: "Extreme waterlogging during heavy cyclonic rain can stunt sapling roots, while young flush leaves occasionally attract leaf-feeding caterpillars.",
    remedies: [
      "Prune affected twig tips showing caterpillar webs and allow fresh breeze through the canopy.",
      "Dig a gentle trench around the tree base to guide stagnant rainwater away from the trunk.",
      "Spray organic bio-pesticide extract on young saplings if leaf spots appear."
    ],
    precautions: [
      "Plant in open sunny fields or wide courtyard corners with ample root space.",
      "Needs very little water once established; naturally drought-hardy.",
      "Avoid wounding the bark when clearing weeds."
    ]
  },
  {
    name: "Mango Tree (Aam)",
    scientific_name: "Mangifera indica",
    family: "Cashew Family (Anacardiaceae)",
    category: "Fruits & Orchards",
    role: "The National Fruit of India, celebrated for iconic varieties like Alphonso, Kesar, and Dasheri. Mango leaves are tied in auspicious torans for Indian doorways, while fruit is enjoyed ripe or as raw pickles (aam panna).",
    description: "A magnificent, long-lived tropical evergreen tree with a dense canopy, glossy dark-green lanceolate leaves with pink-copper new flush, and fragrant panicles of creamy flowers.",
    common_issues: ["Anthracnose leaf spot", "Powdery white blossom mildew", "Mango hopper bugs", "Stem borer beetle"],
    problem_cause: "High humidity and cloudy weather during flowering foster powdery mold that causes blossom drop, while hoppers suck sap from tender panicles.",
    remedies: [
      "Spray copper oxychloride (3g/liter) or organic neem extract on foliage before flower buds open.",
      "Prune overcrowded inner branches after fruit harvest to let sunshine illuminate the canopy center.",
      "Tie sticky bug bands around the main trunk to prevent mealybugs from climbing up."
    ],
    precautions: [
      "Withhold excessive irrigation during winter to stimulate prolific spring flowering.",
      "Remove fallen leaves and rotten fruit from under the canopy to break fungal cycles.",
      "Feed with composted manure and wood ash around the drip-line once every monsoon."
    ]
  },
  {
    name: "Coconut Palm (Nariyal)",
    scientific_name: "Cocos nucifera",
    family: "Palm Family (Arecaceae)",
    category: "Trees & Palms",
    role: "Cherished as 'Kalpavriksha' (the wish-fulfilling tree) along coastal India. Yields sweet coconut water, nutrient-rich flesh, cold-pressed oil, coir ropes, and durable thatch for eco-friendly roofs.",
    description: "A graceful, tall tropical palm reaching 20 to 30 meters with a ringed slender trunk and arching feather-like pinnate green fronds swaying in the coastal breeze.",
    common_issues: ["Brown oval leaf spots", "Crown rot from heavy rains", "Rhinoceros beetle holes in fronds", "Red palm weevil"],
    problem_cause: "Heavy monsoon dampness allows fungal molds into soft center crowns, while nocturnal beetles burrow into developing spear leaves.",
    remedies: [
      "Clean center crown fibers and place a mixture of neem cake powder and coarse sand in top leaf axils.",
      "Spray 1% organic Bordeaux mixture or copper solution over developing fronds to stop fungal spotting.",
      "Drench root basin with beneficial Trichoderma bio-compost tea to boost trunk vigor."
    ],
    precautions: [
      "Plant palms at least 25 feet apart so each receives full tropical sunshine.",
      "Ensure free-flowing drainage; never allow stagnant water to pool around the trunk base.",
      "Feed annually with organic compost and potash (wood ash) to strengthen tough fronds."
    ]
  },
  {
    name: "Hibiscus (Gudhal / Jaswand)",
    scientific_name: "Hibiscus rosa-sinensis",
    family: "Mallow Family (Malvaceae)",
    category: "Garden & Flowers",
    role: "Devotional sacred flower offered to Lord Ganesha and Goddess Kali. Fresh petals are brewed into antioxidant herbal tea and pressed into traditional hair-nourishing Ayurvedic oils.",
    description: "A bushy, perennial flowering shrub with glossy serrated dark-green leaves and stunning, large trumpet-shaped five-petaled blooms in vibrant red, pink, and yellow.",
    common_issues: ["White cottony mealybugs", "Bud drop before opening", "Yellowing lower foliage", "Aphids on flower stems"],
    problem_cause: "White cottony bugs cluster in leaf axils and sap energy from tender flower buds, causing premature yellowing and bud abortion.",
    remedies: [
      "Dab white bug clusters with a cotton swab dipped in rubbing alcohol, or spray with soapy neem emulsion.",
      "Wash foliage with a firm water jet to knock off aphid colonies.",
      "Move container to receive a minimum of 5 to 6 hours of direct daily sunlight."
    ],
    precautions: [
      "Water regularly when topsoil dries; avoid leaving pot sitting in standing drainage water.",
      "Prune branch tips in early spring to encourage dense new shoots and abundant flower buds.",
      "Feed monthly with banana peel compost or fermented mustard cake liquid for vibrant blooms."
    ]
  },
  {
    name: "Lemon (Kagzi Nimbu)",
    scientific_name: "Citrus aurantiifolia",
    family: "Citrus Family (Rutaceae)",
    category: "Fruits & Orchards",
    role: "Indispensable staple fruit in Indian hospitality and cuisine. Squeezed fresh into refreshing nimbu pani, curries, and tangy homemade pickles (nimbu ka achaar); rich in natural vitamin C.",
    description: "A compact, spiny evergreen citrus shrub with aromatic oval leaves, fragrant white blossoms, and clusters of smooth, round thin-skinned juicy yellow fruits.",
    common_issues: ["Citrus canker corky brown spots", "Leaf miner winding trails", "Iron yellowing with green veins", "Caterpillars (lemon butterfly)"],
    problem_cause: "Bacterial splash during windy monsoon showers produces corky brown lesions, while citrus leaf miner larvae chew translucent silver tunnels inside new leaves.",
    remedies: [
      "Spray 1% copper oxychloride or Streptocycline bio-spray on foliage during wet weather.",
      "Spray neem oil (5 ml/liter) on tender new flush leaves to deter egg-laying leaf miners.",
      "Apply micronutrient spray containing iron and zinc to cure pale yellow leaves."
    ],
    precautions: [
      "Plant in well-drained sandy loam soil in full sun.",
      "Prune dead spiny twigs and water shoots to keep the canopy open to light.",
      "Water moderately; avoid excess moisture during fruit ripening to prevent skin cracking."
    ]
  },
  {
    name: "Aloe Vera (Ghritkumari)",
    scientific_name: "Aloe barbadensis",
    family: "Asphodel Family (Asphodelaceae)",
    category: "Medicinal & Herbs",
    role: "Cherished soothing succulent found on Indian balconies. Its cooling inner gel is applied topically to calm burns, nourish skin and hair, and taken internally for digestive vitality.",
    description: "A stemless, clump-forming succulent with thick, fleshy lance-shaped leaves with spiny margins that store clear, hydrating herbal gel. Extremely hardy and drought-tolerant.",
    common_issues: ["Soggy brown rotting base", "Brown sunburn spots", "Pale wrinkled limp leaves", "Mealybugs at leaf base"],
    problem_cause: "Overwatering and poorly draining pots cause root rot and make succulent leaves turn mushy brown and collapse.",
    remedies: [
      "Stop watering immediately; allow soil to dry completely for 10-14 days.",
      "Repot in coarse succulent mix with coarse sand, perlite, and red soil.",
      "Trim away mushy rotting leaves with clean scissors and dust cuts with organic cinnamon powder."
    ],
    precautions: [
      "Water sparingly; wait until the entire potting soil dries before watering again.",
      "Provide bright indirect or filtered sunlight; protect from scorching summer afternoon heat.",
      "Always use pots with functional drainage holes."
    ]
  },
  {
    name: "Jasmine (Mogra / Chameli)",
    scientific_name: "Jasminum sambac",
    family: "Olive Family (Oleaceae)",
    category: "Garden & Flowers",
    role: "India's beloved night-fragrant blossom. Woven into traditional hair gajras for festive celebrations, used in spiritual pujas, and distilled into exquisite natural attar perfume.",
    description: "A bushy climbing shrub with glossy dark-green ovate leaves and prolific clusters of heavenly scented star-shaped white blossoms that bloom primarily in summer and monsoon.",
    common_issues: ["Budworm boring into flower buds", "Fungal leaf spot blotches", "Red spider mites", "Yellowing leaves"],
    problem_cause: "Tiny caterpillars bore tiny holes into flower buds before they open, turning petals brown and ruining fragrance, while mites thrive in dry hot weather.",
    remedies: [
      "Hand-pick and discard infested purple-brown flower buds early in the morning.",
      "Spray neem oil (3 ml/liter) once a week during peak budding season.",
      "Prune mature stems after the monsoon flowering season to trigger fresh blooming flushes."
    ],
    precautions: [
      "Requires full direct sunlight (at least 6 hours daily) for profuse flower production.",
      "Keep soil evenly moist but never swampy.",
      "Feed monthly during active spring and summer with organic bone meal or vermicompost."
    ]
  },
  {
    name: "Turmeric (Haldi)",
    scientific_name: "Curcuma longa",
    family: "Ginger Family (Zingiberaceae)",
    category: "Spices & Kitchen",
    role: "The Golden Herb of India. Celebrated for thousands of years in Indian cooking, wedding ceremonies (Haldi rasam), and Ayurvedic healing as a potent anti-inflammatory and antiseptic.",
    description: "A lush, leafy perennial herb with broad, magnificent emerald-green leaves rising 1 meter high from aromatic, bright golden-orange underground rhizomes.",
    common_issues: ["Rhizome rot in waterlogged soil", "Leaf spot brown blotches", "Shoot borer caterpillar", "Leaf drying at margins"],
    problem_cause: "Heavy stagnant rainwater in poorly drained beds allows soil fungi to rot underground medicinal rhizomes, causing foliage to wilt and turn brown.",
    remedies: [
      "Drench soil with organic Trichoderma bio-agent to protect golden underground rhizomes.",
      "Spray mild copper solution or baking soda water on leaf spots.",
      "Ensure raised garden beds or ridge planting so excess monsoon water runs off freely."
    ],
    precautions: [
      "Plant in rich, loose organic soil with plenty of well-rotted compost.",
      "Mulch beds heavily with dry leaves to maintain cool, moist soil for underground rhizomes.",
      "Harvest rhizomes after 8 to 9 months when large leaves naturally turn yellow and dry."
    ]
  },
  {
    name: "Black Pepper (Kali Mirch)",
    scientific_name: "Piper nigrum",
    family: "Pepper Family (Piperaceae)",
    category: "Spices & Kitchen",
    role: "Known as the 'King of Spices' and 'Black Gold' of the Western Ghats (Kerala & Karnataka). Essential spice in Indian gastronomy and Ayurvedic formulations (Trikatu) for digestion and warmth.",
    description: "A perennial woody evergreen climbing vine with glossy leathery heart-shaped leaves and long hanging spikes of small round berries that turn from green to fiery red when ripe.",
    common_issues: ["Quick wilt (Phytophthora foot rot)", "Slow wilt disease", "Pollu beetle berry hollows", "Yellowing leaves"],
    problem_cause: "Prolonged monsoon dampness and waterlogging around root collars allow water mold to rapidly rot underground roots and trail bases.",
    remedies: [
      "Drench the base of vines with 1% Bordeaux mixture or copper oxychloride before the heavy southwest monsoon.",
      "Apply bio-control Trichoderma enriched in farmyard manure around vine bases twice a year.",
      "Prune lower foliage touching wet soil to eliminate splash infection."
    ],
    precautions: [
      "Train vines on living shade trees like Silver Oak or Areca Palm in partial dappled sunlight.",
      "Ensure sloping terrain or deep drainage channels to prevent water from standing near roots.",
      "Harvest green spikes when berries begin turning orange-red and sun-dry into black peppercorns."
    ]
  },
  {
    name: "Guava (Amrood)",
    scientific_name: "Psidium guajava",
    family: "Myrtle Family (Myrtaceae)",
    category: "Fruits & Orchards",
    role: "Popular tropical orchard fruit enjoyed across Indian households sprinkled with chaat masala. Rich in vitamin C and dietary fiber; tender leaves are chewed for dental and gum health.",
    description: "A tough, small tropical fruit tree with attractive smooth mottled peeling bark, opposite dull-green veined leaves, white fragrant flowers, and aromatic round edible fruits.",
    common_issues: ["Guava wilt (Fusarium)", "Fruit fly maggots inside fruit", "Stylar end rot", "Mealybugs on shoots"],
    problem_cause: "Soil-borne wilt fungus attacks roots in alkaline or waterlogged soils, while fruit flies lay eggs under young fruit skin as ripening begins.",
    remedies: [
      "Hang organic methyl eugenol pheromone traps in the tree canopy to trap fruit flies safely.",
      "Bag developing young fruits with breathable paper or cloth covers 3 weeks before ripening.",
      "Drench the root basin with Trichoderma-enriched compost to defend roots against wilt fungus."
    ],
    precautions: [
      "Prune canopy branches annually after the winter harvest to let sun and air penetrate.",
      "Avoid wounding root systems during weed hoeing.",
      "Water deeply during fruit swelling and reduce watering before harvest to enhance sweetness."
    ]
  }
];

// Alias for backwards compatibility
export const INDIAN_SUONTINENT_PLANTS = SIGNATURE_GALLERY_PLANTS;
export const INDIAN_SUBCONTINENT_PLANTS = SIGNATURE_GALLERY_PLANTS;
