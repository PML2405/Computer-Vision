# 🛠️ PDF extraction tools (pure Python, no dependencies)

Use these **only when your source is a PDF** whose text/figures you need to pull out — they
need no `pip install`, no poppler, no network (built because those were all unavailable). If
your material is already text, or you can read the slides directly, you don't need them.

Run with any Python 3: `python3 tools/<script>.py …`

| Script | Usage | What it does |
|---|---|---|
| **`pdf_text2.py`** | `pdf_text2.py FILE.pdf OUT.txt [start] [end]` | Page-**ordered**, font-aware text extraction. Handles object streams (`/ObjStm`), the page tree, `/ToUnicode` CMaps, and both TrueType (1-byte) and CID/Type0 (2-byte) fonts, with TJ-kerning-aware spacing. Optional `start`/`end` page indices. **Use it for transcripts and slide text.** |
| **`extract_images.py`** | `extract_images.py FILE.pdf OUTDIR [minpx]` | Dumps embedded raster figures: JPEG (`DCTDecode`) written directly as `.jpg`; other bitmaps (`FlateDecode` RGB/Gray) reconstructed to `.png`. `minpx` skips tiny icons/logos below that pixel size. |
| **`map_figures.py`** | `map_figures.py SLIDE.pdf` | Maps each image XObject to the slide **page that uses it** (via the page's `Do` operators). Prints `obj → page`. Imports `pdf_text2.py` from this same folder. |

## Practical notes (from real use)
- **Transcript = ground truth of what was taught** (spoken narration, in order); **slides =
  exact equations, figures, structure.** Use both.
- **Inline math extracts badly** even when prose is clean — reconstruct standard equations
  from domain knowledge, then verify (guide gap-class **G3**). Don't paste garbled math.
- **Slides may need reading by eye** (render the PDF) when text extraction garbles a diagram
  or equation — the tools get you the prose and the raster figures, not a perfect layout.
- **Figures:** don't trust size alone to pick the right image (logos/clip-art are mixed in).
  Run `map_figures.py` to see which page each image belongs to, **view the candidates**, then
  embed only the essential ones (a result on a photo, a before/after) — redraw the rest as SVG.
- **Normalize** extracted transcript text (fix UTF-8-through-latin1 artifacts, en-dashes,
  ligatures, intra-word spacing) before authoring from it.
