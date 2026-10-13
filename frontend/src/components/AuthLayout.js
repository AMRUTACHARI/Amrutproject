import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Sprout, Eye, EyeOff } from "lucide-react";
import { Input } from "@/components/ui/input";

const FACTS = [
  "Cardamom (Elettaria cardamomum) is known as the “Queen of Spices” and flourishes in the shaded mist of the Western Ghats.",
  "Turmeric (Curcuma longa) contains curcumin, a potent natural polyphenol with proven antifungal and immune properties.",
  "Black pepper vines (Piper nigrum) are ancient tropical climbers native to Kerala's Malabar rainforests.",
  "Curry leaf (Murraya koenigii) produces natural carbazole alkaloids that deter destructive psyllid bugs.",
  "Coconut palms (Cocos nucifera) require balanced potassium and magnesium to withstand monsoonal bud rot.",
  "Hibiscus (Hibiscus rosa-sinensis) thrives on gentle acidic loam with morning sun and organic neem sprays.",
];

export function AuthLayout({ title, subtitle, children, footer, testid }) {
  const fact = FACTS[Math.floor(Math.random() * FACTS.length)];

  return (
    <div className="flex min-h-screen bg-background botanical-parchment" data-testid={testid}>
      <div className="relative hidden w-1/2 overflow-hidden lg:block">
        <img
          src="https://images.unsplash.com/photo-1518531933037-91b2f5f229cc?crop=entropy&cs=srgb&fm=jpg&q=85&w=1400"
          alt="Healthy plant leaves"
          className="absolute inset-0 h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-[#071E07] via-[#0D330E]/75 to-[#2D531A]/40" />

        <div className="relative z-10 flex h-full flex-col justify-between p-12 text-white">
          <Link to="/" className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl transition-transform duration-300 hover:scale-105">
              <img src="/logo.svg" alt="" className="h-full w-full object-contain drop-shadow-sm" />
            </div>
            <div>
              <span className="font-serif text-2xl font-bold tracking-tight text-white">
                FLORA<span className="text-[#B7C693]">ai</span>
              </span>
              <p className="font-mono text-[9px] uppercase tracking-[0.25em] text-white/70">
                Plant Doctor & Care
              </p>
            </div>
          </Link>

          <div className="max-w-md">
            <span className="inline-flex items-center gap-1.5 rounded-full border border-white/20 bg-white/10 px-3 py-1 font-mono text-[10px] uppercase tracking-wider text-[#B7C693] backdrop-blur-sm">
              <Sprout className="h-3 w-3" />
              <span>Smart Care for Indian Plants</span>
            </span>
            <h2 className="mt-4 font-serif text-3xl sm:text-4xl font-normal leading-tight text-white">
              Keep your home garden and crops healthy.
            </h2>
            <p className="mt-3 text-sm text-white/75 leading-relaxed">
              Instant AI plant health checks and simple organic remedies for coconut palms, mango trees,
              courtyard flowers, kitchen spices, and medicinal plants.
            </p>

            <div className="mt-8 rounded-2xl border border-white/15 bg-black/25 p-5 backdrop-blur-md">
              <p className="font-mono text-[10px] uppercase tracking-[0.2em] text-[#B7C693]">
                Helpful Plant Fact
              </p>
              <p className="mt-2 text-xs text-white/90 leading-relaxed italic">{fact}</p>
            </div>
          </div>
        </div>
      </div>

      <div className="flex w-full items-center justify-center px-6 py-12 lg:w-1/2">
        <div className="w-full max-w-md animate-fade-up">
          <Link to="/" className="mb-8 flex items-center gap-3 lg:hidden">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl">
              <img src="/logo.svg" alt="" className="h-full w-full object-contain" />
            </div>
            <span className="font-serif text-xl font-bold tracking-tight text-foreground">
              FLORA<span className="text-accent">ai</span>
            </span>
          </Link>

          <h1 className="font-serif text-3xl font-medium tracking-tight text-foreground sm:text-4xl">
            {title}
          </h1>
          {subtitle && (
            <p className="mt-2 text-sm text-muted-foreground leading-relaxed">{subtitle}</p>
          )}

          <div className="mt-8">{children}</div>

          {footer && (
            <div className="mt-8 border-t border-primary/10 pt-6 text-center text-xs text-muted-foreground">
              {footer}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export function PasswordInput({ id, value, onChange, placeholder, testid, autoComplete, ...props }) {
  const [show, setShow] = useState(false);
  return (
    <div className="relative">
      <Input
        id={id}
        type={show ? "text" : "password"}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        autoComplete={autoComplete}
        data-testid={testid}
        className="pr-10"
        {...props}
      />
      <button
        type="button"
        onClick={() => setShow((s) => !s)}
        aria-label={show ? "Hide password" : "Show password"}
        data-testid={`${testid}-toggle`}
        className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground transition-colors hover:text-foreground"
      >
        {show ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
      </button>
    </div>
  );
}

export function PasswordStrength({ password }) {
  if (!password) return null;
  const checks = [
    { label: "8+ characters", ok: password.length >= 8 },
    { label: "Uppercase letter", ok: /[A-Z]/.test(password) },
    { label: "Lowercase letter", ok: /[a-z]/.test(password) },
    { label: "Number", ok: /\d/.test(password) },
    { label: "Special character", ok: /[^A-Za-z0-9]/.test(password) },
  ];
  const score = checks.filter((c) => c.ok).length;
  const color = score <= 2 ? "bg-destructive" : score <= 4 ? "bg-[hsl(38_78%_56%)]" : "bg-primary";
  const label = score <= 2 ? "Weak" : score <= 4 ? "Good" : "Strong";

  return (
    <div className="space-y-2" data-testid="password-strength">
      <div className="flex items-center justify-between">
        <div className="h-1.5 w-full overflow-hidden rounded-full bg-muted">
          <div className={`h-full rounded-full transition-all duration-300 ${color}`} style={{ width: `${(score / 5) * 100}%` }} />
        </div>
        <span className="ml-3 font-mono text-[11px] uppercase tracking-wider text-muted-foreground">{label}</span>
      </div>
      <ul className="grid grid-cols-2 gap-x-3 gap-y-1">
        {checks.map((c) => (
          <li key={c.label} className={`flex items-center gap-1.5 text-[11px] ${c.ok ? "text-primary" : "text-muted-foreground"}`}>
            <span className={`inline-block h-1.5 w-1.5 rounded-full ${c.ok ? "bg-primary" : "bg-muted-foreground/40"}`} />
            {c.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
