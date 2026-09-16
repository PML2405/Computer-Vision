# 📓 Handwritten Study-Notes Kit — START HERE

A **subject-independent, drop-in kit** for turning course material (lecture **slides**,
video **transcripts**, and **assignment solutions**) into **"iPad handwritten notebook"**
study pages: single, self-contained HTML files that look hand-annotated and **re-teach a
topic from scratch**, so you can revise from the notes alone — no slides, no videos —
and answer every assignment/exam question.

It works for **any subject** and adapts to whether the material is **theory, mathematical,
or coding** (or a blend). It was distilled from a full 33-lecture Computer Vision build
that was verified against the real assignments.

---

## 📦 What's in this kit (and what to copy)

Copy the **entire `notes-kit/` folder** into your other subject's project folder. That's it.

| File | What it is | You need it |
|---|---|---|
| **`README.md`** (this file) | how to use the kit + the copy-paste prompt | always |
| **`template.html`** | the **design system as one openable file** — every component rendered; view-source to copy. Also your starter file. | always |
| **`STYLE_GUIDE.md`** | the visual system spec — colours, fonts, components, the code/coding components | always |
| **`NOTES_CREATION_GUIDE.md`** | the **quality playbook** — the gap-classes (G1–G9) that make notes secretly incomplete, and the two-pass verification that catches them | always |
| **`tools/`** | pure-Python PDF extractors (transcript text, embedded figures, figure→page map) + `TOOLS.md` | only if your source is **PDF** and needs text/figure extraction |

> **Nothing in the kit is subject-specific.** Open `template.html` in a browser first —
> it shows you exactly what the notes look like and every building block available.

---

## ▶ How to use it (two ways)

**A. Just tell your assistant.** Drop `notes-kit/` in the project, add your source
material, and say:

> "Build iPad-handwritten study notes for **[SUBJECT]** using the kit in `notes-kit/`.
> Follow `notes-kit/README.md`, reuse `notes-kit/template.html`'s `<head>`+`<style>`
> verbatim, and verify with `notes-kit/NOTES_CREATION_GUIDE.md`. My material is in
> **[folder]**: [slides / transcripts / assignment solutions]."

**B. Paste the prompt.** Use the **"PROMPT CONTEXT TO COPY"** block at the bottom of this
file into a fresh chat, attach your material, and fill in the subject.

---

## 🧭 The workflow (what the assistant should do)

### 1. Inventory & classify the sources *before writing anything*
List every file and what it is. **Read a representative chunk**, then decide the
**dominant subject type** — it sets which components to lean on:

| Type | Tell-tale signs | Lean on |
|---|---|---|
| **Mathematical** | equations, proofs, worked problems | KaTeX for every formula; **worked examples** step-by-step (add one if the source only states a result); a "read it as" bubble under each formula |
| **Conceptual / theory** | definitions, frameworks, "why", cause→effect | big-picture sticky; `def-term` for every term; **comparison tables**; analogies; mnemonics |
| **Coding / algorithmic** | pseudocode, APIs, data structures, complexity | **code blocks** (highlight.js) + inline code; **dry-run trace tables**; complexity pills; algorithm-walkthrough + **common-bugs** boxes; pipeline diagrams |
| **Visual / spatial** | geometry, anatomy, maps, circuits | redrawn inline-SVG diagrams; real figure + redraw side-by-side (`two-col`) |
| **Memorization** | dates, taxonomies, vocab, cases | hand tables; mnemonic stickies; a longer quiz (4–6); labelled colour categories |
| **Narrative / history** | processes over time, literature | timeline SVG; cause→effect chains; "turning point" banners; keep chronology |

Most subjects are a **blend** (economics = conceptual + mathematical; DSA = coding +
mathematical). Name the blend; it decides your component mix. Also note **difficulty**
(more scaffolding for intro; keep rigor for advanced) and whether it's a **series**
(keep a shared cover/TOC/dividers so every page feels like one notebook) or standalone.

### 2. Handle whatever input you have
- **Slides** → exact equations, figures, structure, terminology. Read them (visually if
  text extraction garbles). Extract essential figures with `tools/` (see `TOOLS.md`).
- **Transcripts** → the *ground truth of what was taught* — every explanation, in order.
  The spoken narration usually walks through each slide.
- **Assignment solutions** → **gold.** They tell you the *exact* formulas/methods/criteria
  the exam makes you apply. Use them as the target for verification **Pass B** (below) —
  every question must be answerable from the notes alone.
- Any subset works. With only a transcript, you still get complete notes; with slides +
  assignments too, you get exam-targeted notes.

### 3. Plan the split
Group into coherent topics (~3–8 slides / a lecture each) → **one HTML file per topic**
(or one per week/chapter with internal lecture dividers). Never one file per literal slide.

### 4. Lock the look on ONE topic, then replicate
Duplicate `template.html`, strip the demo gallery, keep the `<head>`+`<style>`, author the
first topic, render it, confirm it looks right — *then* reuse that exact shell for the rest.

### 5. Author each topic
Re-teach, don't summarise. Follow the **per-lecture content contract** and design out the
**gap-classes** in `NOTES_CREATION_GUIDE.md`. Author **directly** (don't offload heavy HTML
generation to fragile background agents — see the guide's tooling notes).

### 6. Verify — the two passes that actually catch gaps
- **Pass A** — adversarial per-lecture review vs the transcript (completeness + correctness).
- **Pass B** — coverage vs the **real assignment solutions**: classify every question
  *sufficient / partial / missing / prerequisite*, then patch.

Full detail, checklist, and the gap-classes: **`NOTES_CREATION_GUIDE.md`**.

---

## ✅ Non-negotiables (the bar)
1. **Re-teach, don't condense** — assume zero prior background; define every term on first use.
2. **Question-answerable, not just concept-present** — the exact formula/criterion/method a
   question makes you apply must be *written*, ideally with a worked example.
3. **Correct** — every formula standard and right; every worked number either the source's
   (verified) or clearly tagged *illustrative*. Never fabricate.
4. **One self-contained `.html` per topic** — plain HTML/CSS/inline-SVG; only CDN deps are
   fonts (always), KaTeX (math), highlight.js (code). Keep the `<style>` identical across pages.
5. **Never rely on colour alone** — always add a text label (accessibility + grayscale print).

---

## ▶ PROMPT CONTEXT TO COPY (hand this + your source material to the model)

> You are creating **"iPad handwritten notes"** — single, self-contained HTML study pages
> that look like a hand-annotated notebook and **re-teach a topic from scratch** to a
> student with zero prior background, so they never need the original source again. Use the
> kit in **`notes-kit/`**: reuse **`template.html`**'s `<head>`+`<style>` verbatim (it holds
> the whole design system — fonts, KaTeX, highlight.js, and every component), follow this
> `README.md`, and verify with `NOTES_CREATION_GUIDE.md`.
>
> **First, classify before formatting.** Read my material and tell me: (1) the dominant
> subject **type** — mathematical / conceptual / **coding** / visual / memorization /
> narrative, or the blend; (2) difficulty & scaffolding needed; (3) standalone or a series;
> (4) how you'll split it into ~3–8-slide topics, one HTML file each. Then say which
> components you'll lean on (e.g. worked-example cards + formula bubbles for math; **code
> blocks + dry-run trace tables + complexity pills + common-bugs boxes** for coding;
> comparison tables + mnemonics for theory/memorization).
>
> **Then build**, reusing the design system exactly: `Caveat`+`Kalam` fonts; KaTeX for all
> math; highlight.js for code; the colour tokens; the `#rough` SVG hand-jitter filter with
> uneven border-radii; the ruled-paper page shell with a red margin line and drop shadow;
> and the component vocabulary — `sticky` (big-picture TL;DR), `sketch-box`, `def-term`,
> highlighter `<mark>`, `index-card`/`eq-card`, `bubble` ("read this as…"), `worked`
> (step-by-step solved examples), inline-SVG `diagram`s, `hand` tables, **`code` blocks +
> `bigO` pills + `hand trace` tables for coding**, one coral `banner`, and a `quiz`.
>
> **Rules:** define every term on first use; keep every worked example / dry-run step-by-step
> (add one if the source only states a result or a function); put a plain-English translation
> under every non-trivial formula; end every page with an inline-answer quiz; never rely on
> colour alone; never fabricate. Output one standalone `.html` per topic (snake_case), plain
> HTML/CSS/inline-SVG + the CDN deps only, `<style>` identical across pages. **Then verify**
> with the two passes (adversarial vs transcript; coverage vs my assignment solutions) and
> report what's covered.
>
> The subject is: **[FILL IN]**. My source material (slides / transcript / assignment
> solutions) is in: **[FILL IN]**.

---

*Distilled from the Computer Vision notebook this kit shipped with. When in doubt about
markup/CSS, open `template.html` and copy a component rather than reinventing it.*
