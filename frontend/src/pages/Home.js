import React, { useState, useEffect } from "react";
import { Link, useNavigate, useLocation } from "react-router-dom";
import { Shell } from "@/components/Navbar";
import { useAuth } from "@/context/AuthContext";
import { ScanResult } from "@/components/ScanResult";
import api, { apiError } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import {
  Sprout,
  ScanLine,
  Leaf,
  Sparkles,
  ArrowRight,
  Compass,
  CheckCircle2,
  AlertTriangle,
  Camera,
  LineChart,
  Activity,
  UploadCloud,
  Loader2,
  X,
} from "lucide-react";
import {
  REAL_PLANT_PHOTOS,
  getPlantImage,
  SIGNATURE_GALLERY_PLANTS,
} from "@/lib/indianPlants";

export { REAL_PLANT_PHOTOS, getPlantImage };

const INTERACTIVE_SPECIMENS = [
  {
    id: "curry-leaf",
    name: "Curry Leaf Plant",
    scientific: "Murraya koenigii (Kadi Patta)",
    part: "Leaves & Shoot Tips",
    status: "Pest Infestation",
    healthScore: 54,
    confidence: 94,
    sampleImage: REAL_PLANT_PHOTOS["Curry Leaf"],
    diagnosis: "Tiny sap-sucking bugs found on leaf tips, causing leaf curling and sticky dark spots.",
    issues: ["Tiny Leaf Bugs", "Curling Leaf Tips", "Black Powder on Leaves"],
    remedies: [
      "Spray 1 tsp organic neem oil mixed with mild liquid soap and water in the evening.",
      "Gently rinse off insect colonies with a garden spray of clean water.",
      "Prune back heavily damaged curled shoots so fresh fragrant leaves emerge.",
    ],
  },
  {
    id: "coconut",
    name: "Coconut Palm",
    scientific: "Cocos nucifera (Nariyal)",
    part: "Crown Fronds & Spindle",
    status: "Leaf Spot",
    healthScore: 68,
    confidence: 92,
    sampleImage: REAL_PLANT_PHOTOS["Coconut Palm"],
    diagnosis: "Brown oval spots observed on outer fronds caused by monsoon dampness. The center spear leaf remains firm and healthy.",
    issues: ["Brown Leaf Spots", "Moisture Stress", "Nutrient Wear"],
    remedies: [
      "Spray 1% organic Bordeaux mixture or copper solution over affected lower leaves.",
      "Add 1 kg organic wood ash or potash around the palm basin to strengthen frond cell walls.",
      "Ensure rainwater drains away freely from the base of the trunk.",
    ],
  },
  {
    id: "mango",
    name: "Mango Tree",
    scientific: "Mangifera indica (Aam - Alphonso)",
    part: "Young Leaves & Twigs",
    status: "Blight",
    healthScore: 62,
    confidence: 95,
    sampleImage: REAL_PLANT_PHOTOS["Mango"],
    diagnosis: "Dark irregular spots on leaf tips caused by fungal spores during cloudy, humid weather.",
    issues: ["Dark Leaf Spots", "Tip Drying", "Humid Weather Stress"],
    remedies: [
      "Spray copper oxychloride (3g per liter) or organic neem extract on foliage.",
      "Prune crowded inner branches after harvest to let sunlight shine into the middle of the tree.",
      "Collect and dispose of fallen dry leaves around the tree base.",
    ],
  },
  {
    id: "hibiscus",
    name: "Hibiscus / Gudhal",
    scientific: "Hibiscus rosa-sinensis",
    part: "Flower Buds & Leaves",
    status: "Pest Infestation",
    healthScore: 48,
    confidence: 96,
    sampleImage: REAL_PLANT_PHOTOS["Hibiscus"],
    diagnosis: "White cottony bugs (mealybugs) clustered near flower buds and leaf joints, causing bud drop.",
    issues: ["White Cottony Mealybugs", "Bud Drop", "Sticky Sap"],
    remedies: [
      "Wipe clusters off with a cotton swab dipped in rubbing alcohol, or spray with soapy neem solution.",
      "Rinse stems with a firm spray of clean water.",
      "Move the plant to a spot with at least 5 to 6 hours of bright direct sunshine daily.",
    ],
  },
  {
    id: "turmeric",
    name: "Turmeric Plant",
    scientific: "Curcuma longa (Haldi)",
    part: "Healthy Foliage & Stem",
    status: "Healthy",
    healthScore: 96,
    confidence: 98,
    sampleImage: REAL_PLANT_PHOTOS["Turmeric"],
    diagnosis: "Completely healthy plant. Deep green leaves with smooth edges and vibrant vegetative growth.",
    issues: ["Healthy green leaves", "Strong Root Vigor"],
    remedies: [
      "Mulch soil around the plant with dry leaves to retain moisture.",
      "Water moderately when top soil feels dry; avoid standing water.",
    ],
  },
];

const GALLERY_TABS = [
  { id: "all", label: "All Plants" },
  { id: "palms", label: "Palms & Big Trees" },
  { id: "spices", label: "Spices & Kitchen" },
  { id: "medicinal", label: "Medicinal & Herbs" },
  { id: "flowers", label: "Garden Flowers" },
  { id: "fruits-trees", label: "Fruits & Orchards" },
  { id: "indoor", label: "Indoor & Air-Purifying" },
];

export default function Home() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const [activeSpecimen, setActiveSpecimen] = useState(INTERACTIVE_SPECIMENS[0]);
  const [isScanningSimulation, setIsScanningSimulation] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState("all");
  const [modalSpice, setModalSpice] = useState(null);

  const [homeImage, setHomeImage] = useState(null);
  const [homeScan, setHomeScan] = useState(null);
  const [homeScanning, setHomeScanning] = useState(false);
  const [homeScanError, setHomeScanError] = useState("");

  const authed = user && typeof user === "object";

  useEffect(() => {
    if (location.hash) {
      const el = document.querySelector(location.hash);
      if (el) el.scrollIntoView({ behavior: "smooth" });
    }
  }, [location.hash]);

  const handleSelectPreset = (specimen) => {
    if (specimen.id === activeSpecimen.id) return;
    setIsScanningSimulation(true);
    setActiveSpecimen(specimen);
    setTimeout(() => setIsScanningSimulation(false), 500);
  };

  const cta = () => navigate(authed ? "/dashboard" : "/signup");

  const readHomeImage = (file) => {
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      setHomeScanError("Choose a plant photo in JPG, PNG, or WEBP format.");
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      setHomeImage(reader.result);
      setHomeScan(null);
      setHomeScanError("");
    };
    reader.readAsDataURL(file);
  };

  const scanHomeImage = async () => {
    if (!authed) {
      navigate("/login", { state: { from: { pathname: "/dashboard", state: { scanImage: homeImage } } } });
      return;
    }
    if (!homeImage) return;
    setHomeScanning(true);
    setHomeScanError("");
    try {
      const { data } = await api.post("/scans", { image_base64: homeImage, plant_name: "" });
      setHomeScan(data.scan);
    } catch (err) {
      setHomeScanError(apiError(err));
    } finally {
      setHomeScanning(false);
    }
  };

  // Filter curated signature plants for showcase gallery
  const filteredGalleryPlants = SIGNATURE_GALLERY_PLANTS.filter((plant) => {
    if (selectedCategory === "all") return true;
    const cat = (plant.category || "").toLowerCase();
    const name = (plant.name || "").toLowerCase();
    if (selectedCategory === "palms") return cat.includes("palm") || name.includes("palm") || cat.includes("wood") || name.includes("bamboo");
    if (selectedCategory === "spices") return cat.includes("spice") || cat.includes("kitchen") || cat.includes("vegetable") || cat.includes("grain") || cat.includes("crop");
    if (selectedCategory === "medicinal") return cat.includes("medicinal") || cat.includes("herb") || cat.includes("ayurvedic") || cat.includes("tonic");
    if (selectedCategory === "flowers") return cat.includes("flower") || cat.includes("garden");
    if (selectedCategory === "fruits-trees") return cat.includes("fruit") || cat.includes("tree") || cat.includes("orchard");
    if (selectedCategory === "indoor") return cat.includes("indoor") || cat.includes("air") || cat.includes("foliage") || name.includes("snake") || name.includes("pothos") || name.includes("peace");
    return true;
  });

  return (
    <Shell>
      {/* HERO SECTION - Responsive on mobile, tablet, and desktop */}
      <section className="relative overflow-hidden pt-6 pb-14 sm:pt-12 sm:pb-20 md:py-24">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="grid items-center gap-8 lg:grid-cols-12 lg:gap-14">
            <div className="lg:col-span-7 animate-fade-up">
              <div
                className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-3 py-1 font-mono text-[10px] sm:text-[11px] font-medium uppercase tracking-[0.18em] text-primary dark:border-accent/30 dark:bg-accent/10 dark:text-accent"
                data-testid="hero-badge"
              >
                <Sprout className="h-3.5 w-3.5 text-accent shrink-0" />
                <span className="truncate">Smart Plant Doctor • Subcontinental Species</span>
              </div>

              <h1 className="mt-4 sm:mt-6 font-serif text-3xl sm:text-5xl lg:text-6xl font-normal tracking-tight text-foreground leading-[1.12]">
                Keep your plants healthy with{" "}
                <span className="italic text-primary underline decoration-accent/40 decoration-wavy decoration-2">
                  instant AI checks
                </span>
                .
              </h1>

              <p className="mt-4 sm:mt-6 max-w-xl text-sm sm:text-base md:text-lg text-muted-foreground leading-relaxed">
                Tuned specifically for Indian subcontinent plants — coconut palms, mango orchards, courtyard flowers,
                kitchen spices, and healing herbs. Simply snap a photo to diagnose issues and get natural organic remedies.
              </p>

              <div className="mt-6 sm:mt-8 flex flex-col sm:flex-row items-stretch sm:items-center gap-3 sm:gap-4">
                <Button
                  onClick={cta}
                  size="lg"
                  className="rounded-full bg-primary px-6 sm:px-8 py-3 text-xs sm:text-sm font-semibold uppercase tracking-wider text-primary-foreground shadow-sm transition-all hover:opacity-95 hover:shadow-md"
                  data-testid="hero-cta-button"
                >
                  <ScanLine className="mr-2 h-4 w-4" />
                  {authed ? "Open Plant Scanner" : "Scan a Plant Now"}
                </Button>
                <a
                  href="#scanner-demo"
                  className="inline-flex items-center justify-center gap-2 rounded-full border border-primary/20 bg-background/80 px-5 sm:px-6 py-3 text-xs font-semibold uppercase tracking-wider text-foreground transition-all hover:bg-secondary/60 hover:border-primary/40 text-center"
                  data-testid="hero-login-button"
                >
                  <Compass className="h-4 w-4 text-primary" />
                  View sample report
                </a>
              </div>

              {/* Responsive Stats row */}
              <div className="mt-8 sm:mt-12 grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 border-t border-primary/10 pt-5 sm:pt-6">
                <div>
                  <p className="font-mono text-lg sm:text-2xl font-bold text-foreground">50+</p>
                  <p className="font-mono text-[9px] sm:text-[10px] uppercase tracking-wider text-muted-foreground">Subcontinent Plants</p>
                </div>
                <div>
                  <p className="font-mono text-lg sm:text-2xl font-bold text-foreground">100%</p>
                  <p className="font-mono text-[9px] sm:text-[10px] uppercase tracking-wider text-muted-foreground">Natural Remedies</p>
                </div>
                <div>
                  <p className="font-mono text-lg sm:text-2xl font-bold text-foreground">Fast AI</p>
                  <p className="font-mono text-[9px] sm:text-[10px] uppercase tracking-wider text-muted-foreground">Instant Diagnosis</p>
                </div>
                <div>
                  <p className="font-mono text-lg sm:text-2xl font-bold text-accent">All Devices</p>
                  <p className="font-mono text-[9px] sm:text-[10px] uppercase tracking-wider text-muted-foreground">Mobile & Tablet</p>
                </div>
              </div>
            </div>

            {/* Showcase Visual Hero Card */}
            <div className="lg:col-span-5">
              <div className="relative mx-auto w-full max-w-sm sm:max-w-md rounded-3xl border border-primary/15 bg-card p-3 sm:p-4 shadow-xl herbarium-glass">
                <div className="flex items-center justify-between border-b border-primary/10 pb-2.5 px-2">
                  <div className="flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full bg-accent" />
                    <span className="font-mono text-[9px] sm:text-[10px] uppercase tracking-[0.18em] text-muted-foreground">
                      VERIFIED INDIAN FLORA
                    </span>
                  </div>
                  <span className="rounded-full bg-primary/10 px-2.5 py-0.5 font-mono text-[9px] uppercase tracking-wider text-primary font-semibold">
                    Coconut Palm
                  </span>
                </div>

                <div className="relative mt-3 h-60 sm:h-72 w-full overflow-hidden rounded-2xl bg-muted/40">
                  <img
                    src={REAL_PLANT_PHOTOS["Coconut Palm"]}
                    alt="Real life coconut palm"
                    className="h-full w-full object-cover transition-transform duration-700 hover:scale-105"
                  />
                  <div className="absolute inset-3 pointer-events-none border border-white/25 rounded-xl">
                    <div className="absolute -top-1 -left-1 h-3 w-3 border-t-2 border-l-2 border-accent" />
                    <div className="absolute -top-1 -right-1 h-3 w-3 border-t-2 border-r-2 border-accent" />
                    <div className="absolute -bottom-1 -left-1 h-3 w-3 border-b-2 border-l-2 border-accent" />
                    <div className="absolute -bottom-1 -right-1 h-3 w-3 border-b-2 border-r-2 border-accent" />
                  </div>
                  <div className="absolute bottom-3 left-3 flex items-center gap-2 rounded-full bg-background/90 backdrop-blur-md px-3 py-1 shadow-md">
                    <span className="flex h-2 w-2 rounded-full bg-accent animate-ping" />
                    <span className="font-mono text-xs font-bold text-foreground">Health: 95/100</span>
                    <span className="font-mono text-[10px] text-muted-foreground hidden sm:inline">· Healthy Palm</span>
                  </div>
                </div>

                <div className="p-2 sm:p-3 pt-3">
                  <div className="flex items-baseline justify-between">
                    <h3 className="font-serif text-base sm:text-lg font-medium text-foreground">Coconut Palm (Nariyal)</h3>
                    <span className="font-serif italic text-xs text-muted-foreground">Cocos nucifera</span>
                  </div>
                  <p className="mt-1 text-xs text-muted-foreground leading-relaxed">
                    Revered as 'Kalpavriksha' across India. Provides refreshing coconut water, healthy oil, and natural fibers.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* QUICK PHOTO SCANNER SECTION */}
      <section id="scanner" className="border-y border-primary/10 bg-secondary/20 py-12 sm:py-16">
        <div className="mx-auto grid max-w-7xl gap-8 px-4 sm:px-6 lg:grid-cols-[0.8fr_1.2fr] lg:px-8 items-center">
          <div>
            <div className="inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.2em] text-primary">
              <ScanLine className="h-4 w-4 text-accent" />
              <span>Plant Health Check</span>
            </div>
            <h2 className="mt-2 font-serif text-2xl sm:text-4xl font-normal tracking-tight text-foreground">
              A clearer picture of plant health
            </h2>
            <p className="mt-3 text-xs sm:text-sm leading-relaxed text-muted-foreground">
              Upload or snap a photo of any leaf, stem, or whole plant. FLORAai checks for visible signs of diseases, pests,
              or nutrient deficiencies and delivers an actionable care report.
            </p>
            <div className="mt-4 flex flex-wrap gap-2 text-xs text-muted-foreground">
              <span className="rounded-full border border-primary/10 bg-background px-3 py-1">All Subcontinent Species</span>
              <span className="rounded-full border border-primary/10 bg-background px-3 py-1">Organic Remedies</span>
            </div>
          </div>

          <Card className="overflow-hidden rounded-3xl border-primary/15 bg-card shadow-lg">
            <CardContent className="p-4 sm:p-7">
              <input
                type="file"
                accept="image/*"
                capture="environment"
                className="hidden"
                id="home-plant-photo"
                data-testid="home-upload-input"
                onChange={(e) => readHomeImage(e.target.files?.[0])}
              />
              {homeImage ? (
                <div className="relative overflow-hidden rounded-2xl bg-neutral-900">
                  <img src={homeImage} alt="Selected plant" className="max-h-80 w-full object-contain" />
                  <button
                    type="button"
                    onClick={() => { setHomeImage(null); setHomeScan(null); }}
                    aria-label="Remove photo"
                    className="absolute right-3 top-3 flex h-8 w-8 items-center justify-center rounded-full bg-black/70 text-white hover:bg-black transition-colors"
                  >
                    <X className="h-4 w-4" />
                  </button>
                </div>
              ) : (
                <label
                  htmlFor="home-plant-photo"
                  data-testid="home-dropzone"
                  className="group flex min-h-52 cursor-pointer flex-col items-center justify-center rounded-2xl border-2 border-dashed border-primary/20 bg-secondary/20 px-4 py-8 text-center transition-colors hover:border-primary/40 hover:bg-secondary/40"
                >
                  <span className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/10 text-primary transition-transform group-hover:scale-105">
                    <UploadCloud className="h-6 w-6" />
                  </span>
                  <span className="mt-3 font-serif text-base sm:text-lg font-medium text-foreground">Add a clear plant photo</span>
                  <span className="mt-1 text-xs text-muted-foreground">Choose from device or take photo with camera</span>
                  <span className="mt-4 rounded-full bg-primary px-5 py-2 text-xs font-semibold uppercase tracking-wider text-primary-foreground shadow-xs">
                    Choose Photo
                  </span>
                </label>
              )}

              {homeScanError && (
                <p role="alert" className="mt-3 rounded-xl bg-destructive/10 px-4 py-2.5 text-xs text-destructive">
                  {homeScanError}
                </p>
              )}

              {homeImage && !homeScan && (
                <div className="mt-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
                  <p className="text-xs text-muted-foreground">
                    {authed ? "Photo ready for instant analysis." : "Sign in to run full analysis and save reports."}
                  </p>
                  <Button
                    onClick={scanHomeImage}
                    disabled={homeScanning}
                    className="rounded-full px-6 py-2.5 text-xs font-semibold uppercase tracking-wider"
                    data-testid="home-scan-button"
                  >
                    {homeScanning ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Checking…
                      </>
                    ) : (
                      <>
                        <ScanLine className="mr-2 h-4 w-4" /> {authed ? "Check Plant Health" : "Sign in to Scan"}
                      </>
                    )}
                  </Button>
                </div>
              )}

              {homeScan && (
                <div className="mt-5">
                  <ScanResult scan={homeScan} />
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </section>

      {/* INTERACTIVE DEMONSTRATION SECTION */}
      <section id="scanner-demo" className="relative border-y border-primary/10 bg-background py-14 sm:py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-2xl mx-auto mb-8 sm:mb-12">
            <div className="inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.22em] text-primary">
              <Activity className="h-3.5 w-3.5 text-accent shrink-0" />
              <span>Interactive Plant Doctor Demo</span>
            </div>
            <h2 className="mt-2 font-serif text-2xl sm:text-4xl font-normal tracking-tight text-foreground">
              See How It Checks Your Plants
            </h2>
            <p className="mt-2 text-xs sm:text-sm text-muted-foreground leading-relaxed">
              Tap any specimen below to see how our AI identifies problems and prescribes simple organic remedies:
            </p>

            {/* Specimen switcher buttons - Touch-friendly and wrapped */}
            <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
              {INTERACTIVE_SPECIMENS.map((s) => {
                const active = s.id === activeSpecimen.id;
                return (
                  <button
                    key={s.id}
                    onClick={() => handleSelectPreset(s)}
                    className={`flex items-center gap-2 rounded-full px-3.5 py-1.5 sm:px-4 sm:py-2 text-[11px] sm:text-xs font-semibold uppercase tracking-wider transition-all ${
                      active
                        ? "bg-primary text-primary-foreground shadow-sm"
                        : "border border-primary/15 bg-card text-muted-foreground hover:text-foreground hover:bg-secondary"
                    }`}
                  >
                    <span>{s.name}</span>
                    <span
                      className={`h-1.5 w-1.5 rounded-full ${
                        s.status === "Healthy" ? "bg-accent" : "bg-[hsl(14_62%_48%)]"
                      }`}
                    />
                  </button>
                );
              })}
            </div>
          </div>

          {/* Viewport: Dynamic for mobile, tablet, and desktop */}
          <div className="grid gap-6 sm:gap-8 lg:grid-cols-12 items-stretch">
            {/* Photo Viewport */}
            <div className="lg:col-span-6 flex flex-col">
              <div className="relative flex-1 overflow-hidden rounded-3xl border border-primary/20 bg-black/90 p-2.5 sm:p-3 shadow-xl">
                <div className="relative h-64 sm:h-80 md:h-96 w-full overflow-hidden rounded-2xl bg-neutral-900">
                  <img
                    src={activeSpecimen.sampleImage}
                    alt={activeSpecimen.name}
                    className={`h-full w-full object-cover transition-all duration-700 ${
                      isScanningSimulation ? "scale-105 filter blur-xs" : "scale-100 filter-none"
                    }`}
                  />

                  {/* Optical Reticle Overlay */}
                  <div className="absolute inset-0 pointer-events-none p-3 sm:p-5 flex flex-col justify-between">
                    <div className="flex items-center justify-between text-white/90 font-mono text-[9px] sm:text-[10px] tracking-wider uppercase">
                      <span className="flex items-center gap-1.5">
                        <span className="h-2 w-2 rounded-full bg-accent animate-ping" />
                        AI SCANNER READY
                      </span>
                      <span>FOCUS: {activeSpecimen.part}</span>
                    </div>

                    <div className="border border-white/25 rounded-xl absolute inset-4 sm:inset-6">
                      <div className="absolute -top-1 -left-1 h-3.5 w-3.5 border-t-2 border-l-2 border-accent" />
                      <div className="absolute -top-1 -right-1 h-3.5 w-3.5 border-t-2 border-r-2 border-accent" />
                      <div className="absolute -bottom-1 -left-1 h-3.5 w-3.5 border-b-2 border-l-2 border-accent" />
                      <div className="absolute -bottom-1 -right-1 h-3.5 w-3.5 border-b-2 border-r-2 border-accent" />
                    </div>

                    <div className="flex items-center justify-between text-white/90 font-mono text-[9px] sm:text-[10px] tracking-widest uppercase">
                      <span>CONFIDENCE: {activeSpecimen.confidence}%</span>
                      <span className="text-accent">{activeSpecimen.status}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Diagnostic Report Panel */}
            <div className="lg:col-span-6 flex flex-col">
              <div className="flex flex-1 flex-col justify-between rounded-3xl border border-primary/20 bg-card p-5 sm:p-7 shadow-xl">
                <div>
                  <div className="flex items-start justify-between border-b border-primary/10 pb-4">
                    <div>
                      <h3 className="font-serif text-xl sm:text-2xl font-medium text-foreground">
                        {activeSpecimen.name}
                      </h3>
                      <p className="font-serif italic text-xs text-muted-foreground mt-0.5">
                        {activeSpecimen.scientific}
                      </p>
                    </div>

                    <div className="text-right">
                      <Badge
                        className={`rounded-full px-3 py-1 font-mono text-[10px] uppercase tracking-wider font-semibold ${
                          activeSpecimen.status === "Healthy"
                            ? "bg-accent/15 text-accent border-accent/25"
                            : "bg-[hsl(14_62%_48%)]/15 text-[hsl(14_62%_48%)] border-[hsl(14_62%_48%)]/25"
                        }`}
                      >
                        {activeSpecimen.status}
                      </Badge>
                      <p className="font-mono text-[10px] text-muted-foreground mt-1">
                        Score: {activeSpecimen.healthScore}/100
                      </p>
                    </div>
                  </div>

                  <p className="mt-4 text-xs sm:text-sm leading-relaxed text-foreground/85">
                    {activeSpecimen.diagnosis}
                  </p>

                  <div className="mt-4">
                    <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground font-semibold">
                      Signs Observed
                    </p>
                    <div className="mt-2 flex flex-wrap gap-1.5">
                      {activeSpecimen.issues.map((issue) => (
                        <span
                          key={issue}
                          className="rounded-full border border-primary/10 bg-primary/5 px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-primary"
                        >
                          {issue}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="mt-5 border-t border-primary/10 pt-4">
                    <p className="flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.2em] text-primary font-semibold">
                      <Leaf className="h-3 w-3 text-accent" />
                      Natural Home Remedies to Fix It
                    </p>
                    <div className="mt-2.5 space-y-2">
                      {activeSpecimen.remedies.map((remedy, idx) => (
                        <div key={idx} className="flex items-start gap-2.5 text-xs text-foreground/85">
                          <span className="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-primary/10 font-mono text-[9px] font-bold text-primary">
                            {idx + 1}
                          </span>
                          <span className="leading-snug">{remedy}</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="mt-6 border-t border-primary/10 pt-4 flex items-center justify-between">
                  <span className="font-mono text-[10px] text-muted-foreground">
                    100% Natural Organic Care
                  </span>
                  <Button
                    onClick={cta}
                    variant="ghost"
                    size="sm"
                    className="text-xs font-semibold text-primary hover:text-primary/80 p-0 hover:bg-transparent"
                  >
                    Check your plant <ArrowRight className="ml-1 h-3.5 w-3.5" />
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CURATED SHOWCASE PLANT GALLERY SECTION */}
      <section id="spices" className="scroll-mt-20 py-14 sm:py-20 md:py-28 mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10">
          <div>
            <div className="inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.22em] text-primary">
              <Compass className="h-3.5 w-3.5 text-accent" />
              <span>Plant Showcase Gallery</span>
            </div>
            <h2 className="mt-2 font-serif text-2xl sm:text-4xl font-normal tracking-tight text-foreground">
              Signature Indian Subcontinent Species
            </h2>
            <p className="mt-2 text-xs sm:text-sm text-muted-foreground max-w-xl">
              Curated verified gallery of signature courtyard flowers, healing herbs, fruit trees, palms, and spices.
              Tap any card to view botanical profiles, common diseases, and natural home remedies.
            </p>
            <a
              className="mt-2 inline-block text-xs text-primary underline underline-offset-4"
              href="/plants/credits.json"
              target="_blank"
              rel="noreferrer"
            >
              View photo licenses and sources
            </a>
          </div>

          {/* Filter tabs - Touch-scrollable on mobile */}
          <div className="flex flex-wrap items-center gap-1.5">
            {GALLERY_TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setSelectedCategory(tab.id)}
                className={`rounded-full px-3.5 py-1.5 text-[11px] sm:text-xs font-semibold uppercase tracking-wider transition-all ${
                  selectedCategory === tab.id
                    ? "bg-primary text-primary-foreground shadow-xs"
                    : "border border-primary/10 bg-background text-muted-foreground hover:text-foreground hover:bg-secondary"
                }`}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        {/* Dynamic Responsive Plant Cards Grid: 1 col on small phones, 2 on tablet, 3-4 on desktop */}
        <div className="grid gap-5 sm:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {filteredGalleryPlants.map((s) => {
            const photoUrl = getPlantImage(s.name);
            const commonName = s.name.split("(")[0].trim();
            const scientificName = s.name.includes("(")
              ? s.name.split("(")[1].replace(")", "")
              : s.scientific_name;

            return (
              <div
                key={s.name}
                onClick={() => setModalSpice(s)}
                className="group relative cursor-pointer overflow-hidden rounded-3xl border border-primary/15 bg-card transition-all duration-300 hover:-translate-y-1 hover:shadow-lg hover:border-primary/30 flex flex-col justify-between"
                data-testid={`plant-card-${commonName.split(" ")[0].toLowerCase()}`}
              >
                <div>
                  <div className="relative h-52 sm:h-56 overflow-hidden bg-muted">
                    {photoUrl ? (
                      <img
                        src={photoUrl}
                        alt={s.name}
                        className="h-full w-full object-cover transition-transform duration-700 group-hover:scale-105"
                      />
                    ) : (
                      <div className="flex h-full flex-col items-center justify-center gap-2 bg-secondary text-muted-foreground">
                        <Sprout className="h-8 w-8" />
                        <span className="text-xs">Photo unavailable</span>
                      </div>
                    )}
                    <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent" />

                    <div className="absolute top-3 right-3 rounded-full bg-accent/95 backdrop-blur-md px-2.5 py-0.5 font-mono text-[9px] uppercase tracking-wider text-accent-foreground font-bold shadow-xs">
                      VERIFIED PHOTO
                    </div>

                    {s.family && (
                      <div className="absolute top-3 left-3 rounded-full bg-black/60 backdrop-blur-md px-2.5 py-0.5 font-mono text-[9px] uppercase tracking-wider text-white border border-white/15">
                        {s.family.split("(")[0].trim()}
                      </div>
                    )}

                    <div className="absolute bottom-3 left-4 right-4 text-white">
                      <p className="font-serif italic text-xs text-white/95 drop-shadow-xs">
                        {scientificName}
                      </p>
                    </div>
                  </div>

                  <div className="p-4 sm:p-5">
                    <div className="flex items-center justify-between">
                      <h3 className="font-serif text-base sm:text-lg font-medium text-foreground group-hover:text-primary transition-colors">
                        {commonName}
                      </h3>
                      <ArrowRight className="h-4 w-4 text-muted-foreground transition-transform group-hover:translate-x-1 group-hover:text-primary shrink-0" />
                    </div>

                    {s.role && (
                      <p className="mt-1.5 text-xs text-muted-foreground line-clamp-2 leading-relaxed font-serif">
                        {s.role}
                      </p>
                    )}

                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {s.common_issues.slice(0, 2).map((issue) => (
                        <span
                          key={issue}
                          className="rounded-full bg-secondary/80 px-2 py-0.5 font-mono text-[9px] uppercase tracking-wide text-secondary-foreground"
                        >
                          {issue}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="px-4 sm:px-5 pb-4 pt-2 border-t border-primary/10 flex items-center justify-between text-xs text-muted-foreground">
                  <span className="font-mono text-[9px] uppercase tracking-wider text-primary font-semibold">
                    ORGANIC CARE
                  </span>
                  <span className="text-[11px] font-medium text-primary">View Care Guide →</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* PLANT DETAIL DIALOG */}
      {modalSpice && (
        <Dialog open={!!modalSpice} onOpenChange={(open) => !open && setModalSpice(null)}>
          <DialogContent className="max-w-xl w-[95vw] sm:w-full rounded-3xl p-5 sm:p-7 max-h-[88vh] overflow-y-auto">
            <DialogHeader>
              <div className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-widest text-primary">
                <Leaf className="h-3.5 w-3.5 text-accent" />
                <span>PLANT CARE GUIDE</span>
              </div>
              <DialogTitle className="font-serif text-xl sm:text-2xl font-medium mt-1">
                {modalSpice.name}
              </DialogTitle>
              <DialogDescription className="font-serif italic text-xs text-muted-foreground">
                {modalSpice.scientific_name || modalSpice.name}
              </DialogDescription>
            </DialogHeader>

            <div className="mt-3 space-y-3.5">
              <div className="h-56 sm:h-64 w-full overflow-hidden rounded-2xl bg-neutral-900 relative">
                {getPlantImage(modalSpice.name) ? (
                  <img
                    src={getPlantImage(modalSpice.name)}
                    alt={modalSpice.name}
                    className="h-full w-full object-cover"
                  />
                ) : (
                  <div className="flex h-full flex-col items-center justify-center gap-2 text-white/70">
                    <Sprout className="h-8 w-8" />
                    <span className="text-xs">Photo unavailable</span>
                  </div>
                )}
                <Badge className="absolute top-3 right-3 bg-accent text-accent-foreground font-mono text-[9px] uppercase tracking-wider font-bold">
                  VERIFIED PHOTO
                </Badge>
                {modalSpice.family && (
                  <Badge className="absolute bottom-3 left-3 bg-black/70 backdrop-blur-md text-white font-mono text-[9px] uppercase tracking-wider">
                    Family: {modalSpice.family}
                  </Badge>
                )}
              </div>

              {modalSpice.role && (
                <div className="rounded-2xl border border-primary/15 bg-primary/5 p-3.5">
                  <h4 className="font-mono text-[10px] uppercase tracking-wider text-primary font-bold">
                    Role & Uses in India (Why this plant is valuable)
                  </h4>
                  <p className="mt-1 text-xs text-foreground/90 font-serif leading-relaxed">
                    {modalSpice.role}
                  </p>
                </div>
              )}

              {modalSpice.description && (
                <div className="rounded-2xl border border-primary/10 bg-secondary/30 p-3.5">
                  <h4 className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
                    About this Plant
                  </h4>
                  <p className="mt-1 text-xs text-foreground/80 leading-relaxed">
                    {modalSpice.description}
                  </p>
                </div>
              )}

              <div>
                <h4 className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
                  Common Problems & Sicknesses
                </h4>
                <div className="mt-1.5 flex flex-wrap gap-1.5">
                  {modalSpice.common_issues.map((i) => (
                    <span
                      key={i}
                      className="rounded-full bg-secondary px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wide text-foreground"
                    >
                      {i}
                    </span>
                  ))}
                </div>
              </div>

              {modalSpice.problem_cause && (
                <div className="rounded-2xl border border-[hsl(14_62%_48%)]/20 bg-[hsl(14_62%_48%)]/5 p-3.5">
                  <h4 className="font-mono text-[10px] uppercase tracking-wider text-[hsl(14_62%_48%)] font-bold">
                    What Happens to this Plant (Why it gets sick)
                  </h4>
                  <p className="mt-1 text-xs text-foreground/85 leading-relaxed">
                    {modalSpice.problem_cause}
                  </p>
                </div>
              )}

              <div className="rounded-2xl border border-primary/15 bg-secondary/30 p-3.5">
                <h4 className="font-mono text-[10px] uppercase tracking-wider text-primary font-bold">
                  Natural Organic Remedies to Fix It
                </h4>
                <div className="mt-1.5 space-y-1">
                  {Array.isArray(modalSpice.remedies) ? (
                    modalSpice.remedies.map((rem, i) => (
                      <p key={i} className="text-xs text-foreground/90 leading-relaxed">
                        • {rem}
                      </p>
                    ))
                  ) : (
                    <p className="text-xs text-foreground/90 leading-relaxed">{modalSpice.remedies}</p>
                  )}
                </div>
              </div>

              {modalSpice.precautions && modalSpice.precautions.length > 0 && (
                <div className="rounded-2xl border-2 border-accent/40 bg-accent/5 p-3.5">
                  <h4 className="font-mono text-[10px] uppercase tracking-wider text-accent font-bold">
                    Simple Steps to Keep this Plant Safe & Healthy
                  </h4>
                  <div className="mt-1.5 space-y-1">
                    {modalSpice.precautions.map((p, i) => (
                      <p key={i} className="text-xs text-foreground/90 leading-relaxed">
                        ✓ {p}
                      </p>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-5 flex justify-end gap-3 pt-2">
                <Button variant="outline" className="rounded-full text-xs" onClick={() => setModalSpice(null)}>
                  Close
                </Button>
                <Button className="rounded-full bg-primary text-primary-foreground text-xs" onClick={cta}>
                  Scan a Photo of this Plant
                </Button>
              </div>
            </div>
          </DialogContent>
        </Dialog>
      )}

      {/* 3 SIMPLE STEPS SECTION */}
      <section id="methodology" className="border-t border-primary/10 bg-secondary/20 py-14 sm:py-20 md:py-28">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="max-w-2xl mx-auto text-center mb-10 sm:mb-14">
            <div className="inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.22em] text-primary">
              <Sprout className="h-3.5 w-3.5 text-accent" />
              <span>Easy 3-Step Process</span>
            </div>
            <h2 className="mt-2 font-serif text-2xl sm:text-4xl font-normal tracking-tight text-foreground">
              How FLORAai Helps Care for Your Plants
            </h2>
            <p className="mt-2 text-xs sm:text-sm text-muted-foreground leading-relaxed">
              No complicated tools or harsh chemicals. Simple natural care accessible to everyone:
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-3">
            {[
              {
                step: "01",
                icon: Camera,
                title: "1. Snap a Photo",
                subtitle: "Phone camera or upload",
                text: "Point your camera at yellowing leaves, brown spots, or pests on any device.",
              },
              {
                step: "02",
                icon: LineChart,
                title: "2. Detects the Problem",
                subtitle: "Disease, pest, or moisture stress",
                text: "Identifies whether the plant suffers from fungus, bugs, poor drainage, or sun stress.",
              },
              {
                step: "03",
                icon: Leaf,
                title: "3. Organic Remedies",
                subtitle: "100% natural, safe, and organic",
                text: "Gives easy recipes like neem oil spray, proper watering, and preventive tips.",
              },
            ].map((card) => (
              <Card
                key={card.step}
                className="rounded-3xl border-primary/15 bg-card p-6 shadow-xs transition-all hover:-translate-y-1 hover:shadow-md"
              >
                <CardContent className="p-0">
                  <div className="flex items-center justify-between">
                    <span className="flex h-11 w-11 items-center justify-center rounded-2xl border border-primary/20 bg-primary/5 text-primary">
                      <card.icon className="h-5 w-5" />
                    </span>
                    <span className="font-mono text-2xl font-bold text-muted-foreground/30">
                      {card.step}
                    </span>
                  </div>
                  <h3 className="mt-5 font-serif text-lg sm:text-xl font-medium text-foreground">
                    {card.title}
                  </h3>
                  <p className="font-mono text-[9px] uppercase tracking-wider text-accent font-semibold mt-1">
                    {card.subtitle}
                  </p>
                  <p className="mt-2 text-xs text-muted-foreground leading-relaxed">
                    {card.text}
                  </p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* CTA BAND */}
      <section className="mx-auto max-w-7xl px-4 pb-16 sm:pb-24 sm:px-6 lg:px-8">
        <div className="relative overflow-hidden rounded-3xl bg-primary px-6 py-10 sm:px-14 sm:py-14 text-primary-foreground shadow-xl">
          <Leaf className="absolute -right-8 -bottom-8 h-56 w-56 text-white/5 pointer-events-none" />
          <div className="relative max-w-xl">
            <span className="inline-flex items-center gap-1.5 rounded-full bg-accent/20 px-3 py-1 font-mono text-[10px] uppercase tracking-wider text-accent font-semibold">
              <Sparkles className="h-3 w-3" />
              <span>Free Plant Care</span>
            </span>
            <h2 className="mt-3 font-serif text-2xl sm:text-4xl font-medium text-white leading-tight">
              {authed ? "Ready to check another plant?" : "Save your plant photos and health reports"}
            </h2>
            <p className="mt-2 text-xs sm:text-sm text-white/80 leading-relaxed">
              {authed
                ? "Go to the scanner to take a photo of any plant or review your past scan history."
                : "Create a free account to track your plants, save health reports, and keep your home garden thriving."}
            </p>
            <div className="mt-6 flex flex-wrap items-center gap-4">
              <Button
                onClick={cta}
                size="lg"
                className="rounded-full bg-accent px-7 py-3 text-xs font-semibold uppercase tracking-wider text-accent-foreground hover:bg-accent/90"
                data-testid="cta-band-button"
              >
                {authed ? "Go to Plant Scanner" : "Get Started for Free"}
                <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
              {!authed && (
                <Link
                  to="/login"
                  className="text-xs font-medium text-white/70 underline underline-offset-4 hover:text-white"
                >
                  Already have an account? Sign in
                </Link>
              )}
            </div>
          </div>
        </div>
      </section>
    </Shell>
  );
}
