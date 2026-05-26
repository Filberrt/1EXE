import re

ALL_PAGES = [
    'index.html', 'ufa.html', 'kazan.html', 'ekb.html',
    'rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html'
]
GALLERY_PAGES = ['ufa.html', 'kazan.html']

# ── 1. Founder section: bigger photo + paragraph break ────────────────────────
FOUNDER_CSS_OVERRIDE = """
    /* founder-fix v7 */
    .founder-photo { width: 240px !important; height: 320px !important; border-radius: 20px !important; object-fit: cover !important; object-position: center top !important; flex-shrink: 0 !important; }
    @media (max-width: 900px) {
      .founder-photo { width: 100% !important; height: 220px !important; border-radius: 16px !important; }
      .founder-card { align-items: flex-start !important; }
      .founder-quote { font-size: 15px !important; }
    }
"""

def fix_founder(html):
    if 'founder-fix v7' in html:
        return html
    # Inject CSS
    html = html.replace('</head>', f'  <style>{FOUNDER_CSS_OVERRIDE}  </style>\n</head>', 1)
    # Add paragraph break before «Мы» in the quote
    html = html.replace(
        'а на доверии. Мы создаём',
        'а на доверии.<br><br>Мы создаём'
    )
    return html


# ── 2. Hero mobile fix: remove full-height ────────────────────────────────────
HERO_MOBILE_CSS = """
    /* hero-mobile-fix v7 */
    @media (max-width: 768px) {
      .hero { min-height: auto !important; align-items: flex-start !important; padding-top: 96px !important; padding-bottom: 48px !important; }
    }
"""

def fix_hero_mobile(html):
    if 'hero-mobile-fix v7' in html:
        return html
    html = html.replace('</head>', f'  <style>{HERO_MOBILE_CSS}  </style>\n</head>', 1)
    return html


# ── 3. Gallery photos: use vw units on mobile, ensure track width ─────────────
GALLERY_MOBILE_CSS = """
    /* gallery-mobile-fix v7 */
    #gallery-track { width: 100% !important; box-sizing: border-box; }
    @media (max-width: 600px) {
      .gallery-carousel-img { flex: 0 0 78vw !important; max-width: 78vw !important; min-width: 0 !important; aspect-ratio: 4/3 !important; }
    }
    @media (min-width: 601px) {
      .gallery-carousel-img { flex: 0 0 calc(48% - 6px) !important; max-width: calc(48% - 6px) !important; aspect-ratio: 4/3 !important; }
    }
"""

def fix_gallery_mobile(html):
    if 'gallery-mobile-fix v7' in html:
        return html
    html = html.replace('</head>', f'  <style>{GALLERY_MOBILE_CSS}  </style>\n</head>', 1)
    return html


# ── 4. Sub-steps mobile redesign ──────────────────────────────────────────────
SUB_STEPS_MOBILE_CSS = """
    /* sub-steps-mobile v7 */
    @media (max-width: 700px) {
      .sub-steps-grid { grid-template-columns: 1fr !important; gap: 12px !important; }
      .sub-step-card { flex-direction: row !important; align-items: stretch !important; min-height: 110px; }
      .sub-step-photo { width: 110px !important; min-width: 110px !important; flex-shrink: 0 !important; }
      .sub-step-photo img { height: 100% !important; min-height: 110px !important; width: 100% !important; object-fit: cover !important; }
      .sub-step-body { padding: 14px 14px 14px !important; display: flex; flex-direction: column; justify-content: center; }
      .sub-step-badge { font-size: 22px !important; }
      .sub-step-tag { font-size: 9px !important; }
      .sub-step-title { font-size: 13px !important; margin-bottom: 4px !important; }
      .sub-step-text { font-size: 11px !important; }
      .sub-step-overlay { padding: 8px !important; gap: 4px !important; }
    }
"""

def fix_sub_steps_mobile(html):
    if 'sub-steps-mobile v7' in html:
        return html
    html = html.replace('</head>', f'  <style>{SUB_STEPS_MOBILE_CSS}  </style>\n</head>', 1)
    return html


# ── Apply ──────────────────────────────────────────────────────────────────────

# Founder + hero mobile fix → index.html only
with open('index.html', encoding='utf-8') as f:
    html = f.read()
html = fix_founder(html)
html = fix_hero_mobile(html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html done')

# Hero mobile fix on all other pages (subdomains have their own hero)
for fname in ['ufa.html', 'kazan.html', 'ekb.html', 'rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html']:
    with open(fname, encoding='utf-8') as f:
        html = f.read()
    html = fix_hero_mobile(html)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} hero mobile done')

# Gallery photo fix → ufa + kazan
for fname in GALLERY_PAGES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()
    html = fix_gallery_mobile(html)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} gallery mobile done')

# Sub-steps redesign → ufa + kazan (they have фотоинструкция)
for fname in GALLERY_PAGES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()
    html = fix_sub_steps_mobile(html)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} sub-steps mobile done')

print('All done.')
