"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { site, telHref, whatsappHref } from "@/config/site";
import { budgets, projectTypes, timeframes, UPLOAD_LIMITS, workOptions } from "@/lib/leads/options";
import { ArrowIcon } from "@/components/ui/Button";
import { CheckIcon, PhoneIcon, UploadIcon, WhatsAppIcon } from "@/components/ui/Icons";

type Status = "idle" | "sending" | "success" | "error";
type Errors = Record<string, string>;

/**
 * Zweistufiges Anfrageformular:
 *  1) Pflichtangaben (Kontakt, Ort, Objektart, Leistungen) – schnell ausfüllbar
 *  2) optionale Details (Fläche, Zeitraum, Budget, Nachricht, Fotos)
 * Fotos werden im Browser auf max. 1600 px / JPEG verkleinert → schneller Upload auch mobil.
 */
export function LeadForm() {
  const [step, setStep] = useState<1 | 2>(1);
  const [status, setStatus] = useState<Status>("idle");
  const [errors, setErrors] = useState<Errors>({});
  const [serverError, setServerError] = useState("");
  const [photos, setPhotos] = useState<File[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const formRef = useRef<HTMLFormElement>(null);
  const startedAt = useRef(0);

  useEffect(() => {
    startedAt.current = Date.now();
    // Vorauswahl über ?leistung=… (Links von den Leistungsseiten); Seite bleibt statisch
    const pre = new URLSearchParams(window.location.search).get("leistung");
    if (pre && (workOptions as readonly string[]).includes(pre)) setSelected([pre]);
  }, []);

  function validateStep1(fd: FormData): Errors {
    const e: Errors = {};
    if (String(fd.get("name") ?? "").trim().length < 2) e.name = "Bitte geben Sie Ihren Namen an.";
    if (!/^[+()\d\s/-]{6,}$/.test(String(fd.get("phone") ?? "").trim())) e.phone = "Bitte geben Sie eine gültige Telefonnummer an.";
    const email = String(fd.get("email") ?? "").trim();
    if (email && !/^\S+@\S+\.\S+$/.test(email)) e.email = "Bitte prüfen Sie die E-Mail-Adresse.";
    if (String(fd.get("location") ?? "").trim().length < 2) e.location = "Bitte geben Sie den Ort an.";
    if (!fd.get("projectType")) e.projectType = "Bitte wählen Sie die Objektart.";
    if (selected.length === 0) e.services = "Bitte wählen Sie mindestens eine Leistung.";
    return e;
  }

  function next() {
    const fd = new FormData(formRef.current!);
    const e = validateStep1(fd);
    setErrors(e);
    if (Object.keys(e).length) {
      focusFirstError(e);
      return;
    }
    setStep(2);
    requestAnimationFrame(() => formRef.current?.scrollIntoView({ behavior: "smooth", block: "start" }));
  }

  async function onPhotos(files: FileList | null) {
    if (!files) return;
    const list = Array.from(files).slice(0, UPLOAD_LIMITS.maxFiles - photos.length);
    const compressed = await Promise.all(list.map((f) => compressImage(f).catch(() => f)));
    setPhotos((p) => [...p, ...compressed].slice(0, UPLOAD_LIMITS.maxFiles));
  }

  async function onSubmit(ev: React.FormEvent<HTMLFormElement>) {
    ev.preventDefault();
    const fd = new FormData(ev.currentTarget);
    const e = validateStep1(fd);
    if (!fd.get("consent")) e.consent = "Bitte stimmen Sie der Verarbeitung Ihrer Daten zu.";
    setErrors(e);
    if (Object.keys(e).length) {
      if (e.consent && Object.keys(e).length === 1) focusFirstError(e);
      else setStep(1);
      return;
    }

    fd.delete("services");
    selected.forEach((s) => fd.append("services", s));
    fd.delete("photos");
    photos.forEach((p) => fd.append("photos", p, p.name));
    fd.set("startedAt", String(startedAt.current));
    fd.set("sourcePage", window.location.pathname);
    fd.set("utm", JSON.stringify(readUtm()));

    setStatus("sending");
    setServerError("");
    try {
      const res = await fetch("/api/lead", { method: "POST", body: fd });
      const data = (await res.json().catch(() => ({}))) as { ok?: boolean; error?: string; fieldErrors?: Errors };
      if (res.ok && data.ok) {
        setStatus("success");
        formRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
        return;
      }
      if (data.fieldErrors) {
        setErrors(data.fieldErrors);
        if (["name", "phone", "email", "location", "projectType", "services"].some((k) => k in data.fieldErrors!)) setStep(1);
      }
      setServerError(data.error ?? "Bitte prüfen Sie Ihre Angaben.");
      setStatus("error");
    } catch {
      setServerError("Keine Verbindung. Bitte versuchen Sie es erneut oder rufen Sie uns an.");
      setStatus("error");
    }
  }

  if (status === "success") {
    return (
      <div className="bg-ink p-8 text-paper sm:p-12" role="status" aria-live="polite">
        <span className="flex size-12 items-center justify-center bg-ziegel">
          <CheckIcon className="size-6" />
        </span>
        <h3 className="text-h2 mt-8 font-semibold">Vielen Dank für Ihre Anfrage.</h3>
        <p className="mt-4 max-w-lg text-lg text-paper/70">
          Wir haben Ihre Angaben erhalten und melden uns zeitnah bei Ihnen. Sie erhalten zusätzlich eine Bestätigung per
          E-Mail, sofern Sie eine Adresse angegeben haben.
        </p>
        <p className="mt-8 text-paper/60">Eilt es? Rufen Sie uns direkt an:</p>
        <a href={telHref} className="mt-2 inline-flex items-center gap-3 text-xl font-semibold">
          <PhoneIcon /> {site.contact.phone}
        </a>
      </div>
    );
  }

  return (
    <form ref={formRef} onSubmit={onSubmit} noValidate className="scroll-mt-28" aria-describedby="form-hint">
      {/* Fortschritt */}
      <div className="mb-10 flex items-center gap-4 text-sm" aria-hidden>
        <StepDot active={step === 1} done={step === 2} label="Kontakt & Projekt" n={1} />
        <span className="h-px flex-1 bg-beton-100" />
        <StepDot active={step === 2} done={false} label="Details (optional)" n={2} />
      </div>
      <p id="form-hint" className="sr-only">
        Schritt {step} von 2. Felder mit Stern sind Pflichtfelder.
      </p>

      {/* Honeypot – für Menschen unsichtbar */}
      <div className="absolute -left-[9999px] h-0 w-0 overflow-hidden" aria-hidden>
        <label>
          Website <input type="text" name="website" tabIndex={-1} autoComplete="off" />
        </label>
      </div>

      <fieldset hidden={step !== 1} className="grid gap-6 sm:grid-cols-2">
        <legend className="sr-only">Kontakt und Projekt</legend>
        <Field label="Name" name="name" required autoComplete="name" error={errors.name} />
        <Field label="Telefon" name="phone" type="tel" required autoComplete="tel" inputMode="tel" error={errors.phone} />
        <Field label="E-Mail" name="email" type="email" autoComplete="email" error={errors.email} hint="Für Ihre Bestätigung" />
        <Field label="Ort des Projekts" name="location" required autoComplete="address-level2" error={errors.location} placeholder="z. B. Heide" />

        <div className="sm:col-span-2">
          <p className="mb-3 text-sm font-medium">
            Objektart <span className="text-ziegel">*</span>
          </p>
          <div className="grid grid-cols-2 gap-2 sm:grid-cols-4" role="radiogroup" aria-invalid={!!errors.projectType}>
            {projectTypes.map((t) => (
              <label key={t} className="relative cursor-pointer">
                <input type="radio" name="projectType" value={t} className="peer sr-only" />
                <span className="flex min-h-12 items-center justify-center border border-ink/15 px-3 text-[0.95rem] transition-colors peer-checked:border-ink peer-checked:bg-ink peer-checked:text-paper peer-focus-visible:outline-2 peer-focus-visible:outline-ziegel hover:border-ink/40">
                  {t}
                </span>
              </label>
            ))}
          </div>
          <FieldError id="projectType" msg={errors.projectType} />
        </div>

        <div className="sm:col-span-2">
          <p className="mb-3 text-sm font-medium">
            Welche Arbeiten? <span className="text-ziegel">*</span>
          </p>
          <div className="flex flex-wrap gap-2">
            {workOptions.map((w) => {
              const on = selected.includes(w);
              return (
                <button
                  key={w}
                  type="button"
                  aria-pressed={on}
                  onClick={() => setSelected((s) => (on ? s.filter((x) => x !== w) : [...s, w]))}
                  className={`min-h-11 border px-4 text-[0.92rem] transition-colors ${
                    on ? "border-ziegel bg-ziegel text-paper" : "border-ink/15 hover:border-ink/40"
                  }`}
                >
                  {w}
                </button>
              );
            })}
          </div>
          <FieldError id="services" msg={errors.services} />
        </div>

        <div className="sm:col-span-2">
          <button type="button" onClick={next} className="group inline-flex min-h-14 w-full items-center justify-center gap-3 bg-ink px-8 font-medium text-paper hover:bg-anthrazit sm:w-auto">
            Weiter zu den Details
            <ArrowIcon className="size-4 transition-transform group-hover:translate-x-1" />
          </button>
        </div>
      </fieldset>

      <fieldset hidden={step !== 2} className="grid gap-6 sm:grid-cols-2">
        <legend className="sr-only">Projektdetails</legend>
        <Field label="Fläche (ca. m²)" name="area" inputMode="numeric" placeholder="z. B. 85" />
        <Select label="Gewünschter Zeitraum" name="timeframe" options={timeframes} />
        <Select label="Budget (optional)" name="budget" options={budgets} className="sm:col-span-2" />
        <div className="sm:col-span-2">
          <label htmlFor="message" className="mb-2 block text-sm font-medium">
            Nachricht
          </label>
          <textarea
            id="message"
            name="message"
            rows={5}
            maxLength={3000}
            placeholder="Was soll gemacht werden? Gibt es Besonderheiten?"
            className="w-full border border-ink/15 bg-paper px-4 py-3 text-base outline-none placeholder:text-beton-300 focus:border-ink"
          />
        </div>

        <div className="sm:col-span-2">
          <p className="mb-2 text-sm font-medium">Fotos hochladen (optional)</p>
          <label className="flex min-h-28 cursor-pointer flex-col items-center justify-center gap-2 border border-dashed border-ink/25 px-4 text-center text-sm text-anthrazit/70 hover:border-ink">
            <UploadIcon />
            <span>
              Bis zu {UPLOAD_LIMITS.maxFiles} Fotos – <span className="underline">auswählen</span> oder Kamera nutzen
            </span>
            <input
              type="file"
              name="photos"
              accept="image/*"
              multiple
              className="sr-only"
              onChange={(e) => {
                onPhotos(e.target.files);
                e.target.value = "";
              }}
            />
          </label>
          {photos.length > 0 && (
            <ul className="mt-3 flex flex-wrap gap-2 text-sm">
              {photos.map((p, i) => (
                <li key={p.name + i} className="flex items-center gap-2 bg-paper-2 py-1.5 pr-1.5 pl-3">
                  <span className="max-w-40 truncate">{p.name}</span>
                  <button type="button" className="px-2 text-beton-500 hover:text-ink" onClick={() => setPhotos((ph) => ph.filter((_, j) => j !== i))} aria-label={`${p.name} entfernen`}>
                    ×
                  </button>
                </li>
              ))}
            </ul>
          )}
          <FieldError id="photos" msg={errors.photos} />
        </div>

        <div className="sm:col-span-2">
          <label className="flex cursor-pointer gap-3 text-sm leading-relaxed text-anthrazit/80">
            <input type="checkbox" name="consent" className="mt-1 size-5 shrink-0 accent-ziegel" aria-invalid={!!errors.consent} />
            <span>
              Ich bin einverstanden, dass meine Angaben und Fotos zur Bearbeitung meiner Anfrage gespeichert und verarbeitet
              werden. Details in der{" "}
              <Link href="/datenschutz" className="underline">
                Datenschutzerklärung
              </Link>
              . <span className="text-ziegel">*</span>
            </span>
          </label>
          <FieldError id="consent" msg={errors.consent} />
        </div>

        {serverError && (
          <p className="border-l-2 border-ziegel bg-paper-2 p-4 text-sm sm:col-span-2" role="alert">
            {serverError}{" "}
            <a href={whatsappHref} className="inline-flex items-center gap-1 underline" target="_blank" rel="noopener">
              <WhatsAppIcon className="size-4" /> WhatsApp
            </a>
          </p>
        )}

        <div className="flex flex-col-reverse gap-3 sm:col-span-2 sm:flex-row sm:items-center sm:justify-between">
          <button type="button" onClick={() => setStep(1)} className="min-h-12 text-sm text-anthrazit/70 underline-offset-4 hover:underline">
            ← Zurück
          </button>
          <button
            type="submit"
            disabled={status === "sending"}
            className="group inline-flex min-h-14 items-center justify-center gap-3 bg-ziegel px-8 font-semibold text-paper hover:bg-ziegel-dark disabled:opacity-60"
          >
            {status === "sending" ? "Wird gesendet …" : "Projekt anfragen"}
            <ArrowIcon className="size-4 transition-transform group-hover:translate-x-1" />
          </button>
        </div>
      </fieldset>
    </form>
  );
}

function StepDot({ active, done, label, n }: { active: boolean; done: boolean; label: string; n: number }) {
  return (
    <span className={`flex items-center gap-3 ${active || done ? "text-ink" : "text-beton-500"}`}>
      <span className={`flex size-8 items-center justify-center text-xs font-semibold ${active ? "bg-ink text-paper" : done ? "bg-ziegel text-paper" : "border border-beton-300"}`}>
        {done ? <CheckIcon /> : n}
      </span>
      <span className="hidden sm:inline">{label}</span>
    </span>
  );
}

type FieldProps = React.InputHTMLAttributes<HTMLInputElement> & { label: string; name: string; error?: string; hint?: string };

function Field({ label, name, error, hint, required, className = "", ...rest }: FieldProps) {
  return (
    <div className={className}>
      <label htmlFor={name} className="mb-2 flex items-baseline justify-between text-sm font-medium">
        <span>
          {label} {required && <span className="text-ziegel">*</span>}
        </span>
        {hint && <span className="text-xs font-normal text-beton-500">{hint}</span>}
      </label>
      <input
        id={name}
        name={name}
        required={required}
        aria-invalid={!!error}
        aria-describedby={error ? `${name}-error` : undefined}
        className={`min-h-13 w-full border bg-paper px-4 text-base outline-none placeholder:text-beton-300 focus:border-ink ${error ? "border-ziegel" : "border-ink/15"}`}
        {...rest}
      />
      <FieldError id={name} msg={error} />
    </div>
  );
}

function Select({ label, name, options, className = "" }: { label: string; name: string; options: readonly string[]; className?: string }) {
  return (
    <div className={className}>
      <label htmlFor={name} className="mb-2 block text-sm font-medium">
        {label}
      </label>
      <select id={name} name={name} defaultValue="" className="min-h-13 w-full border border-ink/15 bg-paper px-4 text-base outline-none focus:border-ink">
        <option value="">Bitte wählen</option>
        {options.map((o) => (
          <option key={o} value={o}>
            {o}
          </option>
        ))}
      </select>
    </div>
  );
}

function FieldError({ id, msg }: { id: string; msg?: string }) {
  if (!msg) return null;
  return (
    <p id={`${id}-error`} className="mt-2 text-sm text-ziegel" role="alert">
      {msg}
    </p>
  );
}

function focusFirstError(e: Errors) {
  const first = Object.keys(e)[0];
  if (!first) return;
  const el = document.getElementById(first) ?? document.querySelector<HTMLElement>(`[name="${first}"]`);
  el?.focus();
}

function readUtm(): Record<string, string> {
  const params = new URLSearchParams(window.location.search);
  const out: Record<string, string> = {};
  for (const k of ["utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid"]) {
    const v = params.get(k);
    if (v) out[k] = v;
  }
  return out;
}

/** Verkleinert Fotos clientseitig (max. 1600 px, JPEG 0.82). HEIC fällt auf das Original zurück. */
async function compressImage(file: File): Promise<File> {
  if (!file.type.startsWith("image/") || file.type.includes("heic") || file.type.includes("heif")) return file;
  const bitmap = await createImageBitmap(file);
  const scale = Math.min(1, 1600 / Math.max(bitmap.width, bitmap.height));
  const canvas = document.createElement("canvas");
  canvas.width = Math.round(bitmap.width * scale);
  canvas.height = Math.round(bitmap.height * scale);
  canvas.getContext("2d")!.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
  const blob = await new Promise<Blob | null>((r) => canvas.toBlob(r, "image/jpeg", 0.82));
  if (!blob) return file;
  return new File([blob], file.name.replace(/\.\w+$/, "") + ".jpg", { type: "image/jpeg" });
}
