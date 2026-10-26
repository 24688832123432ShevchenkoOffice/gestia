# Brief: Gestia home page 1:1 from Figma (Django, vanilla CSS, no Tailwind, no React)

RULE: invent NOTHING. Every color, font, size, spacing, text, image, icon comes from Figma sources below. If something is not in Figma, do NOT invent it; add it to docs/figma/OPEN_QUESTIONS.md.

## Sources (all in docs/figma/)
- gestia_home_build_spec.md — structured spec (container 1302, margins 69, 4 cols x303, gutter 30, Inter 400/500 only, radius 0, no shadows). READ IT FULLY.
- desktop/design_context.tsx.txt — Figma-generated React+Tailwind reference for desktop «Головна» node 130:23071, 1440x6678. Asset files referenced as `${assetPathPrefix}/<name>` live in docs/figma/desktop/<name>.
- mobile/design_context.tsx.txt — mobile «Головна» 121:14588, 393x6191; assets in docs/figma/mobile/.
- megamenu/ (130:23224, catalog mega-menu open state, desktop), locale_popup/ (130:23959, country/language popup over hero), mobile_burger/ (121:14700 burger menu) — design contexts + assets. Implement these states (menu opens on Каталог click, burger opens on mobile, locale popup on UA/EN click) only as shown.
- Target screenshots: figma_desktop_1440.png, figma_mobile_393.png, figma_desktop_variant_*.png, figma_mobile_burger_393.png.

## Tasks
1. Remove starter design: old templates (templates/content/home.html, partials header/footer, base CSS in src/core/static) replaced by Figma-based ones. Other pages (catalog, product, cart, checkout, about) must keep working (render without errors) using the new base/header/footer; do not redesign them beyond that.
2. Remove demo products: delete src/core/management/commands/seed_demo.py, any fixtures, media/seed; delete demo Product/Category/etc rows and demo content rows from db.sqlite3 (backup exists). Keep models unless the home page needs extra fields; add migrations if so.
3. Content shown in Figma (hero texts, category tiles, popular products, advantages, reviews, section titles, footer contacts) must be editable in admin (existing HomeBlock/Advantage/SiteSettings/Category/Product, plus e.g. a Review model if needed), loaded via a NEW management command `load_figma_content` that creates exactly the Figma texts/prices/images (copy images from docs/figma/* into media via Django File). Not hardcoded in templates. Static icons/logo/svg go to src/core/static/... copied from docs/figma assets (do not edit SVGs, keep width/height attrs).
4. Build the home page pixel-perfect: desktop at 1440 exactly per Figma; mobile at 393 per mobile frame. Breakpoint between them: use a simple switch (e.g. max-width 1439/ 767) — intermediate widths are NOT designed: just keep it sane and note it as an open question. Inter via Google Fonts (400,500).
5. Mockup errors — do NOT silently fix, keep as in Figma where reasonable and list in OPEN_QUESTIONS.md: call-form button text «Перейти до каталогу»; rows wider than container (1562); stray elements (2 icons over hero, line at y≈5060, extra black footer outside frame — do not render the extra footer/stray icons/line, but list). Hover/focus/transitions not in Figma: minimal neutral (e.g. opacity/underline none), list as open question.
6. Video blocks: Figma shows a video icon placeholder over an image — render image + icon as in Figma; real video source = open question.
7. Run `python manage.py check`, `python manage.py test`, migrations, `load_figma_content`. Use .venv/bin/python.
8. Do NOT git push, do NOT deploy, do not touch .env. Do not commit — I will commit.
At the end print a summary: files changed, removed, models/migrations, how to load content, open questions.
