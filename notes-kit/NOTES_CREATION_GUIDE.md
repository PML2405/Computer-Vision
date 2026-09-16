# Study-Notes Creation Guide (subject-independent)

A reusable playbook for turning course material (lecture **transcripts** + **slides**, and ideally **assignments/past papers**) into study notes so complete a student can **rely on the notes alone — no videos, no slides — and answer every assignment/exam question.**

This guide is distilled from a full multi-week course build where the first pass *looked* complete but a rigorous verification found real gaps. The point of this document is: **know those gap-classes up front and design them out from the start**, then verify against the actual assessment.

> Copy this file into any new notes project. Nothing below is subject-specific.

---

## 0. The standard to hit

The bar is **not** "a good summary." It is:
1. **Re-teach, don't condense.** Assume zero prior knowledge; define every term the first time; give the *why* + an analogy, not just the *what*.
2. **Question-answerable, not just concept-present.** The test is: could a student solve the *assignment/exam questions* from the notes alone? A concept can be "mentioned" and still leave a question unanswerable (see §3).
3. **Faithful to what was actually taught** — cover every method the instructor spends time on, keep their worked examples, use their terminology.
4. **Correct.** Every formula standard and right; every worked number either the instructor's or clearly labelled illustrative.

---

## 1. Process overview (the pipeline that works)

1. **Inventory the sources.** List every transcript/slide/assignment file; identify what each is; get page/lecture counts.
2. **Build reliable extraction** (§6). Transcript = the ground truth of what was taught (spoken word). Slides = exact equations, diagrams, figures.
3. **Map the structure.** Which lectures belong to which week/unit; where each lecture starts/ends in the transcript.
4. **Lock the style/template on ONE lecture first** (§5), render it, confirm it looks right, then replicate.
5. **Author each lecture** directly (see §7 on why *not* to use background workflows for generation), covering everything in that lecture's transcript.
6. **Verify — two passes** (§4): (a) adversarial per-lecture review vs transcript; (b) coverage check vs the actual assignments/past papers.
7. **Patch every gap, re-validate, deliver.**

---

## 2. ⭐ The gap-classes that bite you (design these out from the start)

These are the concrete failure modes found in real verification. **Treat this as a checklist while authoring each lecture.**

### G1 — Dropping a whole method the instructor teaches
Compression is the #1 enemy. If the instructor spends even a couple of minutes on a *distinct method*, it is testable and must appear in full — not folded into a sibling. Examples that were wrongly compressed away:
- an alternative solver (e.g. the **non-homogeneous least-squares / pseudo-inverse** route alongside the homogeneous/SVD route),
- a **closed-form formula** (e.g. a Cramer's-rule expression as an alternative to a matrix inverse),
- an entire **named technique** in a list (e.g. one of four texture methods silently skipped).
> Rule: for every "we can also do X", "another method is Y", "there are N ways/kinds" — each item gets its own explained block.

### G2 — Concept present, but not the exact rule the question needs
The single most common gap. The notes explain the *idea* but omit the *specific criterion/formula/step* an exam would apply. Examples:
- taught "separability" of transform *bases* but never stated the operational rule **"a filter mask is separable ⇔ rank 1 (outer product)."**
- gave a *general* formula that needs data the question doesn't supply, but not the **special-case shortcut** the question actually uses (e.g. plane normal `= x₁ × x₂` for a camera at the origin, vs the general `Pᵀ(xᵢ×xⱼ)`).
> Rule: for each concept, ask **"what would a numerical/exam question make me *compute*?"** and make sure that exact formula/criterion is written, ideally with a one-line worked check.

### G3 — Wrong or garbled math from the source
Transcript/slide extraction **garbles equations** (custom fonts, OCR). Reconstruct standard forms from domain knowledge, but this is where sign/label/order errors creep in. Real errors found:
- a **swapped left/right** pairing (e.g. left vs right epipole read off the wrong row/column),
- a **reversed vector/coordinate order** in a worked example,
- a matrix written as `diag(...)` when it must be **upper-triangular** (a diagonal can scale but not translate),
- a **mislabeled annotation** (an `underbrace` blaming the wrong quantity for a DOF count).
> Rule: cross-check every non-trivial formula against a **standard reference** for the field. Re-derive DOF counts. Verify any "read-off-the-matrix" claim by actually testing it on a small example.

### G4 — Losing the instructor's specific worked numbers (or inventing wrong ones)
Keep every worked *numerical* example — that's exam gold. But when the exact slide numbers can't be extracted:
- **do not assert wrong numbers as if they were the instructor's.** Either recover them (view the slide) or present the **method** with **clearly-labelled illustrative** numbers ("illustrative — our own numbers to show the method").
> Rule: a worked example is either (a) the source's real numbers, verified, or (b) explicitly tagged illustrative. Never a third, ambiguous state.

### G5 — Not naming things the instructor names
Exam questions use the terminology. If the instructor says a map is a "correlation", or names "disparity", "vector quantization", "conjugate rotation", "characteristic scale" — the term must be **in bold in the notes**, even if you also explain it plainly.

### G6 — Teaching one variant without naming the canonical ones
When the instructor teaches a *specific variant* of a standard thing, teach that variant faithfully **but also name the canonical/standard forms**, because the exam may use either. (E.g. a corner-response measure taught as `det/tr` — the harmonic-mean/Noble form — should also mention the canonical Harris–Stephens `det − k·tr²` and Shi–Tomasi `min(λ)`.)

### G7 — Cumulative / cross-unit assessment
Assignments and exams **review cumulatively**. If a topic is split across "weeks/units" (e.g. a big topic spread over several lectures), a later unit's assignment will lean on earlier units' formulas. **Each unit's notes should be self-sufficient for that unit's assessment** — add a compact **"essentials recap" box** cross-referencing the key carried-over formulas, so the student needn't flip back mid-problem.

### G8 — Assessment tests deferred or forward-looking material
Instructors sometimes say "we'll cover X in the next topic" — and then the current assignment tests X anyway. Also, exams pull "look-ahead" standard tools. **Add a clearly-labelled "look-ahead" box** covering deferred-but-tested topics (name + one-line what-it-does + the key formula), flagged as beyond the current lectures.

### G9 — Prerequisite vs course gap (don't over- or under-react)
Some questions rely on **general background** the notes reasonably assume (reading a normal/z-table, basic matrix arithmetic, a covariance-matrix definition, solving a 2×2 characteristic equation, a parametric-curve tangent). These are **not course gaps** — don't pad the notes with a whole stats course. But **do** offer/insert a one-line refresher box where a rusty student would otherwise stall. Classify each shortfall as *course-gap* (fix it) vs *fair-prerequisite* (optional refresher) and say which.

---

## 3. Per-lecture content contract (what every lecture must contain)

- **Big-picture opener** — why this topic exists / what problem it solves, before any detail.
- **Every concept from the transcript**, in the instructor's order, each: definition (plain language) → intuition/analogy → the exact formula(s) → how it's used.
- **Every distinct method/derivation** the instructor covers (see G1), each in full.
- **The operational criterion for each concept** (see G2) — the thing a question makes you compute.
- **At least one worked example** with real or clearly-illustrative numbers (see G4), step by step.
- **Named terms** in bold (see G5); **canonical variants** noted (see G6).
- **A comparison table** whenever ≥2 things are contrasted (transforms, detectors, transform-hierarchies, etc.).
- **A short self-check quiz** (3–4 Q&A, answers shown) so the student can verify retention.
- **Cross-references** to prior lectures the material builds on; a recap box if the unit's assessment is cumulative (G7).

---

## 3.5 Adapting the contract to the subject type (theory · math · coding)

The gap-classes and the two-pass verification are universal. What "complete" and "correct"
*mean* shifts with the material — **classify the subject first** (see the kit README's type
table), then apply the matching contract. Most subjects **blend** types; apply every contract
that fits (DSA = coding + mathematical; ML = math + coding + conceptual; economics = conceptual
+ mathematical).

**Mathematical** — every formula in KaTeX; a plain-language "read it as" bubble under each;
**every worked example step-by-step** (add one if the source only states a result). G2 = the
exact formula a numerical question makes you *compute*; G3 = cross-check the math.

**Conceptual / theory** — lead with intuition + analogy; `def-term` every term; a comparison
table for every set of competing ideas. The "operational" thing a question tests is often a
*distinction* or a *criterion to classify* — make that explicit. Watch G5 (name what the
instructor names) and G6 (canonical vs the taught variant).

**Coding / algorithmic** — the coding analogues of the math contract:
- **Both the algorithm in words (numbered steps) *and* the code** (in a `.code` block) — not
  one or the other. Name the algorithm/pattern (G5) and its standard variants (G6).
- **Correctness = it runs and handles edge cases.** The code must be valid and complete; call
  out edge cases (empty input, single element, duplicates, overflow, off-by-one). A
  plausible-but-buggy snippet is the coding form of G2/G3 — verify it mentally or actually run it.
- **A dry-run trace is the coding "worked example"** (G4): walk concrete inputs through the code,
  one row per iteration, in a `hand trace` table. Keep the source's own example inputs.
- **State complexity** — time & space Big-O (a `.bigO` pill) with one line on *why*.
- **A common-bugs / gotchas box** — the coding equivalent of a warning; exam-relevant.
- If the **assignment traces code / data-structure operations**, G2 = ensure the exact operation
  it asks about (an insertion, a recurrence step, a pointer update, an output) is shown in the notes.

---

## 4. Verification — the two passes that actually catch gaps

Author quality alone is not enough; the first pass always *looks* complete. Run both:

### Pass A — adversarial per-lecture review vs the transcript
For each lecture, an **independent critical reviewer** (fresh eyes, told to *refute*, not rubber-stamp) diffs the notes against that lecture's transcript and reports, per lecture:
- **completeness**: every concept/derivation/worked-example present? list what's missing or thin.
- **correctness**: are the equations standard and right? flag wrong/garbled/mislabelled math.
- **clarity**: anything too terse to learn from cold?
- **figure need**: any place a *real* image is essential (see §8)?
- verdict + "could a student ace the exam from this alone?"

### Pass B — coverage against the real assessment (assignments / past papers)
This is the decisive test. For each assignment (ideally with its answer key), classify **every question**:
- **sufficient** — concept + formula + method all clearly in the notes.
- **partial** — concept present but a specific formula/step the question needs is missing/thin. → fix.
- **missing** — the course concept the question tests is absent (and should be there). → fix.
- **prerequisite** — general assumed background, not a course gap (see G9). → optional refresher.
> Watch for the **cross-unit artifact**: a unit may look under-covered only because the reviewer saw one unit's notes while the assignment reviews several. Check the *full* note set before concluding "missing" (see G7).

Then **patch every partial/missing**, re-validate, and re-run coverage if needed.

---

## 5. Style/format system (the "handwritten notebook" template)

A consistent visual system makes a multi-lecture set feel like one continuous notebook and keeps authoring fast. **The concrete, ready-to-use version lives in `template.html` (open it to see every component) with the spec in `STYLE_GUIDE.md` — copy a component from there rather than reinventing CSS.**
- **One self-contained HTML file per unit/week.** Plain HTML/CSS + inline SVG; no framework/build step.
- **Two CDN dependencies only:** a handwriting-font pair (a "marker" display font for titles/headers + a legible "pen" font for body) and, for math-heavy subjects, **KaTeX** (auto-render).
- **Reusable components (CSS classes), used verbatim across every page:** page shell (ruled paper, margin rule, drop shadow), title block, **sticky note** (big-picture callouts), **sketch-box** (definitions/warnings; tinted variants), **index-card** (boxed key formula), **speech bubble** ("read this formula as…"), **worked-example card**, **diagram card** (inline SVG), **hand table** (comparisons), one **coral takeaway banner** per page, **quiz card**, signoff. **Coding subjects add:** a crisp (un-jittered) **`.code`** block with syntax highlighting (highlight.js) + filename tab, a **`hand trace`** dry-run table, **`.bigO`** complexity pills, and algorithm-walkthrough / common-bugs sketch-boxes.
- **Hand-drawn feel:** an SVG turbulence/displacement filter (`#rough`) + uneven border-radius on boxes; vary the filter seed so boxes don't wobble identically; a couple of small doodle SVGs per page (use restraint).
- **Math:** for dense subjects, render real math with **KaTeX inside the hand-drawn boxes** (crisp equations in a handwritten container reads best) — inline `$…$`, display `$$…$$`. For light math, hand-font text equations are fine. Always give each important formula a plain-language "read it as" bubble.
- **Lock the template on lecture 1, render it, confirm, then replicate.** Extract the shared `<head>`+`<style>` once; reuse for every unit.
- **Group logically:** one file per unit; within it, one titled section per lecture; number sections 1..N and restart per lecture.

---

## 6. Source extraction (transcript & slides) — practical notes

- **Transcript = ground truth of teaching** (the spoken narration usually describes each slide). **Slides = exact equations, figures, structure.** Use both: transcript for *what was said/every explanation*, slides for *exact math + figures*.
- **Extraction is often hard.** Expect: PDFs with **custom/re-encoded fonts** (text comes out as glyph-code garbage), **mixed TrueType + CID/Type0** pages, **object streams**, out-of-order objects. A robust extractor needs: page-tree ordering, `/ToUnicode` CMap decoding, CID (2-byte) handling, and TJ-kerning-aware spacing.
- **Inline math extracts badly** even when prose is clean — reconstruct standard equations from domain knowledge (then verify, see G3). Don't paste garbled math.
- **Slides may need visual reading** (rendered pages) to capture diagrams/exact equations when text extraction fails.
- **Normalize** transcript text (fix UTF-8-through-latin1 artifacts, en-dashes, ligatures, intra-word spacing).

---

## 7. ⚙️ Tooling & workflow gotchas (important, saves hours)

- **Background multi-agent workflows: use them ONLY for read + structured-output tasks** (verification, coverage checks) — those ran reliably. **Do NOT use them for heavy generation** (authoring/patching full HTML): those agents **stall** (long no-progress timeouts × retries) and are **killed/restarted every time the user sends a message** (each user turn preempts in-flight background work). **Author and patch directly in the main thread**, or in small structured pieces.
- If a background run stalls/loops, **stop it and recover partial results from the run's journal** (agents may have written useful output before dying), then finish inline.
- **Structured-output verification workflows are excellent** — one reviewer per lecture/question, returning a strict schema (completeness/correctness/coverage). Reliable and fast.

---

## 8. Figures — SVG vs real slide images

- **Redraw as inline SVG** for anything conceptual/geometric/plot-like (pipelines, coordinate frames, geometry, histograms, small diagrams). SVG is clean, consistent, and often *better* than the slide.
- **Embed the REAL slide image only when a redraw genuinely can't convey it:** a result *on a real photo/pattern* (e.g. an eigenvalue map showing corners light up, keypoints overlaid on a scene, a before/after rectification, a retrieval demo). The verification's "figure need" flag tells you exactly where.
- **Extraction:** embedded raster figures can be pulled from the PDF (JPEG dumps directly; other bitmaps reconstruct to PNG); **map each figure to the slide page that uses it** (via the page's XObject `Do` calls) — dimension-guessing alone is unreliable (logos/clip-art mixed in). **View each candidate** before embedding to avoid mislabeling.
- **Self-containment:** base64-inline the chosen figures into the HTML so the file "just opens" anywhere (and validate each data-URI actually decodes). Alternatively an assets folder beside the file — but a single self-contained file is the most robust deliverable.

---

## 9. HTML correctness pitfalls (validate every file)

- **Div-balance bug:** a common slip is closing a container with the wrong tag (e.g. a callout `<div class="bubble">…</p>` closed with a stray `</p>` instead of `</div>`), leaving it unclosed. Browsers auto-close it — so it *renders fine* — but the container silently swallows following content (and in a multi-block file, later sections nest wrong). **Always check `<div>`/`</div>` counts per block.**
- **Math:** balanced `$$` delimiters; balanced `{}` inside each display equation; only valid KaTeX commands (`\\` matrix row-breaks are false positives in naive scanners). Confirm KaTeX actually renders (count `.katex` / `.katex-error` elements via JS) — a wrong command silently fails.
- **Images:** every referenced image exists / every base64 data-URI decodes to a valid image signature; zero unresolved relative refs in a "self-contained" file.
- **Structure:** exactly one takeaway banner + one quiz per lecture; correct page count; each block starts/ends with its page wrapper.
- **Preview may be unavailable** (a stuck browser pane, or file→`data:` snapshots that block relative paths/CDN). Fall back to **static validation** (the checks above) and JS introspection rather than screenshots.

---

## 10. Pre-delivery checklist (run before saying "done")

**Content**
- [ ] Every lecture's transcript concepts covered; no whole method dropped (G1).
- [ ] For every concept, the exact operational formula/criterion a question would use is present (G2).
- [ ] All non-trivial math cross-checked vs a standard reference; DOF counts re-derived; read-off-the-matrix claims tested (G3).
- [ ] Worked examples: real-and-verified or clearly-illustrative, never ambiguous (G4).
- [ ] Instructor's named terms in bold (G5); canonical variants named (G6).
- [ ] Cumulative-assessment recap boxes where a unit's assignment spans earlier units (G7).
- [ ] Look-ahead boxes for deferred-but-tested topics (G8); prerequisite refreshers where reasonable (G9).
- [ ] One worked example + one quiz per lecture; comparison tables where ≥2 things contrast.

**Verification**
- [ ] Pass A (per-lecture adversarial review vs transcript) run; all findings triaged.
- [ ] Pass B (coverage vs the actual assignments/past papers) run; every question sufficient or fair-prerequisite.
- [ ] All patches applied and re-validated.

**Technical**
- [ ] Per-file: div-balanced, `$$`-balanced, valid KaTeX, one banner+quiz/lecture, correct page count.
- [ ] Real figures embedded where flagged; all images decode; self-contained (no unresolved refs).
- [ ] Rendering confirmed (visually, or via `.katex`/`.katex-error` counts + static checks if the browser is unavailable).

**Honesty in the hand-off**
- [ ] State what's covered vs any residual minor enrichments.
- [ ] Note that verification was AI-assisted (thorough, not infallible) and recommend working the assignments (which often include solutions) as the final self-check.
- [ ] Flag anything genuinely beyond the provided lectures (assigned textbook sections, tutorials) that the notes can't cover.

---

### One-line summary
**Re-teach everything the instructor taught, write the exact formula each question needs, verify twice (against the transcript *and* against the real assignments), keep the math correct and the terminology named — and author directly, not via fragile background generation.**
