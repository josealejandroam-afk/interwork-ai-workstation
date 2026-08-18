# InterWork Brand Identity
_Extracted 2026-07-28 from `Blank Interwork BOL -.docx` (Alejandro's OneDrive Desktop), the company's real Bill of Lading template. This is the reference for any document, PDF, slide, or artifact created going forward — see `feedback_document_branding` in personal memory for the standing rule._

## Rule

**Every document InterWork Claude sessions produce — PDFs, Word docs, artifacts, handouts, reports — should use this identity: the real logo, the real brand color, not a generic default (e.g. not the placeholder blue used in the first draft of the onboarding handout).** This applies whether the doc is for InterWork itself or a client.

## Logo

File: [`assets/interwork_logo.png`](assets/interwork_logo.png) (452x127px, transparent background) — copied from the BOL template's header, this is the canonical logo file to embed in generated documents. Do not regenerate or redraw it; use this file directly.

Wordmark: "INTERWORK OFFICE SOLUTIONS" with a chevron (`>`) replacing the leading "I" in INTERWORK, and a trademark mark. All-caps, bold, condensed sans-serif.

## Colors

| Name | Hex | Where it comes from / how to use it |
|---|---|---|
| **InterWork Red** (primary) | `#BC4749` | Sampled directly from the logo pixels — this is the authoritative brand color. Use for headings, accent bars, primary buttons/highlights. |
| Word-swatch red (as-built approximation) | `#C00000` | What the BOL template actually uses for table header shading (Word's standard "Dark Red" swatch, not a true color-matched brand red). Don't propagate this approximation into new documents — use `#BC4749` instead now that we have the real value. |
| Body text | `#231F20` | Near-black, used for body copy in the BOL rather than pure black |
| Light gray (table/structure) | `#BFBFBF` | Table borders, secondary structure |
| Mid gray | `#767171` | Secondary shading |

## Typography

Calibri (Office theme default — the BOL template doesn't embed or specify a custom font). Use Calibri, or a comparable clean sans-serif (Helvetica/Arial) where Calibri isn't available (e.g. some PDF-generation libraries), rather than a serif or a mismatched sans-serif.

## Company footer block

From the BOL template's footer — use for formal documents that need a company contact block:

```
Interwork Office Solutions
Distribution Center: 100 Springdale Road, A3-300, Cherry Hill, NJ 08003
439 Commerce Lane, West Berlin, NJ 08091
Phone: 855-755-WORK (9675)
interworkoffice.com
```

(Cross-check against `memory/company_knowledge/INTERWORK_OVERVIEW.md` — that file already had both addresses; this adds the phone number and website.)

## Layout convention observed in the BOL

Logo top-left in the header, with a thin full-width red rule beneath it. Not a requirement to replicate exactly, but a reasonable default for a letterhead-style header.

## What this doesn't cover

This is a color/logo/font extraction, not a full brand guideline document (no spacing rules, no logo clear-space minimums, no secondary/tertiary palette). If a real brand guideline PDF exists somewhere, it should supersede this file — this was reverse-engineered from one template.
