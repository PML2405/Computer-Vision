# Handwritten Study Notes — Generation Guide

You are creating **"iPad handwritten notes"** style study pages from raw lecture
slides/transcripts (NPTEL, university lectures, textbook chapters, etc.). Each
output is a **single self-contained HTML file** that looks like a Pinterest-aesthetic,
hand-annotated notebook page — not a slide deck, not a plain summary.

Treat every input as content for **a student encountering this topic for the very
first time**, who wants to *never have to go back to the original PDF/video*.

---

## 1. Content rules (apply before any styling)

- Assume **zero prior background** on the topic. Define every term the first time
  it appears, in plain language, before using it again.
- Do not just condense the slide — **re-teach it**. Add the "why", the intuition,
  and at least one concrete analogy per major concept if the slide doesn't
  already give one.
- **Keep every worked numerical example from the source material.** Show the
  math step-by-step, don't skip to the answer.
- Preserve all formulas exactly (LaTeX-style notation is fine, rendered as plain
  styled text — no MathJax dependency needed unless the equations are very dense).
- End every page with a **quick self-check** (2–4 questions with hand-style
  answers) so the student can verify the concept stuck.
- If a slide explicitly says "why this matters for GenAI" or connects to a later
  topic, call that out clearly — these connective threads are exam-relevant and
  easy to lose in a plain summary.
- Prefer **short paragraphs, bullets, and labeled boxes** over dense prose walls.
  This is a notebook, not an essay.
- Never fabricate facts, numbers, or citations not present in the source
  material. If the source is ambiguous, say so plainly rather than inventing.

---

## 2. Visual identity — "iPad handwritten notebook"

This is the exact design system used in the reference page. Reuse it verbatim
across every new page so the whole set feels like one continuous notebook.

### Fonts
Load both from Google Fonts:
```html
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&family=Kalam:wght@300;400;700&display=swap" rel="stylesheet">
```
- `Caveat` (700) → titles, section headers, big equations, emphasis callouts.
  This is the "flowing marker" font.
- `Kalam` (400/700) → all body text, labels, table text. This is the "ballpoint
  pen" font — must stay legible, don't overuse Caveat for anything you need to
  actually read closely.

### Color tokens (CSS variables — reuse these names/values exactly)
```css
--paper:#FBF7EC;   /* page background */
--rule:#E2D9C4;    /* faint ruled-paper lines */
--margin:#F3B8B0;  /* red margin line, like school paper */
--ink:#2E2A3D;     /* main "pen" color — never pure black */
--ink-soft:#5b5678;/* secondary/annotation text */
--yellow:#FFE98A;  /* highlighter / sticky notes */
--pink:#FFB8CE;    /* highlighter / accent nodes */
--mint:#A9E8CE;    /* highlighter / accent nodes */
--blue:#A9D4F5;    /* highlighter / accent nodes / speech bubbles */
--coral:#FF7A5C;   /* takeaway banners, stars, strong emphasis */
--tape1:#F6C89F; --tape2:#CBE7DE; --tape3:#F3AEBB; /* washi tape strips */
```

### The "hand-jitter" trick (this is what makes boxes look hand-drawn)
Define once per page, apply to every sketchy border:
```html
<svg class="defs" style="position:absolute;width:0;height:0;">
  <filter id="rough">
    <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="3.4"/>
  </filter>
</svg>
```
Apply `filter:url(#rough)` + an **uneven border-radius** (e.g.
`225px 15px 225px 15px/15px 225px 15px 225px`) to any box that should look
sketched rather than digitally drawn. Vary the `seed` value slightly between
boxes on the same page so they don't all wobble identically.

### Page shell
- Body background: flat neutral (`#DDD6C4`), page itself centered, `max-width:900px`.
- Page background: ruled paper via `repeating-linear-gradient` on `--paper`/`--rule`,
  33–35px line spacing.
- A single vertical `--margin` line ~46–70px from the left edge (like school
  notebook paper), page content padded to sit right of it.
- Page has a soft drop shadow (`box-shadow: 0 18px 40px rgba(0,0,0,.25)`) so it
  reads as a physical sheet sitting on a table.

### Reusable components (build these as CSS classes, reuse across every page)
1. **Title block** — big `Caveat` title + a hand-drawn wavy SVG underline
   (a single squiggly `<path>`, stroke = `--coral`) + a small italic subtitle line.
2. **Sticky note** (`.sticky`) — solid highlighter color, slightly rotated
   (`rotate(-1.3deg)`), rough-filter border, a small rotated "washi tape" `::before`
   rectangle pinning it at the top. Use for "big picture" / TL;DR callouts.
3. **Sketch box** (`.sketch-box`) — white or tinted background, `rough` filter,
   thick ink border, uneven radius. Use for key definitions/warnings. Offer
   `.tint-blue / .tint-mint / .tint-pink` variants.
4. **Highlighter mark** — `<mark>` styled as `linear-gradient(180deg, transparent 55%, var(--yellow) 55%)`
   so text sits *in front of* a marker stroke, not fully boxed. Never use plain
   `background:yellow` — it should look like a highlighter swipe.
5. **Index card** (`.index-card`) — small rotated card (`rotate(-0.6deg)`) for
   equations, isolated worked examples, or short numeric tables.
6. **Speech bubble** (`.bubble`) — rounded rough-bordered box with a CSS
   triangle tail, used for "read this as..." plain-language translations of formulas.
7. **Architecture/diagram card** (`.arch-card`) — used whenever the slide has
   a pipeline, network diagram, or process flow. Contains an inline `<svg>`
   hand-drawn diagram (see §3) plus a short caption paragraph.
8. **Hand table** (`.hand table`) — thick ink borders, `Caveat` header row on a
   highlighter color, alternating highlighter-colored first column per row.
9. **Takeaway banner** (`.banner`) — full-width coral block, white/cream text,
   one bold `Caveat` headline sentence + one small supporting line. One per page,
   used for the single most important "so what" of the topic.
10. **Quiz card** (`.quiz`) — dashed ink border, "✎ quick check" tab label
    overlapping the top border, numbered questions with `→ green answer` reveals
    inline (not hidden/collapsed — this is a printed note, not an interactive app).
11. **Decorative doodles** — a couple of small SVG stars/scribbles absolutely
    positioned in empty corners. Use sparingly (2–4 per page max) — restraint
    matters more than density.

### Diagram rules (for any network/pipeline/flow diagram)
- Always build diagrams as **inline SVG**, never as images.
- Circles/boxes filled with one highlighter color + `stroke:var(--ink)`.
- Connecting lines should be **slightly curved** (`C`/`Q` bezier paths), not
  straight — straight lines read as "computer-drawn."
- Label nodes with short `Kalam`-font SVG `<text>`, not HTML overlays.
- Self-loops (for memory/recurrence) drawn as small arcing paths above nodes.
- Keep each diagram's `viewBox` compact and legible at ~250–280px wide — these
  sit inside a card, not full width.

---

## 3. Page structure template

Every generated page should follow this skeleton (omit sections that genuinely
don't apply to the slide's content, but don't skip the quiz or takeaway):

```
1. Title + wavy underline + one-line subtitle
2. 🧠 "Big picture" sticky note — one paragraph, why this topic exists / what
   problem it solves, before any details
3. Numbered sections (h2.section, auto-incrementing circled number badge),
   each covering one concept from the slide, in the slide's original order
   - definitions in plain language before formulas
   - formulas in index-cards or bubbles, never bare in paragraph text
   - worked numerical examples preserved in full
   - analogies where useful
4. Diagram/architecture cards wherever the slide has a visual/pipeline
5. A hand-drawn comparison table if the slide compares multiple things
6. One takeaway banner — the single most important sentence of the page
7. Quick-check quiz (2–4 Q&A)
8. Small "— end of section notes ✏️" signoff, right-aligned, Caveat font
```

---

## 4. Workflow instructions for Claude Code

- Output **one HTML file per logical topic/section** (not per literal slide —
  group 3–8 related slides into one coherent notebook page, the way the
  reference page merged several slides on "discriminative mindset" into one page).
- Save files with descriptive snake_case names, e.g. `week1_optimizers_notes.html`,
  into a consistent output folder (e.g. `/notes/`).
- Keep the `<style>` block identical/shared across pages where possible —
  consider extracting it to a shared `notes-style.css` once you have 2+ pages,
  and `<link>` it, so the whole set stays visually consistent with zero drift.
- Do not use any JS framework, build step, or external CSS framework — plain
  HTML/CSS/inline SVG only, so every file opens standalone in a browser with
  no dependencies besides the Google Fonts link.
- After generating each page, do a self-review pass: confirm every formula
  and worked example from the source survived, confirm the quiz questions are
  actually answerable from the page content alone, and confirm no box relies on
  color alone to convey meaning (add labels/text alongside color-coding).
- If a topic is long, it's fine to make a taller single page (the format
  scrolls) rather than fragmenting one concept across multiple files.

---

## 5. Reference implementation

A full working example of this exact style (fonts, tokens, filter, all
components above) is attached as `discriminative_mindset_notes.html`. Use it
as the literal source of truth for markup/CSS — copy its structure and adapt
the content, rather than reinventing the component styles from scratch.
