# 🎨 Style Guide — the "iPad handwritten notebook" design system

> **The living version of this document is [`template.html`](template.html).** Open it in a
> browser to *see* every component; view its source to *copy* the exact markup + CSS. This
> file explains the system so you can use and tune it. **Reuse the design verbatim** across
> every page of a subject so all notes look like one product.

---

## 1. The two (three) CDN dependencies

Paste the whole `<head>` from `template.html`. It loads:

- **Fonts (always):** `Caveat` (the flowing *marker* font → titles, headers, banners,
  equations-as-emphasis) + `Kalam` (the *pen* font → all body text, labels, tables). Body
  text must stay in Kalam; never set long text in Caveat. `Fira Code` is loaded for code.
- **KaTeX (math subjects):** renders `$…$` / `$$…$$` crisply on load. Delete this block for
  a non-mathematical subject.
- **highlight.js (coding subjects):** syntax-highlights `<pre><code class="language-xxx">`.
  Delete this block if there's no code.

---

## 2. Colour tokens (reuse these names & values exactly)

```css
:root{
  --paper:#FBF7EC;   /* page background */
  --rule:#E2D9C4;    /* faint ruled-paper lines */
  --margin:#F3B8B0;  /* red margin line, like school paper */
  --ink:#2E2A3D;     /* main pen colour — never pure black */
  --ink-soft:#5b5678;/* secondary / annotation text */
  --yellow:#FFE98A; --pink:#FFB8CE; --mint:#A9E8CE; --blue:#A9D4F5; /* highlighters/accents */
  --coral:#FF7A5C;   /* takeaway banners, stars, strong emphasis */
  --tape1:#F6C89F; --tape2:#CBE7DE; --tape3:#F3AEBB; /* washi-tape strips */
}
```

The **paper + ink + ruled-line + margin** base is fixed identity — keep it. The highlighter
accents (`yellow/pink/mint/blue/coral`) may be re-themed per subject (e.g. a "forest" palette
for biology), but never let decoration fight legibility.

---

## 3. The "hand-jitter" trick (what sells the hand-drawn look)

Define once per page; apply `filter:url(#rough)` **plus an uneven border-radius** (e.g.
`225px 15px 225px 15px/15px 225px 15px 225px`) to any box that should look sketched. Vary the
`seed` slightly between nearby boxes so they don't wobble identically.

```html
<svg class="defs" style="position:absolute;width:0;height:0;">
  <filter id="rough">
    <feTurbulence type="fractalNoise" baseFrequency="0.018" numOctaves="2" seed="7" result="noise"/>
    <feDisplacementMap in="SourceGraphic" in2="noise" scale="3.2"/>
  </filter>
</svg>
```

> **Exception:** do **not** apply `#rough` to **code blocks** — the displacement waves
> monospace text and hurts readability. Code cards stay crisp (see §5).

---

## 4. Page shell

- Body background flat neutral `#DDD6C4`; the page centred, `max-width:~920px`.
- Page background = ruled paper via `repeating-linear-gradient` on `--paper`/`--rule`
  (~33–35px line spacing).
- One vertical `--margin` line ~50px from the left; content padded to sit right of it.
- Soft drop shadow so it reads as a real sheet.

---

## 5. Component vocabulary (build once as CSS classes, reuse by name)

Every class below is already defined in `template.html`. Grab the one you need there.

**Structure & framing**
- `.cover` / `.toc` *(series only)* — big Caveat title / rough-bordered contents card with anchors.
- `.lec-divider` — dark ink strip announcing a new lecture/chapter.
- `.title-block` + wavy `<svg>` underline — for standalone pages.
- `h2.section` (auto-numbered circled badge) — one per concept, in source order.

**Teaching blocks**
- `.sticky` (+`.blue/.mint/.pink`) — the **big-picture TL;DR** at the top of a topic.
- `.sketch-box` (+`.tint-blue/.tint-mint/.tint-pink/.tint-yellow`) — the workhorse box for
  definitions, key ideas, warnings (`tint-pink`).
- `.def-term` — a term being defined for the first time (bold).
- `<mark>` (+`.yellow/.mint/.blue`) — highlighter swipe *behind* text (a gradient, never solid).

**Math**
- `.index-card` / `.eq-card` — a boxed key formula (KaTeX inside).
- `.bubble` (+`.say`) — plain-language **"read this as…"** translation of a formula/jargon.
- `.worked` (`.tag` label) — a full step-by-step solved example; final answer in `\boxed{}`.

**Coding** *(this kit's additions)*
- `.code` — a "taped-in printout": dark card + filename/language tab + `<pre><code class="language-…">`.
  **Kept crisp (no `#rough`).** Reference code inline with `code.inline`.
- `.bigO` (+`.good/.bad`) — a complexity pill, e.g. `O(log n)`.
- `table.hand.trace` — a **dry-run / trace table** (mint header): walk real values through the
  code, one row per iteration. This is the coding equivalent of a worked example.
- Algorithm walkthrough = a numbered `.sketch-box.tint-mint`; **common bugs** = `.sketch-box.tint-pink`.

**Visuals**
- `.diagram` — a card holding **inline hand-style SVG** (pipeline, geometry, timeline). Nodes =
  highlighter fill + ink stroke; connectors = curved bezier + `marker-end="url(#arrow)"`, never
  dead-straight. Pair with `.two-col` to sit a diagram beside its explanation.
- `.fig` — a **real** source image (embed only when a redraw genuinely can't convey it, e.g. a
  result on a photo). Base64-inline it for a self-contained file, or use a sibling `_assets/` folder.

**Close-outs**
- `.banner` — exactly **one** coral block per page: the single "so what" sentence.
- `.quiz` — dashed card, "✎ quick check" tab, numbered questions with **inline** `.ans` (never hidden).
- `.signoff` + `.doodle` — a small "— end ✏️" and 2–4 tiny corner doodles. Restraint > density.

---

## 6. Page structure (skeleton)

Omit sections that don't apply, but **never skip the banner or the quiz**:

```
[series only] Cover → Table of contents
1. Lecture/chapter divider (if several under one file)
2. Title (+ wavy underline) + one-line subtitle
3. 🧠 big-picture sticky — why this topic exists — BEFORE any detail
4. Numbered sections, one per concept, in source order:
     • plain-language definition (def-term) BEFORE any formula/code
     • formulas in index-cards + a "read it as" bubble  |  code in .code blocks + a dry-run trace
     • worked examples / traces preserved in full
     • analogies where useful
5. Diagram / figure cards wherever the source has a visual
6. A hand comparison table if ≥2 things are contrasted
7. One coral takeaway banner
8. Quick-check quiz (2–6 Q&A, inline answers)
9. Small right-aligned "— end ✏️" signoff
```

---

## 7. Self-review after every page
- [ ] Every formula/worked example — or every function + a dry-run trace — survived.
- [ ] Every first-use term defined in plain language.
- [ ] Every quiz question answerable **from the page alone**.
- [ ] No box relies on colour alone — always a text label too.
- [ ] KaTeX renders with **zero `.katex-error`**; code highlights; `<div>` tags balanced.
- [ ] Nothing fabricated beyond reconstructing standard, well-known facts.

For the deeper *content* quality bar (the gap-classes and two-pass verification), see
[`NOTES_CREATION_GUIDE.md`](NOTES_CREATION_GUIDE.md).
