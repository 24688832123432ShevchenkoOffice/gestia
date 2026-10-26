# Iteration 2 — fix diffs vs Figma (compare ~/gestia_shots/site_desktop_1440.png with docs/figma/figma_desktop_1440.png; script ~/gestia_shots/shot.mjs, server at http://127.0.0.1:8765 may be running; re-run `node ~/gestia_shots/shot.mjs` from ~/gestia_shots to re-screenshot and visually compare yourself). Same rules as docs/figma/BRIEF.md (invent nothing). Do not commit.
Desktop 1440:
1. Page height is 6795 vs Figma 6678 (+117) and scrollWidth 1441 (should be 1440, no horizontal page scroll). Find where vertical extra comes from and match Figma section y-positions from desktop/design_context.tsx.txt (absolute top values).
2. Hero image crop differs: Figma shows the whole garden scene (trees, grass at top, tables, chairs) — site shows zoomed-in chairs. Reproduce Figma's exact image box (size/offset/object-position from design_context "Hero Image" node and the image node inside) for hero AND the middle full-width image AND the video block image (same issue).
3. Callback title «Замовити зворотний дзвінок» wraps into 2 lines on site but is 1 line in Figma — fix width/size per Figma. Also advantage descriptions wrap differently (Figma widths per text node). Check all text box widths against Figma.
4. Keep mobile (393) unchanged except obvious diffs vs docs/figma/figma_mobile_393.png.
Run check+tests at the end; print short summary.
