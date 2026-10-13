import React, { useEffect, useState, useRef } from "react";
import { Link, useLocation } from "react-router-dom";
import { Shell, PageHeader } from "@/components/Navbar";
import { ScanResult, statusColor } from "@/components/ScanResult";
import { useAuth } from "@/context/AuthContext";
import api, { apiError } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
  SelectGroup,
  SelectLabel,
} from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import {
  UploadCloud,
  Loader2,
  ScanLine,
  X,
  History,
  MailWarning,
  Camera,
  Leaf,
  Sparkles,
  Sprout,
  Image as ImageIcon,
  CheckCircle2,
} from "lucide-react";
import { toast } from "sonner";

const QUICK_SAMPLE_PLANTS = [
  { name: "Curry Leaf", label: "Curry Leaf (Kadi Patta)", url: "/plants/curry_leaf.jpg", category: "Spices" },
  { name: "Coconut Palm", label: "Coconut Palm (Nariyal)", url: "/plants/coconut.jpg", category: "Palms" },
  { name: "Lipstick Palm", label: "Lipstick Palm (Sealing Wax)", url: "/plants/lipstick_palm.jpg", category: "Palms" },
  { name: "Mango", label: "Mango Tree (Aam)", url: "/plants/mango.jpg", category: "Fruit" },
  { name: "Hibiscus / Gudhal", label: "Hibiscus (Gudhal)", url: "/plants/hibiscus.jpg", category: "Garden" },
  { name: "Tulsi", label: "Tulsi (Holy Basil)", url: "/plants/tulsi.jpg", category: "Medicinal" },
  { name: "Turmeric", label: "Turmeric (Haldi)", url: "/plants/turmeric.jpg", category: "Spices" },
  { name: "Neem", label: "Neem Tree", url: "/plants/neem.jpg", category: "Medicinal" },
  { name: "Lemon / Acid Lime", label: "Lemon Tree (Nimbu)", url: "/plants/lemon.jpg", category: "Fruit" },
  { name: "Guava", label: "Guava Tree (Amrood)", url: "/plants/guava.jpg", category: "Fruit" },
  { name: "Aloe Vera", label: "Aloe Vera (Ghritkumari)", url: "/plants/aloe_vera.jpg", category: "Medicinal" },
];

export default function Dashboard() {
  const { user } = useAuth();
  const location = useLocation();
  const fileRef = useRef(null);
  const videoRef = useRef(null);
  const streamRef = useRef(null);
  const [cameraOpen, setCameraOpen] = useState(false);
  const [image, setImage] = useState(null);
  const [plant, setPlant] = useState("");
  const [scanning, setScanning] = useState(false);
  const [scanStage, setScanStage] = useState(0);
  const [isDragging, setIsDragging] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [recent, setRecent] = useState([]);

  useEffect(() => {
    if (location.state?.scanImage) {
      setImage(location.state.scanImage);
      setResult(null);
    }
  }, [location.state]);

  const loadRecent = () =>
    api
      .get("/users/me/history")
      .then((r) => setRecent(r.data.scans.slice(0, 5)))
      .catch(() => {});

  useEffect(() => {
    loadRecent();
  }, []);

  useEffect(() => {
    if (!scanning) {
      setScanStage(0);
      return;
    }
    const interval = setInterval(() => {
      setScanStage((s) => (s + 1) % 3);
    }, 1200);
    return () => clearInterval(interval);
  }, [scanning]);

  const onFile = (file) => {
    if (!file) return;
    if (!file.type.startsWith("image/")) {
      setError("Please choose a valid image file (JPEG, PNG or WEBP).");
      return;
    }
    const reader = new FileReader();
    reader.onload = () => {
      setImage(reader.result);
      setResult(null);
      setError("");
    };
    reader.readAsDataURL(file);
  };

  const loadSamplePlant = async (sample) => {
    setError("");
    setPlant(sample.name);
    try {
      const response = await fetch(sample.url);
      const blob = await response.blob();
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
        setResult(null);
        toast.info(`Loaded photo for ${sample.label}. Click "Check Plant Health".`);
      };
      reader.readAsDataURL(blob);
    } catch {
      setError("Could not load sample plant photo. Please try uploading an image.");
    }
  };

  const scan = async () => {
    if (!image) {
      setError("Please upload or capture a plant photo to diagnose.");
      return;
    }
    setScanning(true);
    setError("");
    try {
      const { data } = await api.post("/scans", {
        image_base64: image,
        plant_name: plant === "Other / Auto-detect" ? "" : plant,
      });
      setResult(data.scan);
      toast.success("Plant health check complete.");
      loadRecent();
    } catch (err) {
      setError(apiError(err));
    } finally {
      setScanning(false);
    }
  };

  const reset = () => {
    setImage(null);
    setResult(null);
    setPlant("");
    if (fileRef.current) fileRef.current.value = "";
  };

  const openCamera = async () => {
    setError("");
    setCameraOpen(true);
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" },
      });
      streamRef.current = stream;
      if (videoRef.current) videoRef.current.srcObject = stream;
    } catch (e) {
      setCameraOpen(false);
      setError("Could not access camera. Please check browser permissions or upload a file.");
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
    setCameraOpen(false);
  };

  const capturePhoto = () => {
    const video = videoRef.current;
    if (!video) return;
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    canvas.getContext("2d").drawImage(video, 0, 0, canvas.width, canvas.height);
    setImage(canvas.toDataURL("image/jpeg", 0.9));
    setResult(null);
    setError("");
    stopCamera();
  };

  const scanMessages = [
    "Analyzing leaf venation & chloroplast density…",
    "Cross-referencing subcontinent botanical pathogen models…",
    "Formulating targeted organic Ayurvedic remedy protocol…",
  ];

  return (
    <Shell>
      <div className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        <PageHeader
          eyebrow={`Plant Care Studio • ${user.name.split(" ")[0]}`}
          title="Scan Your Plant"
          description="Take or upload a photo of any sick leaf, stem, or plant. We'll tell you what's wrong and give you simple, natural remedies to fix it."
          action={
            <Button
              asChild
              variant="outline"
              size="sm"
              className="rounded-full border-primary/20 text-xs font-semibold uppercase tracking-wider"
              data-testid="dashboard-history-button"
            >
              <Link to="/history">
                <History className="mr-1.5 h-3.5 w-3.5" /> My Scan History
              </Link>
            </Button>
          }
        />

        {user.email_verified === false && (
          <Alert
            className="mb-6 rounded-2xl border-[hsl(38_78%_54%)]/40 bg-[hsl(38_78%_54%)]/10"
            data-testid="verify-banner"
          >
            <MailWarning className="h-4 w-4 text-[hsl(38_78%_40%)]" />
            <AlertDescription className="text-xs text-foreground">
              Your email is pending verification.{" "}
              <Link to="/verify-email" className="font-semibold underline underline-offset-2">
                Verify now
              </Link>{" "}
              to enable automated weekly care digests.
            </AlertDescription>
          </Alert>
        )}

        <div className="grid gap-8 lg:grid-cols-[1.3fr_0.9fr] items-start">
          {/* Main Scanner Section */}
          <div className="space-y-6">
            <Card className="rounded-3xl border-primary/20 bg-card shadow-sm overflow-hidden">
              <CardContent className="p-6 sm:p-8">
                <input
                  ref={fileRef}
                  type="file"
                  accept="image/*"
                  className="hidden"
                  onChange={(e) => onFile(e.target.files?.[0])}
                  data-testid="plant-upload-input"
                />

                {!image ? (
                  <div className="space-y-4">
                    <button
                      type="button"
                      onClick={() => fileRef.current?.click()}
                      onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
                      onDragLeave={() => setIsDragging(false)}
                      onDrop={(e) => {
                        e.preventDefault();
                        setIsDragging(false);
                        if (e.dataTransfer.files?.[0]) onFile(e.dataTransfer.files[0]);
                      }}
                      className={`group flex w-full flex-col items-center justify-center gap-3.5 rounded-2xl border-2 border-dashed py-14 px-6 text-center transition-all ${
                        isDragging
                          ? "border-accent bg-accent/10 scale-[1.01]"
                          : "border-primary/20 bg-secondary/20 hover:border-primary/40 hover:bg-secondary/40"
                      }`}
                      data-testid="upload-dropzone"
                    >
                      <div className="relative flex h-16 w-16 items-center justify-center rounded-2xl border border-primary/20 bg-background/90 text-primary shadow-xs transition-transform duration-300 group-hover:scale-105">
                        <UploadCloud className="h-8 w-8" />
                        <span className="absolute -top-1 -right-1 h-3 w-3 rounded-full bg-accent" />
                      </div>
                      <div>
                        <p className="font-serif text-lg font-medium text-foreground">
                          Upload your plant photo
                        </p>
                        <p className="mt-1 font-mono text-[11px] uppercase tracking-wider text-muted-foreground">
                          Drop photo here or tap to browse · JPG, PNG, WEBP
                        </p>
                      </div>
                    </button>

                    <div className="flex flex-col sm:flex-row items-center gap-3">
                      <Button
                        type="button"
                        variant="outline"
                        onClick={openCamera}
                        className="w-full sm:flex-1 rounded-full border-primary/20 text-xs font-semibold uppercase tracking-wider hover:bg-secondary"
                        data-testid="open-camera-button"
                      >
                        <Camera className="mr-2 h-4 w-4 text-primary" /> Take a Photo with Camera
                      </Button>
                    </div>

                    {/* Quick test sample photos */}
                    <div className="pt-3 border-t border-primary/10">
                      <div className="flex items-center justify-between mb-2">
                        <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-muted-foreground font-semibold">
                          Try with sample plant photos:
                        </p>
                        <span className="font-mono text-[9px] text-muted-foreground">9 verified presets</span>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {QUICK_SAMPLE_PLANTS.map((sp) => (
                          <button
                            key={sp.label}
                            type="button"
                            onClick={() => loadSamplePlant(sp)}
                            className="inline-flex items-center gap-1.5 rounded-full border border-primary/15 bg-background px-3 py-1 text-[11px] font-medium text-foreground/80 hover:border-accent hover:bg-accent/10 hover:text-foreground transition-all shadow-2xs"
                          >
                            <ImageIcon className="h-3 w-3 text-primary" />
                            <span>{sp.label}</span>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {/* Image Preview with Viewfinder Brackets & Laser Scanning Beam */}
                    <div className="relative overflow-hidden rounded-2xl bg-neutral-900 shadow-md">
                      <img
                        src={image}
                        alt="Selected plant"
                        className="max-h-96 w-full object-cover"
                        data-testid="preview-image"
                      />

                      {/* Laser scanner overlay during diagnostic run */}
                      {scanning ? (
                        <div className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-black/50 backdrop-blur-2xs">
                          <div className="absolute inset-x-0 h-1 bg-gradient-to-r from-transparent via-accent to-transparent shadow-[0_0_15px_hsl(var(--accent))] animate-scan-laser" />
                          <div className="mx-4 rounded-2xl border border-accent/40 bg-background/90 px-5 py-3 text-center shadow-lg backdrop-blur-md">
                            <div className="flex items-center justify-center gap-2 text-accent font-mono text-xs uppercase tracking-wider font-semibold">
                              <Sparkles className="h-4 w-4 animate-spin" />
                              <span>AI Diagnostic Engine Active</span>
                            </div>
                            <p className="mt-1 font-mono text-[11px] text-muted-foreground transition-all">
                              {scanMessages[scanStage]}
                            </p>
                          </div>
                        </div>
                      ) : (
                        <>
                          {/* Reticle Brackets */}
                          <div className="absolute inset-5 pointer-events-none border border-white/20 rounded-xl">
                            <div className="absolute -top-1 -left-1 h-3 w-3 border-t-2 border-l-2 border-accent" />
                            <div className="absolute -top-1 -right-1 h-3 w-3 border-t-2 border-r-2 border-accent" />
                            <div className="absolute -bottom-1 -left-1 h-3 w-3 border-b-2 border-l-2 border-accent" />
                            <div className="absolute -bottom-1 -right-1 h-3 w-3 border-b-2 border-r-2 border-accent" />
                          </div>

                          <button
                            onClick={reset}
                            className="absolute right-3 top-3 flex h-8 w-8 items-center justify-center rounded-full bg-black/70 text-white backdrop-blur-md hover:bg-black transition-colors"
                            data-testid="clear-image-button"
                            title="Remove photo"
                          >
                            <X className="h-4 w-4" />
                          </button>

                          <div className="absolute bottom-3 left-3 flex items-center gap-1.5 rounded-full bg-black/60 backdrop-blur-md px-3 py-1 font-mono text-[10px] text-white">
                            <CheckCircle2 className="h-3 w-3 text-accent" />
                            <span>PHOTO READY TO CHECK</span>
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                )}

                {/* Configuration controls */}
                <div className="mt-5 flex flex-col gap-3 sm:flex-row">
                  <Select value={plant} onValueChange={setPlant}>
                    <SelectTrigger className="sm:w-64 rounded-xl" data-testid="dashboard-spice-select">
                      <SelectValue placeholder="Select plant name (or auto-detect)" />
                    </SelectTrigger>
                    <SelectContent className="max-h-80">
                      <SelectItem value="Other / Auto-detect">Auto-detect plant (AI)</SelectItem>
                      <SelectGroup>
                        <SelectLabel className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                          Kitchen Vegetables & Herbs
                        </SelectLabel>
                        <SelectItem value="Okra / Lady Finger">Okra / Lady Finger (Bhindi)</SelectItem>
                        <SelectItem value="Bitter Gourd">Bitter Gourd (Karela)</SelectItem>
                        <SelectItem value="Bottle Gourd">Bottle Gourd (Lauki)</SelectItem>
                        <SelectItem value="Spinach">Spinach (Palak)</SelectItem>
                        <SelectItem value="Mint">Mint (Pudina)</SelectItem>
                      </SelectGroup>
                      <SelectGroup>
                        <SelectLabel className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                          Palms & Big Plants
                        </SelectLabel>
                        <SelectItem value="Coconut Palm">Coconut Palm (Nariyal)</SelectItem>
                        <SelectItem value="Areca Nut / Betel Palm">Areca Nut / Supari Palm</SelectItem>
                        <SelectItem value="Lipstick Palm">Lipstick Palm (Sealing Wax Palm)</SelectItem>
                        <SelectItem value="Palmyra Palm">Palmyra Palm (Tadgola / Taad)</SelectItem>
                        <SelectItem value="Date Palm">Date Palm (Khajoor)</SelectItem>
                        <SelectItem value="Wild Date Palm">Wild Date Palm (Khajuri / Nolen Gur)</SelectItem>
                        <SelectItem value="Fish-tail Palm">Fish-tail Palm (Mari / Kitul)</SelectItem>
                        <SelectItem value="Golden Cane Palm">Golden Cane Palm (Dypsis)</SelectItem>
                        <SelectItem value="Royal Palm">Royal Palm (Raj Taad)</SelectItem>
                        <SelectItem value="Foxtail Palm">Foxtail Palm</SelectItem>
                        <SelectItem value="Bottle Palm">Bottle Palm</SelectItem>
                        <SelectItem value="Bismarck Palm">Bismarck Palm (Silver Fan Palm)</SelectItem>
                        <SelectItem value="Bamboo">Bamboo (Baans)</SelectItem>
                        <SelectItem value="Banana / Plantain">Banana Plant (Kela)</SelectItem>
                      </SelectGroup>
                      <SelectGroup>
                        <SelectLabel className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                          Fruit Trees
                        </SelectLabel>
                        <SelectItem value="Mango">Mango Tree (Aam - Alphonso/Kesar)</SelectItem>
                        <SelectItem value="Guava">Guava Tree (Amrood)</SelectItem>
                        <SelectItem value="Papaya">Papaya Plant (Papita)</SelectItem>
                        <SelectItem value="Lemon / Acid Lime">Lemon / Lime (Nimbu)</SelectItem>
                        <SelectItem value="Pomegranate">Pomegranate (Anaar)</SelectItem>
                        <SelectItem value="Jackfruit">Jackfruit Tree (Kathal)</SelectItem>
                      </SelectGroup>
                      <SelectGroup>
                        <SelectLabel className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                          Garden & Flowering Plants
                        </SelectLabel>
                        <SelectItem value="Hibiscus / Gudhal">Hibiscus (Gudhal / Jaswand)</SelectItem>
                        <SelectItem value="Jasmine / Mogra">Jasmine (Mogra / Chameli)</SelectItem>
                        <SelectItem value="Rose / Gulab">Rose (Gulab)</SelectItem>
                        <SelectItem value="Marigold / Genda">Marigold (Genda)</SelectItem>
                        <SelectItem value="Bougainvillea">Bougainvillea</SelectItem>
                        <SelectItem value="Plumeria / Champa">Champa (Plumeria)</SelectItem>
                        <SelectItem value="Lotus / Kamal">Lotus (Kamal)</SelectItem>
                      </SelectGroup>
                      <SelectGroup>
                        <SelectLabel className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                          Kitchen Spices
                        </SelectLabel>
                        <SelectItem value="Curry Leaf">Curry Leaf (Kadi Patta)</SelectItem>
                        <SelectItem value="Cardamom">Cardamom (Elaichi)</SelectItem>
                        <SelectItem value="Turmeric">Turmeric (Haldi)</SelectItem>
                        <SelectItem value="Black Pepper">Black Pepper (Kali Mirch)</SelectItem>
                        <SelectItem value="Cinnamon">Cinnamon (Dalchini)</SelectItem>
                        <SelectItem value="Clove">Clove (Laung)</SelectItem>
                        <SelectItem value="Ginger">Ginger (Adrak)</SelectItem>
                      </SelectGroup>
                      <SelectGroup>
                        <SelectLabel className="font-mono text-[10px] uppercase tracking-wider text-muted-foreground">
                          Medicinal & Courtyard Plants
                        </SelectLabel>
                        <SelectItem value="Tulsi">Tulsi (Holy Basil)</SelectItem>
                        <SelectItem value="Neem">Neem Tree</SelectItem>
                        <SelectItem value="Aloe Vera">Aloe Vera (Ghritkumari)</SelectItem>
                        <SelectItem value="Giloy">Giloy (Guduchi Vine)</SelectItem>
                        <SelectItem value="Brahmi">Brahmi (Water Hyssop)</SelectItem>
                        <SelectItem value="Shatavari">Shatavari (Wild Asparagus)</SelectItem>
                        <SelectItem value="Kalmegh">Kalmegh (King of Bitters)</SelectItem>
                        <SelectItem value="Vasaka">Vasaka / Adhatoda (Vasa)</SelectItem>
                        <SelectItem value="Money Plant">Money Plant (Pothos)</SelectItem>
                      </SelectGroup>
                    </SelectContent>
                  </Select>

                  <Button
                    onClick={scan}
                    disabled={scanning || !image}
                    className="flex-1 rounded-full bg-primary px-6 py-2.5 text-xs font-semibold uppercase tracking-wider text-primary-foreground shadow-sm hover:opacity-95 transition-opacity"
                    data-testid="scan-button"
                  >
                    {scanning ? (
                      <>
                        <Loader2 className="mr-2 h-4 w-4 animate-spin text-accent" />
                        Analyzing plant health…
                      </>
                    ) : (
                      <>
                        <ScanLine className="mr-2 h-4 w-4" />
                        Check Plant Health
                      </>
                    )}
                  </Button>
                </div>

                {error && (
                  <Alert variant="destructive" className="mt-4 rounded-2xl" data-testid="scan-error">
                    <AlertDescription className="text-xs">{error}</AlertDescription>
                  </Alert>
                )}
              </CardContent>
            </Card>

            {/* Diagnostic Result Certificate */}
            {result && <ScanResult scan={result} />}

            {/* Camera Dialog with Viewfinder */}
            <Dialog open={cameraOpen} onOpenChange={(o) => !o && stopCamera()}>
              <DialogContent className="max-w-md w-[92vw] sm:w-full rounded-3xl p-5 sm:p-6" data-testid="camera-dialog">
                <DialogHeader>
                  <DialogTitle className="font-serif text-lg sm:text-xl">Take Plant Photo</DialogTitle>
                  <DialogDescription className="text-xs">
                    Point your camera at the sick leaf or stem, then tap Take Photo.
                  </DialogDescription>
                </DialogHeader>
                <div className="relative overflow-hidden rounded-2xl bg-black aspect-4/3 sm:aspect-auto sm:h-72">
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="h-full w-full object-cover"
                  />
                  {/* Visual reticle */}
                  <div className="absolute inset-4 sm:inset-6 pointer-events-none border border-white/30 rounded-xl">
                    <div className="absolute -top-1 -left-1 h-3 w-3 border-t-2 border-l-2 border-accent" />
                    <div className="absolute -top-1 -right-1 h-3 w-3 border-t-2 border-r-2 border-accent" />
                    <div className="absolute -bottom-1 -left-1 h-3 w-3 border-b-2 border-l-2 border-accent" />
                    <div className="absolute -bottom-1 -right-1 h-3 w-3 border-b-2 border-r-2 border-accent" />
                  </div>
                </div>
                <div className="flex gap-3 mt-4">
                  <Button
                    variant="outline"
                    className="flex-1 rounded-full text-xs font-semibold uppercase"
                    onClick={stopCamera}
                    data-testid="camera-cancel-button"
                  >
                    Cancel
                  </Button>
                  <Button
                    className="flex-1 rounded-full bg-primary text-primary-foreground text-xs font-semibold uppercase"
                    onClick={capturePhoto}
                    data-testid="camera-capture-button"
                  >
                    <Camera className="mr-1.5 h-3.5 w-3.5" /> Take Photo
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Right Column: Recent Scans & Photo Tips */}
          <div className="space-y-6">
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-serif text-lg font-medium text-foreground">
                  Recent Scans
                </h3>
                <Link
                  to="/history"
                  className="font-mono text-[10px] uppercase tracking-wider text-primary hover:underline"
                >
                  View all ({recent.length})
                </Link>
              </div>

              <div className="space-y-2.5" data-testid="recent-scans">
                {recent.length === 0 ? (
                  <Card className="rounded-2xl border-dashed border-primary/20 bg-transparent">
                    <CardContent className="flex flex-col items-center gap-2 py-10 text-center">
                      <Sprout className="h-8 w-8 text-muted-foreground/40" />
                      <p className="text-xs text-muted-foreground">
                        No scans yet. Upload or take a plant photo above.
                      </p>
                    </CardContent>
                  </Card>
                ) : (
                  recent.map((s) => (
                    <Link
                      key={s.id}
                      to={`/history?scan=${s.id}`}
                      className="block group"
                      data-testid={`recent-scan-${s.id}`}
                    >
                      <Card className="rounded-2xl border-primary/10 bg-card p-3.5 transition-all hover:border-primary/30 hover:shadow-xs">
                        <div className="flex items-center justify-between gap-3">
                          <div className="min-w-0">
                            <p className="truncate font-serif text-sm font-medium text-foreground group-hover:text-primary transition-colors">
                              {s.plant_name || "Plant"}
                            </p>
                            <p className="font-mono text-[10px] text-muted-foreground mt-0.5">
                              {new Date(s.created_at).toLocaleDateString()} · Health: {s.health_score}/100
                            </p>
                          </div>
                          <Badge
                            className={`rounded-full border text-[10px] font-mono uppercase tracking-wider ${statusColor(
                              s.status
                            )}`}
                          >
                            {s.status}
                          </Badge>
                        </div>
                      </Card>
                    </Link>
                  ))
                )}
              </div>
            </div>

            {/* Photo Guide Tips */}
            <div className="rounded-3xl border border-primary/15 bg-secondary/30 p-6">
              <div className="flex items-center gap-2 font-mono text-[10px] uppercase tracking-[0.2em] text-primary font-semibold">
                <Leaf className="h-3.5 w-3.5 text-accent" />
                <span>Tips for Taking Good Photos</span>
              </div>
              <h4 className="mt-2 font-serif text-base font-medium text-foreground">
                How to get the most accurate results
              </h4>
              <ul className="mt-3 space-y-2 text-xs text-muted-foreground leading-relaxed">
                <li className="flex items-start gap-2">
                  <span className="text-accent font-bold">›</span>
                  <span><strong>Good Daylight:</strong> Take photos in bright morning or diffused daylight so leaves are clearly visible.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-accent font-bold">›</span>
                  <span><strong>Focus on the Spots:</strong> Make sure the camera clearly captures the diseased spots along with some healthy leaf.</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-accent font-bold">›</span>
                  <span><strong>Check Under the Leaf:</strong> Turn the leaf over if tiny pests, webs, or white powder are hiding underneath.</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </Shell>
  );
}
