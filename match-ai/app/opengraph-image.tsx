import { ImageResponse } from "next/og";
import { brand } from "@/lib/config/brand";
import { getMessages } from "@/lib/i18n";

export const alt = `${brand.name} — AI match analysis from a screenshot`;
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default function OpengraphImage() {
  const m = getMessages();
  return new ImageResponse(
    (
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
          padding: 72,
          background:
            "radial-gradient(70% 70% at 50% 0%, rgba(139,147,255,0.35), rgba(7,8,12,0) 70%), #07080c",
          color: "#eef0f5",
          fontFamily: "sans-serif",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 18 }}>
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: 16,
              border: "2px solid rgba(165,171,255,0.6)",
              background: "#0d0f15",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 30,
              fontWeight: 700,
              color: "#a5abff",
            }}
          >
            M
          </div>
          <div style={{ fontSize: 30, fontWeight: 600, letterSpacing: 3 }}>{brand.name}</div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", gap: 24 }}>
          <div style={{ fontSize: 80, fontWeight: 700, letterSpacing: -2, lineHeight: 1.05 }}>
            {m.landing.hero.title}
          </div>
          <div style={{ fontSize: 30, color: "#9aa1b2", maxWidth: 900, lineHeight: 1.4 }}>{brand.tagline}</div>
        </div>
        <div style={{ fontSize: 20, color: "#6b7285" }}>{m.common.responsibleUse}</div>
      </div>
    ),
    size,
  );
}
