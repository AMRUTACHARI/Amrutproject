import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Leaf,
  AlertTriangle,
  CheckCircle2,
  Copy,
  Check,
  FileCheck2,
  ShieldCheck,
  AlertCircle,
  Sprout,
  HeartHandshake,
  Volume2,
  VolumeX,
  Printer,
  Maximize2,
  X,
  Sparkles,
} from "lucide-react";
import { toast } from "sonner";

export function statusColor(status) {
  if (status === "Healthy") return "text-accent bg-accent/10 border-accent/20";
  if (status === "Unknown") return "text-muted-foreground bg-muted border-border";
  if (status === "Deficiency") return "text-amber-600 bg-amber-500/10 border-amber-500/20";
  if (status === "Pest Infestation") return "text-rose-600 bg-rose-500/10 border-rose-500/20";
  return "text-[hsl(14_62%_48%)] bg-[hsl(14_62%_48%)]/10 border-[hsl(14_62%_48%)]/20";
}

export function scoreColor(score) {
  if (score >= 80) return "hsl(var(--accent))";
  if (score >= 50) return "hsl(38 78% 54%)";
  return "hsl(14 62% 48%)";
}

export function HealthGauge({ score }) {
  const r = 44;
  const c = 2 * Math.PI * r;
  const offset = c - (score / 100) * c;
  return (
    <div className="relative h-24 w-24 shrink-0" data-testid="health-gauge">
      <svg className="h-full w-full -rotate-90" viewBox="0 0 110 110">
        <circle cx="55" cy="55" r={r} fill="none" stroke="hsl(var(--muted))" strokeWidth="7" />
        <circle
          cx="55"
          cy="55"
          r={r}
          fill="none"
          stroke={scoreColor(score)}
          strokeWidth="7"
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={offset}
          style={{ transition: "stroke-dashoffset 1s cubic-bezier(0.16, 1, 0.3, 1)" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-mono text-xl font-bold tracking-tight text-foreground">{score}</span>
        <span className="font-mono text-[8px] uppercase tracking-widest text-muted-foreground">Health</span>
      </div>
    </div>
  );
}

export function ScanResult({ scan }) {
  const [copied, setCopied] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [appliedRemedies, setAppliedRemedies] = useState(new Set());
  const [lightbox, setLightbox] = useState(false);

  if (!scan) return null;

  const healthy = scan.status === "Healthy";
  const remediesList = Array.isArray(scan.remedies) ? scan.remedies : [];
  const remediesText = remediesList.length
    ? remediesList.map((r, i) => `${i + 1}. ${r}`).join("\n")
    : scan.remedies || "";
  const precautionsText = Array.isArray(scan.precautions)
    ? scan.precautions.map((p, i) => `${i + 1}. ${p}`).join("\n")
    : scan.precautions || "";

  const toggleRemedy = (idx) => {
    setAppliedRemedies((prev) => {
      const next = new Set(prev);
      if (next.has(idx)) next.delete(idx);
      else next.add(idx);
      return next;
    });
  };

  const toggleSpeech = () => {
    if (typeof window === "undefined" || !("speechSynthesis" in window)) {
      toast.info("Audio narration is not supported in this browser.");
      return;
    }
    if (speaking) {
      window.speechSynthesis.cancel();
      setSpeaking(false);
      return;
    }
    const text = `${scan.plant_name || "Plant"} health report. Status: ${scan.status}. Health score: ${scan.health_score} out of 100. Diagnosis: ${scan.diagnosis || ""}. Remedies: ${remediesList.join(". ")}`;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 0.95;
    utterance.onend = () => setSpeaking(false);
    utterance.onerror = () => setSpeaking(false);
    setSpeaking(true);
    window.speechSynthesis.speak(utterance);
  };

  const copyFullReport = () => {
    const text = [
      `FLORAai Plant Health Report`,
      `===========================`,
      `Plant Name: ${scan.plant_name || "Plant"}`,
      `Scientific Name: ${scan.scientific_name || "N/A"}`,
      `Plant Family: ${scan.plant_family || "N/A"}`,
      `Health Status: ${scan.status} (Health Score: ${scan.health_score}/100, Accuracy: ${scan.confidence}%)`,
      ``,
      `[Role & Uses in India]:`,
      `${scan.plant_role || "N/A"}`,
      ``,
      `[About this Plant]:`,
      `${scan.plant_description || "N/A"}`,
      ``,
      `[What We Observed]:`,
      `${scan.diagnosis || "N/A"}`,
      ``,
      `[Why this Happened (Problem & Cause)]:`,
      `${scan.problem_cause || "N/A"}`,
      ``,
      `[Organic Home Remedies]:`,
      remediesText || "None needed.",
      ``,
      `[Conclusion: Simple Steps to Protect this Plant]:`,
      precautionsText || "Maintain regular care and proper watering.",
    ].join("\n");

    navigator.clipboard.writeText(text);
    setCopied(true);
    toast.success("Plant report copied to clipboard.");
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <Card
      className="overflow-hidden rounded-3xl border-primary/20 bg-card shadow-lg animate-fade-up transition-all"
      data-testid="scan-result"
    >
      {/* Header Bar */}
      <div className="border-b border-primary/10 bg-secondary/40 px-4 sm:px-6 py-3 flex flex-wrap items-center justify-between gap-2.5">
        <div className="flex items-center gap-2">
          <FileCheck2 className="h-4 w-4 text-primary shrink-0" />
          <span className="font-mono text-[10px] uppercase tracking-[0.2em] text-primary font-bold">
            PLANT HEALTH REPORT
          </span>
          <span className="rounded-full bg-accent/15 px-2 py-0.5 text-[9px] font-mono font-semibold text-accent uppercase">
            AI Verified
          </span>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <button
            type="button"
            onClick={toggleSpeech}
            className={`inline-flex items-center gap-1 font-mono text-[10px] uppercase tracking-wider transition-colors px-2.5 py-1 rounded-full border ${
              speaking
                ? "bg-accent text-accent-foreground border-accent animate-pulse"
                : "border-primary/20 text-muted-foreground hover:text-primary hover:border-primary/40"
            }`}
            title={speaking ? "Stop narration" : "Listen to audio narration"}
          >
            {speaking ? <VolumeX className="h-3.5 w-3.5" /> : <Volume2 className="h-3.5 w-3.5" />}
            <span>{speaking ? "Listening…" : "Listen"}</span>
          </button>
          <button
            type="button"
            onClick={copyFullReport}
            className="inline-flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-wider text-muted-foreground hover:text-primary transition-colors"
            title="Copy report"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-accent" /> Copied
              </>
            ) : (
              <>
                <Copy className="h-3.5 w-3.5" /> Copy
              </>
            )}
          </button>
          <button
            type="button"
            onClick={() => window.print()}
            className="inline-flex items-center gap-1 font-mono text-[10px] uppercase tracking-wider text-muted-foreground hover:text-primary transition-colors"
            title="Print report"
          >
            <Printer className="h-3.5 w-3.5" /> Print
          </button>
          <span className="font-mono text-[10px] text-muted-foreground border-l border-primary/10 pl-2">
            {new Date(scan.created_at || Date.now()).toLocaleDateString(undefined, {
              month: "short",
              day: "numeric",
              year: "numeric",
            })}
          </span>
        </div>
      </div>

      <CardContent className="p-0">
        <div className="grid gap-0 md:grid-cols-[1fr_1.4fr]">
          {/* Left Column: Plant Photo Frame */}
          <div className="relative min-h-[280px] sm:min-h-[320px] md:min-h-full bg-neutral-950 overflow-hidden flex items-center justify-center group">
            {scan.image_base64 ? (
              <>
                <img
                  src={scan.image_base64}
                  alt={scan.plant_name}
                  className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105 cursor-pointer"
                  onClick={() => setLightbox(true)}
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/20 to-black/30 pointer-events-none" />
                <button
                  type="button"
                  onClick={() => setLightbox(true)}
                  className="absolute right-3 top-3 rounded-full bg-black/60 p-1.5 text-white/80 backdrop-blur-md opacity-0 group-hover:opacity-100 transition-opacity hover:text-white"
                  title="Enlarge photo"
                >
                  <Maximize2 className="h-3.5 w-3.5" />
                </button>
              </>
            ) : (
              <div className="flex flex-col items-center justify-center p-8 text-muted-foreground/60">
                <Sprout className="h-16 w-16 mb-2 stroke-1" />
                <p className="font-serif italic text-sm">Plant photo</p>
              </div>
            )}

            {/* Health Status Pill */}
            <Badge
              className={`absolute left-4 top-4 rounded-full border backdrop-blur-md px-3 py-1 font-mono text-xs uppercase tracking-wider shadow-sm ${statusColor(
                scan.status
              )}`}
              data-testid="scan-status-badge"
            >
              {healthy ? (
                <CheckCircle2 className="mr-1.5 h-3.5 w-3.5 text-accent" />
              ) : (
                <AlertTriangle className="mr-1.5 h-3.5 w-3.5" />
              )}
              <span>{scan.status}</span>
            </Badge>

            {/* Reticle Focus Corners */}
            <div className="absolute inset-4 sm:inset-5 pointer-events-none border border-white/20 rounded-2xl">
              <div className="absolute -top-1 -left-1 h-3.5 w-3.5 border-t-2 border-l-2 border-accent" />
              <div className="absolute -top-1 -right-1 h-3.5 w-3.5 border-t-2 border-r-2 border-accent" />
              <div className="absolute -bottom-1 -left-1 h-3.5 w-3.5 border-b-2 border-l-2 border-accent" />
              <div className="absolute -bottom-1 -right-1 h-3.5 w-3.5 border-b-2 border-r-2 border-accent" />
            </div>

            {/* Photo Bottom Tagging */}
            <div className="absolute bottom-4 left-4 sm:left-5 right-4 sm:right-5 text-white pointer-events-none">
              <p className="font-serif italic text-sm text-white/95 drop-shadow-md">
                {scan.scientific_name || scan.plant_name}
              </p>
              <div className="flex items-center justify-between mt-1 text-[10px] font-mono text-white/75">
                <span>Confidence: {scan.confidence}%</span>
                {scan.plant_family && <span className="text-accent">{scan.plant_family}</span>}
              </div>
            </div>
          </div>

          {/* Right Column: Plant Information & Health Report */}
          <div className="p-5 sm:p-8 flex flex-col justify-between space-y-5 sm:space-y-6">
            <div>
              {/* Plant Names & Family */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-primary/10 pb-5">
                <div className="min-w-0 flex-1">
                  {scan.plant_family && (
                    <div className="inline-flex items-center gap-1.5 rounded-full border border-primary/20 bg-primary/5 px-3 py-0.5 mb-2 font-mono text-[10px] uppercase tracking-wider text-primary">
                      <Sprout className="h-3 w-3 text-accent" />
                      <span>Family: {scan.plant_family}</span>
                    </div>
                  )}

                  <h3
                    className="font-serif text-2xl sm:text-3xl font-medium tracking-tight text-foreground break-words"
                    data-testid="scan-plant-name"
                  >
                    {scan.plant_name || "Your Plant"}
                  </h3>

                  {scan.scientific_name && (
                    <p className="font-serif italic text-sm text-muted-foreground mt-0.5">
                      Scientific Name: {scan.scientific_name}
                    </p>
                  )}
                </div>

                <div className="flex flex-col items-center">
                  <HealthGauge score={scan.health_score} />
                  <span className="mt-1 font-mono text-[9px] uppercase tracking-wider text-muted-foreground">
                    {scan.health_score >= 80 ? "Optimal Vigor" : scan.health_score >= 50 ? "Moderate Stress" : "Critical Care"}
                  </span>
                </div>
              </div>

              {/* Plant Role & Uses in India */}
              {scan.plant_role && (
                <div className="mt-5 rounded-2xl border border-primary/15 bg-primary/5 p-4" data-testid="scan-plant-role">
                  <div className="flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.2em] text-primary font-bold">
                    <HeartHandshake className="h-3.5 w-3.5 text-accent" />
                    <span>Role & Uses in India (Why this plant is valuable)</span>
                  </div>
                  <p className="mt-2 text-xs sm:text-sm leading-relaxed text-foreground/90 font-serif">
                    {scan.plant_role}
                  </p>
                </div>
              )}

              {/* About this Plant Species */}
              {scan.plant_description && (
                <div className="mt-4 rounded-2xl border border-primary/10 bg-secondary/30 p-4" data-testid="scan-plant-description">
                  <div className="flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.2em] text-foreground/70 font-semibold">
                    <Leaf className="h-3.5 w-3.5 text-accent" />
                    <span>About this Plant</span>
                  </div>
                  <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                    {scan.plant_description}
                  </p>
                </div>
              )}

              {/* What We Observed */}
              <div className="mt-4 rounded-2xl border border-primary/10 bg-secondary/20 p-4">
                <div className="flex items-center justify-between">
                  <span className="font-mono text-[10px] uppercase tracking-[0.2em] text-primary font-semibold">
                    What We Observed in this Photo
                  </span>
                  <span className="font-mono text-[10px] text-muted-foreground font-mono">
                    Confidence: {scan.confidence}%
                  </span>
                </div>
                <p className="mt-2 text-xs sm:text-sm leading-relaxed text-foreground/90">
                  {scan.diagnosis}
                </p>

                {/* Visible symptoms / signs */}
                {scan.issues?.length > 0 && (
                  <div className="mt-3 flex flex-wrap gap-1.5">
                    {scan.issues.map((i) => (
                      <span
                        key={i}
                        className="rounded-full border border-primary/15 bg-background px-2.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-primary shadow-xs"
                      >
                        {i}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* What Happened (Cause of the Problem) */}
              {scan.problem_cause && (
                <div className="mt-4 rounded-2xl border border-[hsl(14_62%_48%)]/20 bg-[hsl(14_62%_48%)]/5 p-4" data-testid="scan-problem-cause">
                  <div className="flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.2em] text-[hsl(14_62%_48%)] font-bold">
                    <AlertCircle className="h-3.5 w-3.5" />
                    <span>What Happened to this Plant (Why it got sick)</span>
                  </div>
                  <p className="mt-2 text-xs leading-relaxed text-foreground/85">
                    {scan.problem_cause}
                  </p>
                </div>
              )}

              {/* Simple Organic Remedies with Interactive Checklist */}
              {remediesList.length > 0 && (
                <div className="mt-5 border-t border-primary/10 pt-4" data-testid="scan-remedies">
                  <div className="flex items-center justify-between">
                    <p className="flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.2em] text-primary font-bold">
                      <Leaf className="h-3.5 w-3.5 text-accent" />
                      Simple Home & Organic Remedies
                    </p>
                    {appliedRemedies.size > 0 && (
                      <span className="rounded-full bg-accent/20 px-2.5 py-0.5 font-mono text-[10px] font-bold text-accent">
                        {appliedRemedies.size} of {remediesList.length} applied
                      </span>
                    )}
                  </div>
                  <div className="mt-2.5 space-y-2">
                    {remediesList.map((r, idx) => {
                      const isDone = appliedRemedies.has(idx);
                      return (
                        <div
                          key={idx}
                          onClick={() => toggleRemedy(idx)}
                          className={`flex items-start gap-2.5 rounded-xl border p-2.5 text-xs transition-all cursor-pointer ${
                            isDone
                              ? "border-accent/40 bg-accent/10 text-foreground"
                              : "border-primary/10 bg-background/50 hover:bg-secondary/40 text-foreground/90"
                          }`}
                        >
                          <span
                            className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full font-mono text-[10px] font-bold transition-colors ${
                              isDone ? "bg-accent text-accent-foreground" : "bg-primary/10 text-primary"
                            }`}
                          >
                            {isDone ? "✓" : idx + 1}
                          </span>
                          <span className={`flex-1 leading-snug ${isDone ? "line-through opacity-70" : ""}`}>
                            {r}
                          </span>
                          <span className="font-mono text-[9px] uppercase tracking-wider text-muted-foreground shrink-0">
                            {isDone ? "Applied" : "Tap to mark done"}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}

              {/* Conclusion: Precautions to Keep Plant Safe */}
              <div
                className="mt-6 rounded-2xl border-2 border-accent/40 bg-accent/5 p-4 sm:p-5"
                data-testid="scan-precautions-conclusion"
              >
                <div className="flex items-center gap-2">
                  <ShieldCheck className="h-4 w-4 text-accent" />
                  <span className="font-mono text-[11px] uppercase tracking-[0.2em] text-accent font-bold">
                    CONCLUSION: SIMPLE STEPS TO KEEP YOUR PLANT SAFE & HEALTHY
                  </span>
                </div>
                <p className="mt-1 text-xs text-muted-foreground">
                  Follow these easy everyday tips to protect your plant from future sickness and pests:
                </p>

                <div className="mt-3 space-y-2">
                  {scan.precautions && scan.precautions.length > 0 ? (
                    scan.precautions.map((prec, idx) => (
                      <div
                        key={idx}
                        className="flex items-start gap-2.5 text-xs text-foreground/90 leading-snug bg-background/60 rounded-xl p-2.5 border border-primary/10"
                      >
                        <span className="flex h-4 w-4 shrink-0 items-center justify-center rounded-full bg-accent/20 font-mono text-[9px] font-bold text-accent">
                          ✓
                        </span>
                        <span>{prec}</span>
                      </div>
                    ))
                  ) : (
                    <div className="flex items-start gap-2 text-xs text-muted-foreground italic">
                      <span>• Water at the roots, make sure water does not stand in the pot, and give good sunlight.</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Footer */}
            <div className="border-t border-primary/10 pt-3 flex flex-col sm:flex-row items-center justify-between gap-1 text-[10px] text-muted-foreground font-mono">
              <span className="flex items-center gap-1">
                <Sparkles className="h-3 w-3 text-accent" /> FLORAai Smart Botanical Diagnostic
              </span>
              <span>100% Natural Organic Remedies</span>
            </div>
          </div>
        </div>
      </CardContent>

      {/* Lightbox inspection dialog */}
      {lightbox && scan.image_base64 && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm animate-fade-in"
          onClick={() => setLightbox(false)}
        >
          <div className="relative max-h-[90vh] max-w-3xl overflow-hidden rounded-2xl bg-neutral-950 p-2" onClick={(e) => e.stopPropagation()}>
            <img src={scan.image_base64} alt={scan.plant_name} className="max-h-[80vh] w-auto rounded-xl object-contain mx-auto" />
            <div className="mt-2 flex items-center justify-between px-2 text-white font-mono text-xs">
              <span>{scan.plant_name} ({scan.status})</span>
              <button
                type="button"
                onClick={() => setLightbox(false)}
                className="rounded-full bg-white/20 px-3 py-1 text-[11px] hover:bg-white/30"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </Card>
  );
}
