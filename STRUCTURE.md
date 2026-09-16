# 📁 Project structure

This repo hosts **iPad-style handwritten study notes** for the NPTEL *Computer Vision*
course (Prof. Jayanta Mukhopadhyay, IIT Kharagpur), plus the reusable kit that produced them.

```
computer-vision/
├── index.html                 ← landing page (GitHub Pages entry point)
├── README.md                  ← the reusable, subject-independent notes kit / prompt
├── NOTES_CREATION_GUIDE.md    ← playbook: gap-classes (G1–G9) + two-pass verification
├── STRUCTURE.md               ← this file
│
├── notes/                     ← THE DELIVERABLES — one self-contained HTML file per week
│   ├── week1_notes.html       ·  Fundamentals of Image Processing & Image Transforms  (L1–4)
│   ├── week2_notes.html       ·  Projective Geometry & Homography                      (L5–10)
│   ├── week3_notes.html       ·  Camera Geometry — single view                         (L11–15)
│   ├── week4_notes.html       ·  Stereo Geometry — epipolar geom. & fundamental matrix (L16–19)
│   ├── week5_notes.html       ·  Stereo Geometry — estimating F, recovering structure  (L20–23)
│   ├── week6_notes.html       ·  Feature Detection & Description                       (L24–28)
│   └── week7_notes.html       ·  Feature Matching & Model Fitting                      (L29–33)
│
├── source/                    ← original course material (INPUTS, not published — see .gitignore)
│   ├── slides/                ·  per-week lecture-slide PDFs + the full-course master PDF
│   └── assignments/           ·  Week1–6 assignment PDFs
│
├── reference/                 ← the style guide + a friend's exemplar the look is based on
│   ├── NOTES_STYLE_GUIDE.md
│   └── discriminative_mindset_notes.html
│
└── .build/                    ← generation machinery (hidden; kept out of the published site)
    ├── tools/                 ·  pure-Python PDF extractors + the week assembler
    ├── work/                  ·  intermediate scratch: transcripts, per-lecture HTML blocks,
    │                             raw extracted figures, per-week configs, verification JSON
    └── assets/                ·  curated slide images actually embedded in the notes
```

## Viewing the notes
Open **`index.html`** in any browser, or open a `notes/weekN_notes.html` file directly.
Every notes file is **fully self-contained** (all images are base64-inlined); only KaTeX (math)
and the Google Fonts load from a CDN, so an internet connection makes the math render but is not
needed for the text/figures.

## Hosting (GitHub Pages)
`index.html` is at the repo root and links to `notes/…`, so enabling GitHub Pages on the default
branch (root) serves the whole site with no build step.

## Regenerating a week (optional)
The notes are already built; to rebuild one from its lecture blocks:

```bash
python3 .build/tools/assemble_week.py .build/work/week6_cfg.json
```

The assembler is self-locating: it reads the shared shell from `.build/work/exemplar_week1.html`,
stitches the per-lecture blocks from `.build/work/weekN_blocks/`, base64-inlines any
`weekN_assets/…` images from `.build/assets/`, and writes the finished file to `notes/`.

## What is *not* committed
See `.gitignore` — the large/copyrighted source PDFs (`source/slides/`) and the `.build/` scratch
stay local. The published repo is just the site (`index.html` + `notes/`) and the docs.
The assignment PDFs and the source material remain on your machine for regeneration.
