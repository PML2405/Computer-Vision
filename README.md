# 📓 Handwritten Study Notes — Reusable Generation Kit

> **📦 Copying this to another subject? Use [`notes-kit/`](notes-kit/).** It's the packaged,
> portable version of this recipe — bundling the quality playbook, a ready **`template.html`**
> (the entire design system in one openable file), a style spec, and the PDF tools, and it
> adds **coding-subject support** (code blocks, dry-run traces, complexity pills). Copy the
> whole `notes-kit/` folder into any subject's project and start at
> [`notes-kit/README.md`](notes-kit/README.md). Everything below is the original write-up it was distilled from.

A **subject-independent** recipe for turning raw course material (lecture slides,
transcripts, textbook chapters, PDFs, your own scribbles) into **"iPad handwritten
notebook"** style study pages — single, self-contained HTML files that look like a
Pinterest-aesthetic, hand-annotated notebook and read as if a good tutor sat down
and re-taught the topic from scratch.

This folder contains a worked example of the kit applied to a **Computer Vision**
course — the finished notes live in `notes/` (`week1_notes.html` … `week6_notes.html`),
the style reference in `reference/`, and the generation machinery in `.build/`
(see [`STRUCTURE.md`](STRUCTURE.md) for the full map). This README is the **portable prompt/context** you hand to Claude
(or any capable model) to reproduce the *same design and quality* for **any other
subject** — history, biology, macroeconomics, operating systems, organic chemistry,
music theory, whatever.

> **How to use this file:** paste the whole "▶ PROMPT CONTEXT TO COPY" block at the
> bottom into a new chat, attach your source material, and tell it which topic to
> cover. Everything above that block explains *why* it works so you can tune it.

---

## 0. The one-sentence goal

> Produce notes so complete and so pleasant to read that the student **never has to
> open the original PDF/video again** — and actually *enjoys* revising from them.

Two non-negotiables fall out of that goal:

1. **Re-teach, don't summarize.** A summary assumes you already understood the
   lecture. These notes assume **zero prior background** and build the concept up.
2. **One self-contained `.html` file per logical topic.** No build step, no
   framework — opens in any browser by double-clicking. Math via KaTeX (CDN),
   fonts via Google Fonts (CDN), everything else inline.

---

## 1. STEP ONE — Brainstorm the subject *before* writing anything

**Do not start formatting until you have classified the material.** The design is
fixed, but *which components you lean on* and *how you pace the teaching* depend
entirely on what kind of subject it is. Read a representative chunk of the source,
then answer these questions out loud (in your planning, not in the output):

### 1a. What *type* of subject is this? (pick the dominant 1–2)

| Type | Tell-tale signs | What the notes must emphasize |
|---|---|---|
| **Mathematical / derivation-heavy** | equations, proofs, worked problems, symbols | Every formula rendered in KaTeX; **preserve every worked example step-by-step**; add a plain-language "read this as…" bubble under each formula; add a solved example even if the source only states the result. |
| **Conceptual / theory** | definitions, frameworks, "why", cause→effect | Lead with intuition + analogy; use `def-term` for every new term; comparison tables for competing ideas; a "big picture" sticky before details. |
| **Procedural / algorithmic / coding** | step lists, pseudocode, pipelines, APIs | Number the steps; use `diagram` cards for pipelines/flow; show input→output; a small code/pseudocode `index-card`; a "common mistakes" sketch-box. |
| **Visual / spatial** | geometry, anatomy, maps, circuits, architecture | Redraw diagrams as **inline SVG** (hand-style); embed the real figure *and* a simplified redraw side-by-side; heavy use of `two-col`. |
| **Memorization-heavy** | dates, taxonomies, vocab, classifications, cases | Hand-drawn tables; mnemonic sticky notes; tight `quiz` with more questions than usual; color-coded (but always also text-labeled) categories. |
| **Narrative / sequential** | history, literature, processes over time | A timeline SVG or ordered divider strip; cause→effect chains; keep chronology; call out "turning points" in coral banners. |

Most real subjects are a **blend** — e.g. an economics lecture is *conceptual +
mathematical*, a biology lecture is *conceptual + memorization + visual*. Name the
blend and let it set your component mix.

### 1b. How hard / dense is it, and how much scaffolding does the reader need?

- **Foundational / intro** → more analogies, more "why does this even exist",
  slower pace, define absolutely everything.
- **Intermediate** → assume the prior page's terms are known (if it's part of a
  series), focus on connecting ideas.
- **Advanced / graduate** → keep rigor, don't dumb down the math, but still add the
  one intuition sentence experts skip.

### 1c. Is this part of a series, or standalone?

- **Series** (e.g. "Week 3 of 6") → keep a consistent cover + table-of-contents +
  lecture dividers so all pages feel like one continuous notebook. Reuse the
  identical `<style>` block across every page (or `<link>` a shared CSS once you
  have 2+ pages) so there's **zero visual drift**.
- **Standalone** → cover/TOC optional; jump straight into the title block.

### 1d. Plan the split.

Group the source into **coherent topics of ~3–8 slides / a few textbook pages
each**, and output **one HTML file per topic** (or one per week/chapter with
internal lecture dividers, like this folder does). Never one file per literal
slide — merge related slides into one teaching narrative.

> **Output of Step One** should be a short plan: "This is a *mathematical +
> conceptual* intermediate subject, part of a 6-part series. I'll produce N pages;
> page 1 covers X (leaning on formula bubbles + worked examples), page 2 covers Y
> (leaning on comparison tables)…". *Then* start building.

---

## 2. STEP TWO — Content rules (apply before any styling)

- **Assume zero prior background.** Define every term the first time it appears, in
  plain language, before using it again. Wrap first-use terms in `.def-term`.
- **Re-teach, don't condense.** Add the *why*, the intuition, and **at least one
  concrete analogy per major concept** if the source doesn't already give one.
- **Keep every worked numerical example** from the source, shown step-by-step —
  never skip to the answer. For math subjects, *add* a solved example where the
  source only states a formula.
- **Preserve every formula exactly.** Render with **KaTeX** (see §3) so it's crisp,
  not a screenshot. Under any non-trivial formula, add a `.bubble` that translates
  it into plain English ("read this as: …").
- **End every page with a `quiz`** — 2–4 (memorization subjects: 4–6) self-check
  questions with the answers shown inline (these are printed notes, not an app —
  don't hide answers behind a click).
- **Call out connective threads.** If the source says "this matters later for…" or
  "this connects to…", flag it — those links are exam-relevant and easy to lose.
- **Short paragraphs, bullets, labeled boxes** over walls of prose. It's a
  notebook, not an essay.
- **Never fabricate** facts, numbers, dates, or citations not in the source. If the
  source is ambiguous, say so plainly instead of inventing. (Reconstructing a
  *standard, well-known* equation that the source garbled is fine — note when you do.)

---

## 3. STEP THREE — The visual identity ("iPad handwritten notebook")

This is the exact design system used in this folder. **Reuse it verbatim** for
every subject so any set of notes made with this kit looks like one product.

### 3.1 Head — fonts + math (paste as-is)

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;600;700&family=Kalam:wght@300;400;700&display=swap" rel="stylesheet">
<!-- KaTeX for crisp math inside the hand-drawn boxes -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<script>
  window.addEventListener("DOMContentLoaded", function () {
    if (window.renderMathInElement) {
      renderMathInElement(document.body, {
        delimiters: [
          {left: "$$", right: "$$", display: true},
          {left: "\\[", right: "\\]", display: true},
          {left: "$", right: "$", display: false},
          {left: "\\(", right: "\\)", display: false}
        ],
        throwOnError: false
      });
    }
  });
</script>
```

- **`Caveat` (700)** → titles, section headers, big equations-as-emphasis, banners.
  The flowing marker font.
- **`Kalam` (400/700)** → all body text, labels, table text. The ballpoint pen font
  — must stay legible; don't set long text in Caveat.
- Write math inline with `$…$` / `$$…$$`; KaTeX renders it on load. (For a
  purely non-mathematical subject you can drop the KaTeX block entirely.)

### 3.2 Color tokens (reuse these names & values exactly)

```css
:root{
  --paper:#FBF7EC;   /* page background */
  --rule:#E2D9C4;    /* faint ruled-paper lines */
  --margin:#F3B8B0;  /* red margin line, like school paper */
  --ink:#2E2A3D;     /* main pen color — never pure black */
  --ink-soft:#5b5678;/* secondary / annotation text */
  --yellow:#FFE98A;  /* highlighter / sticky */
  --pink:#FFB8CE;    /* highlighter / accent */
  --mint:#A9E8CE;    /* highlighter / accent */
  --blue:#A9D4F5;    /* highlighter / accent / bubbles */
  --coral:#FF7A5C;   /* takeaway banners, stars, strong emphasis */
  --tape1:#F6C89F; --tape2:#CBE7DE; --tape3:#F3AEBB; /* washi-tape strips */
}
```

### 3.3 The "hand-jitter" trick (this is what sells the hand-drawn look)

Define once per page, apply to any box that should look sketched:

```html
<svg class="defs" style="position:absolute;width:0;height:0;">
  <filter id="rough">
    <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="3.4"/>
  </filter>
</svg>
```

Apply `filter:url(#rough)` **plus an uneven border-radius** (e.g.
`225px 15px 225px 15px/15px 225px 15px 225px`) to boxes. Vary the `seed` a little
between nearby boxes so they don't wobble identically.

### 3.4 Page shell

- Body background flat neutral `#DDD6C4`; page centered, `max-width:~920px`.
- Page background = ruled paper via `repeating-linear-gradient` on `--paper`/`--rule`
  (~33–35px line spacing).
- One vertical `--margin` line ~50px from the left; content padded to sit right of it.
- Soft drop shadow (`box-shadow:0 18px 40px rgba(0,0,0,.25)`) so it reads as a real sheet.

### 3.5 Component vocabulary (build once as CSS classes, reuse everywhere)

These are the exact classes used in this folder — build them once, reuse by name:

1. **`.cover`** *(series only)* — big Caveat title, kicker line, subtitle, author/prof line.
2. **`.toc` / `.toc-card`** *(series only)* — rough-bordered contents card with anchor links.
3. **`.lec-divider`** — dark ink strip announcing a new lecture/chapter (`lno` label + Caveat `h2` + `lsub`).
4. **Title block** — big Caveat title + a hand-drawn wavy SVG underline (single squiggly `<path>`, stroke `--coral`) + an italic subtitle.
5. **`.sticky`** (+`.blue/.mint/.pink`) — solid highlighter note, slightly rotated, rough border, washi-tape `::before`. Use for the **"big picture" / TL;DR** at the top of each topic.
6. **`.sketch-box`** (+`.tint-blue/.tint-mint/.tint-pink/.tint-yellow`) — the workhorse box for definitions, warnings, key ideas.
7. **`.def-term`** — inline styling for a term being defined for the first time.
8. **`<mark>` highlighter** — `linear-gradient(180deg, transparent 55%, var(--yellow) 55%)` so text sits *in front of* a marker swipe. Never a plain solid `background:yellow`.
9. **`.index-card` / `.eq-card`** — small rotated card for an isolated equation, worked example, or short table.
10. **`.bubble`** (+`.say`) — rough box with a CSS-triangle tail, for **plain-language "read this as…" translations** of formulas/jargon.
11. **`.worked`** (with a `.tag` label like *"worked example"*) — a full step-by-step solved problem, steps in an `<ol>`, final answer `\boxed{}`.
12. **`.diagram`** — a card holding an **inline hand-style SVG** (pipeline, flow, geometry, timeline) + short caption. Use `.two-col` to sit a diagram beside its explanation.
13. **`.fig` / `.illus`** — an embedded real figure from the source (stored beside the HTML in an `assets/` folder — *not* base64), with a `.cap` caption. Pair a real figure with a redrawn SVG when it helps.
14. **`.hand table`** — thick ink borders, Caveat header row on a highlighter color, alternating-tinted first column. For any comparison of ≥2 things.
15. **`.banner`** — one full-width coral block per page: the single most important "so what" sentence in Caveat.
16. **`.quiz`** — dashed-border card, "✎ quick check" tab overlapping the top edge, numbered `<li>` questions with inline `.ans` reveals.
17. **`.signoff`** — small right-aligned Caveat "— end of section ✏️".
18. **`.doodle`** — 2–4 small absolutely-positioned SVG stars/scribbles in empty corners. **Restraint > density.**

### 3.6 Diagram rules (any flow / network / geometry / timeline)

- Always **inline SVG**, never a rasterized diagram.
- Nodes = one highlighter fill + `stroke:var(--ink)`; connectors = **slightly curved
  bezier** (`C`/`Q`) paths, never dead-straight (straight = "computer-drawn").
- Labels = short `Kalam` SVG `<text>`, not HTML overlays.
- Keep each `viewBox` compact and legible at ~250–280px wide inside a card.

---

## 4. STEP FOUR — Page structure template

Every generated page follows this skeleton (omit sections that genuinely don't
apply, but **never skip the takeaway banner or the quiz**):

```
[series only] Cover  →  Table of contents
1. Lecture/chapter divider (if grouping several under one file)
2. Title + wavy underline + one-line subtitle
3. 🧠 "Big picture" sticky — one paragraph: why this topic exists / what problem
   it solves — BEFORE any details
4. Numbered sections (h2.section, auto-incrementing circled badge), each = one
   concept, in the source's original order:
     • plain-language definition (def-term) BEFORE any formula
     • formulas in index-cards/eq-cards or bubbles, never bare in a paragraph
     • worked examples preserved in full (.worked)
     • analogies where useful
5. Diagram / figure cards wherever the source has a visual, pipeline, or geometry
6. A hand-drawn comparison table if the source compares multiple things
7. One coral takeaway banner — the single most important sentence of the page
8. Quick-check quiz (2–6 Q&A, inline answers)
9. Small right-aligned "— end of section ✏️" signoff
```

---

## 5. STEP FIVE — Workflow, guardrails & self-review

- **One HTML file per logical topic**, descriptive `snake_case` names
  (`week3_camera_geometry_notes.html`, `ch2_thermodynamics_notes.html`).
- **Assets live in a sibling folder** (`<name>_assets/`) referenced by relative
  path — *not* base64-embedded — so files stay small and openable.
- **Keep the `<style>` block identical across pages.** Once you have 2+ pages,
  extract it to a shared `notes-style.css` and `<link>` it, to prevent drift.
- **No JS framework, no build step, no CSS framework.** Plain HTML + CSS + inline
  SVG + the two CDN links (fonts, KaTeX) only. Each file must open standalone.
- **Self-review pass after every page** — verify explicitly:
  - [ ] Every formula & worked example from the source survived.
  - [ ] Every first-use term is defined in plain language.
  - [ ] Every quiz question is answerable **from the page alone**.
  - [ ] **No box relies on color alone** to carry meaning — always add a text label
        too (accessibility + prints fine in grayscale).
  - [ ] KaTeX renders with **zero `.katex-error`** (spot-check in a browser).
  - [ ] Nothing was fabricated beyond reconstructing standard, well-known facts.
- If a topic is long, prefer **one taller scrolling page** over fragmenting a single
  concept across files.

---

## 6. Adapting the design (optional)

The *structure* is subject-independent; only swap surface details when it genuinely
helps the subject:

- **Palette:** the highlighter accents (`--yellow/pink/mint/blue/coral`) can be
  re-themed per subject (e.g. a "forest" palette for a biology set) — but keep the
  **paper + ink + ruled-line + margin** base identical so it still reads as a notebook.
- **Fonts:** Caveat + Kalam are the identity; don't change them unless you're
  deliberately making a distinct notebook set.
- **Density of doodles/tape:** dial down for a serious/technical subject, up for a
  lighter one — but never let decoration fight legibility.

---

## ▶ PROMPT CONTEXT TO COPY (hand this + your source material to the model)

> You are creating **"iPad handwritten notes"** — single, self-contained HTML study
> pages that look like a Pinterest-aesthetic hand-annotated notebook and re-teach a
> topic from scratch to a student with **zero prior background**, so they never need
> the original source again. Follow the kit in `README.md` exactly.
>
> **First, brainstorm before formatting.** Read the material I give you and tell me:
> (1) what *type* of subject it is — mathematical / conceptual / procedural / visual
> / memorization-heavy / narrative, or which blend; (2) its difficulty and how much
> scaffolding the reader needs; (3) whether it's standalone or part of a series; and
> (4) how you'll split it into ~3–8-slide topics, one HTML file each. Then state
> which components you'll lean on given that classification (e.g. formula bubbles +
> worked examples for math; comparison tables + mnemonics for memorization).
>
> **Then build**, reusing verbatim the design system in `README.md §3`: `Caveat` +
> `Kalam` Google Fonts; KaTeX via CDN for all math; the exact color tokens; the
> `#rough` SVG hand-jitter filter with uneven border-radii; ruled-paper page shell
> with a red margin line and drop shadow; and the component vocabulary — `sticky`
> (big-picture TL;DR), `sketch-box`, `def-term`, highlighter `<mark>`, `index-card`/
> `eq-card`, `bubble` ("read this as…"), `worked` (step-by-step solved examples),
> inline-SVG `diagram`s (curved connectors, highlighter nodes), `hand table`,
> one coral `banner`, and a `quiz`. Follow the page structure in `README.md §4`.
>
> **Rules:** define every term on first use before using it; keep every worked
> example step-by-step (add one if math is stated without a solved example); put a
> plain-English translation under every non-trivial formula; end every page with an
> inline-answer quiz; never rely on color alone (always label); never fabricate
> facts/numbers/dates not in my source. Output one standalone `.html` per topic
> (snake_case), assets in a sibling `_assets/` folder by relative path (not base64),
> plain HTML/CSS/inline-SVG only (no framework/build step), and keep the `<style>`
> block identical across all pages. After each page, run the `README.md §5`
> self-review checklist and report the result.
>
> The subject is: **[FILL IN]**. My source material is attached: **[ATTACH]**.

---

*This kit was distilled from the Computer Vision notebook in this folder
(`week1_notes.html` … `week4_notes.html`, `reference /NOTES_STYLE_GUIDE.md`). Use
those as the literal source of truth for markup/CSS when in doubt — copy a component
and swap the content rather than reinventing it.*
