import { NextResponse } from "next/server";
import { buildLeadPayload, getLeadSink } from "@/lib/leads";
import { UPLOAD_LIMITS } from "@/lib/leads/options";
import { leadInputSchema } from "@/lib/leads/schema";
import type { LeadAttachment } from "@/lib/leads/types";

export const runtime = "nodejs";

// Best-effort-Drosselung pro Instanz (für echte Last: Upstash/Redis o. Ä.)
const hits = new Map<string, number[]>();
function rateLimited(ip: string) {
  const now = Date.now();
  const recent = (hits.get(ip) ?? []).filter((t) => now - t < 10 * 60_000);
  recent.push(now);
  hits.set(ip, recent);
  return recent.length > 5;
}

export async function POST(req: Request) {
  const ip = req.headers.get("x-forwarded-for")?.split(",")[0]?.trim() ?? "unknown";
  if (rateLimited(ip)) {
    return NextResponse.json({ ok: false, error: "Zu viele Anfragen. Bitte versuchen Sie es später erneut." }, { status: 429 });
  }

  let form: FormData;
  try {
    form = await req.formData();
  } catch {
    return NextResponse.json({ ok: false, error: "Ungültige Anfrage." }, { status: 400 });
  }

  // Spam-Schutz: Honeypot + Mindest-Ausfüllzeit (3 s). Bots erhalten ein scheinbares OK.
  const startedAt = Number(form.get("startedAt") ?? 0);
  if (form.get("website") || !startedAt || Date.now() - startedAt < 3000) {
    return NextResponse.json({ ok: true });
  }

  const parsed = leadInputSchema.safeParse({
    name: str(form.get("name")),
    phone: str(form.get("phone")),
    email: str(form.get("email")),
    location: str(form.get("location")),
    projectType: str(form.get("projectType")),
    services: form.getAll("services"),
    area: str(form.get("area")),
    timeframe: str(form.get("timeframe")),
    budget: str(form.get("budget")),
    message: str(form.get("message")),
    consent: form.get("consent") === "on" || form.get("consent") === "true",
    sourcePage: str(form.get("sourcePage")),
    utm: safeJson(form.get("utm")),
  });

  if (!parsed.success) {
    const fieldErrors: Record<string, string> = {};
    for (const issue of parsed.error.issues) {
      const key = String(issue.path[0] ?? "form");
      fieldErrors[key] ??= issue.message;
    }
    return NextResponse.json({ ok: false, fieldErrors }, { status: 422 });
  }

  const files = form.getAll("photos").filter((f): f is File => f instanceof File && f.size > 0);
  const total = files.reduce((n, f) => n + f.size, 0);
  if (
    files.length > UPLOAD_LIMITS.maxFiles ||
    total > UPLOAD_LIMITS.maxTotalBytes ||
    files.some((f) => f.size > UPLOAD_LIMITS.maxFileBytes || !UPLOAD_LIMITS.accept.includes(f.type))
  ) {
    return NextResponse.json(
      { ok: false, fieldErrors: { photos: "Bitte maximal 6 Fotos (JPG, PNG, WebP) hochladen." } },
      { status: 422 },
    );
  }

  const attachments: LeadAttachment[] = files.map((file, i) => ({ field: `file_${i}`, file }));
  const payload = buildLeadPayload(parsed.data, attachments, { userAgent: req.headers.get("user-agent") ?? "" });

  try {
    await getLeadSink().send(payload, attachments);
  } catch (err) {
    console.error("[lead] Weiterleitung fehlgeschlagen", payload.lead_id, err);
    return NextResponse.json(
      { ok: false, error: "Ihre Anfrage konnte gerade nicht übermittelt werden. Bitte rufen Sie uns an oder schreiben Sie uns per WhatsApp." },
      { status: 502 },
    );
  }

  return NextResponse.json({ ok: true, leadId: payload.lead_id });
}

const str = (v: FormDataEntryValue | null) => (typeof v === "string" ? v : "");

function safeJson(v: FormDataEntryValue | null): Record<string, string> {
  if (typeof v !== "string" || !v) return {};
  try {
    const o = JSON.parse(v);
    return o && typeof o === "object" ? o : {};
  } catch {
    return {};
  }
}
