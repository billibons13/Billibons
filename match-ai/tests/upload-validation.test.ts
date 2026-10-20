import { describe, expect, it } from "vitest";
import { getMaxUploadBytes } from "@/lib/config/upload";
import { getExtension, sniffImageType, validateUpload } from "@/lib/upload/validate";

const PNG = new Uint8Array([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0, 0, 0, 0x0d]);
const JPEG = new Uint8Array([0xff, 0xd8, 0xff, 0xe0, 0, 0x10, 0x4a, 0x46, 0x49, 0x46, 0, 1]);
const WEBP = new Uint8Array([0x52, 0x49, 0x46, 0x46, 0x24, 0, 0, 0, 0x57, 0x45, 0x42, 0x50]);
const GIF = new Uint8Array([0x47, 0x49, 0x46, 0x38, 0x39, 0x61, 0, 0, 0, 0, 0, 0]);
const PDF = new Uint8Array([0x25, 0x50, 0x44, 0x46, 0x2d, 0x31, 0x2e, 0x34, 0, 0, 0, 0]);
const RIFF_WAV = new Uint8Array([0x52, 0x49, 0x46, 0x46, 0x24, 0, 0, 0, 0x57, 0x41, 0x56, 0x45]);

const MAX = 8 * 1024 * 1024;

describe("sniffImageType", () => {
  it("detects PNG, JPEG and WEBP by magic bytes", () => {
    expect(sniffImageType(PNG)).toBe("image/png");
    expect(sniffImageType(JPEG)).toBe("image/jpeg");
    expect(sniffImageType(WEBP)).toBe("image/webp");
  });

  it("rejects other formats and truncated input", () => {
    expect(sniffImageType(GIF)).toBeNull();
    expect(sniffImageType(PDF)).toBeNull();
    expect(sniffImageType(RIFF_WAV)).toBeNull();
    expect(sniffImageType(new Uint8Array([0x89, 0x50]))).toBeNull();
    expect(sniffImageType(new Uint8Array())).toBeNull();
  });
});

describe("getExtension", () => {
  it("returns the lowercase extension", () => {
    expect(getExtension("Screen Shot.PNG")).toBe("png");
    expect(getExtension("dir/a.b.jpeg")).toBe("jpeg");
    expect(getExtension("noext")).toBe("");
    expect(getExtension(".hidden")).toBe("");
  });
});

describe("validateUpload", () => {
  it("accepts valid images", () => {
    expect(validateUpload({ bytes: PNG, declaredType: "image/png", fileName: "a.png", size: 1000 }, MAX)).toEqual({
      ok: true,
      type: "image/png",
      extension: "png",
    });
    expect(validateUpload({ bytes: JPEG, declaredType: "image/jpg", fileName: "a.JPG", size: 1000 }, MAX).ok).toBe(true);
    expect(validateUpload({ bytes: WEBP, declaredType: "image/webp", fileName: "a.webp", size: 1000 }, MAX).ok).toBe(true);
  });

  it("rejects files that are too large", () => {
    expect(validateUpload({ bytes: PNG, declaredType: "image/png", fileName: "a.png", size: MAX + 1 }, MAX)).toEqual({
      ok: false,
      code: "IMAGE_TOO_LARGE",
    });
  });

  it("rejects empty files", () => {
    expect(validateUpload({ bytes: new Uint8Array(), declaredType: "image/png", fileName: "a.png", size: 0 }, MAX)).toEqual({
      ok: false,
      code: "INVALID_IMAGE",
    });
  });

  it("rejects unsupported MIME types and extensions", () => {
    expect(validateUpload({ bytes: GIF, declaredType: "image/gif", fileName: "a.gif", size: 10 }, MAX)).toEqual({
      ok: false,
      code: "UNSUPPORTED_FORMAT",
    });
    expect(validateUpload({ bytes: PNG, declaredType: "image/png", fileName: "a.exe", size: 10 }, MAX)).toEqual({
      ok: false,
      code: "UNSUPPORTED_FORMAT",
    });
  });

  it("rejects spoofed files whose content does not match", () => {
    // PDF renamed to .png with a PNG MIME type
    expect(validateUpload({ bytes: PDF, declaredType: "image/png", fileName: "a.png", size: 10 }, MAX)).toEqual({
      ok: false,
      code: "INVALID_IMAGE",
    });
    // JPEG content declared as PNG
    expect(validateUpload({ bytes: JPEG, declaredType: "image/png", fileName: "a.png", size: 10 }, MAX)).toEqual({
      ok: false,
      code: "INVALID_IMAGE",
    });
    // PNG content with .jpg extension
    expect(validateUpload({ bytes: PNG, declaredType: "image/png", fileName: "a.jpg", size: 10 }, MAX)).toEqual({
      ok: false,
      code: "INVALID_IMAGE",
    });
  });
});

describe("getMaxUploadBytes", () => {
  it("uses MAX_UPLOAD_MB or the default", () => {
    expect(getMaxUploadBytes("2")).toBe(2 * 1024 * 1024);
    expect(getMaxUploadBytes(undefined)).toBe(8 * 1024 * 1024);
    expect(getMaxUploadBytes("abc")).toBe(8 * 1024 * 1024);
    expect(getMaxUploadBytes("-1")).toBe(8 * 1024 * 1024);
  });
});
