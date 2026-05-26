import re

TG_MAIN = 'https://t.me/atomexchange_manager'
YANDEX_UFA   = 'https://yandex.com/maps/org/atom_exchange/158423731194/?ll=55.944020%2C54.724120&z=17.63'
YANDEX_KAZAN = 'https://yandex.com/maps/org/atom_exchange/29547548182/?ll=49.110706%2C55.792893&z=17.63'

SUBDOMAIN_PAGES = ['ufa.html', 'kazan.html', 'ekb.html']
ALL_PAGES = [
    'index.html', 'ufa.html', 'kazan.html', 'ekb.html',
    'rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html'
]

NEW_CRYPTO_CARDS = """          <div class="service-card">
            <span class="service-icon">✕</span>
            <span class="service-name">Обмен XRP</span>
            <span class="service-tag">RUB ↔ XRP</span>
            <a href="{tg}" class="btn-ask-rate btn-ask-rate--sm" target="_blank" rel="noopener">Узнать курс в моменте</a>
          </div>
          <div class="service-card">
            <span class="service-icon">⚡</span>
            <span class="service-name">Обмен TRX</span>
            <span class="service-tag">RUB ↔ TRX</span>
            <a href="{tg}" class="btn-ask-rate btn-ask-rate--sm" target="_blank" rel="noopener">Узнать курс в моменте</a>
          </div>
          <div class="service-card">
            <span class="service-icon">🔴</span>
            <span class="service-name">Обмен AVAX</span>
            <span class="service-tag">RUB ↔ AVAX</span>
            <a href="{tg}" class="btn-ask-rate btn-ask-rate--sm" target="_blank" rel="noopener">Узнать курс в моменте</a>
          </div>
          <div class="service-card">
            <span class="service-icon">Ð</span>
            <span class="service-name">Обмен DOGE</span>
            <span class="service-tag">RUB ↔ DOGE</span>
            <a href="{tg}" class="btn-ask-rate btn-ask-rate--sm" target="_blank" rel="noopener">Узнать курс в моменте</a>
          </div>""".replace('{tg}', TG_MAIN)

# Yandex button styled as a proper button
YANDEX_BTN_UFA = (
    f'<a href="{YANDEX_UFA}" target="_blank" rel="noopener" '
    'style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;'
    'border-radius:10px;background:rgba(255,50,0,0.08);border:1px solid rgba(255,50,0,0.3);'
    'color:#ff3200;font-size:13px;font-weight:600;text-decoration:none;margin-bottom:16px;">'
    '📍 Открыть в Яндекс Картах ↗</a>'
)
YANDEX_BTN_KAZAN = (
    f'<a href="{YANDEX_KAZAN}" target="_blank" rel="noopener" '
    'style="display:inline-flex;align-items:center;gap:8px;padding:10px 18px;'
    'border-radius:10px;background:rgba(255,50,0,0.08);border:1px solid rgba(255,50,0,0.3);'
    'color:#ff3200;font-size:13px;font-weight:600;text-decoration:none;margin-bottom:16px;">'
    '📍 Открыть в Яндекс Картах ↗</a>'
)
# index.html office cards yandex links
YANDEX_LINK_UFA_INDEX = (
    f'<a href="{YANDEX_UFA}" class="office-link" target="_blank" rel="noopener" '
    'style="display:inline-flex;align-items:center;gap:6px;opacity:1;'
    'background:rgba(255,50,0,0.08);border:1px solid rgba(255,50,0,0.25);'
    'color:#ff3200;font-size:12px;font-weight:600;border-radius:8px;padding:6px 12px;'
    'text-decoration:none;">📍 Яндекс Карты ↗</a>'
)
YANDEX_LINK_KAZAN_INDEX = (
    f'<a href="{YANDEX_KAZAN}" class="office-link" target="_blank" rel="noopener" '
    'style="display:inline-flex;align-items:center;gap:6px;opacity:1;'
    'background:rgba(255,50,0,0.08);border:1px solid rgba(255,50,0,0.25);'
    'color:#ff3200;font-size:12px;font-weight:600;border-radius:8px;padding:6px 12px;'
    'text-decoration:none;">📍 Яндекс Карты ↗</a>'
)

# Photo CSS fix: landscape aspect ratio + overflow clip on wrapper
GALLERY_CSS_OVERRIDE = """
    /* gallery-fix v6: landscape ratio */
    .gallery-carousel-img { flex: 0 0 calc(50% - 6px) !important; scroll-snap-align: start; border-radius: 12px; aspect-ratio: 4/3 !important; object-fit: cover; display: block; }
    @media (max-width: 600px) { .gallery-carousel-img { flex: 0 0 82% !important; } }
    .gallery-carousel-wrap { overflow: hidden; border-radius: 12px; }
"""


# ── 1. Fix photo aspect ratio + gallery wrapper overflow ──────────────────────
def fix_gallery_css(html):
    if 'gallery-fix v6' in html:
        return html
    # Replace old aspect-ratio:3/4 → 4/3 in existing rules
    html = html.replace('aspect-ratio: 3/4; object-fit: cover; border-radius: 16px; display: block; }',
                        'aspect-ratio: 4/3; object-fit: cover; border-radius: 12px; display: block; }')
    html = html.replace('aspect-ratio: 3/4; object-fit: cover; border-radius: 12px; display: block; }',
                        'aspect-ratio: 4/3; object-fit: cover; border-radius: 12px; display: block; }')
    # Inject override before </head>
    html = html.replace('</head>', f'  <style>{GALLERY_CSS_OVERRIDE}  </style>\n</head>', 1)
    # Add overflow:hidden to carousel wrapper div
    html = html.replace(
        '<div style="position:relative;"><div class="gallery-carousel-track"',
        '<div style="position:relative;overflow:hidden;border-radius:12px;"><div class="gallery-carousel-track"'
    )
    return html


# ── 2. Add XRP/TRX/AVAX/DOGE crypto cards to subdomain services ───────────────
def add_crypto_subdomain(html):
    if 'Обмен XRP' in html:
        return html
    return html.replace(
        '          </div>\n        </div>\n        </div>\n      </div>\n<div style="text-align:center',
        '          </div>\n' + NEW_CRYPTO_CARDS + '\n        </div>\n        </div>\n      </div>\n<div style="text-align:center',
        1
    )


# ── 3. Restyle Yandex Maps buttons to red branded buttons ─────────────────────
OLD_YANDEX_UFA_LINK = (
    f'<a href="{YANDEX_UFA}" target="_blank" rel="noopener" '
    'style="font-size:13px;color:#5b8aff;opacity:0.75;display:inline-block;margin-bottom:12px;">'
    '📍 Открыть в Яндекс Картах ↗</a>'
)
OLD_YANDEX_KAZAN_LINK = (
    f'<a href="{YANDEX_KAZAN}" target="_blank" rel="noopener" '
    'style="font-size:13px;color:#5b8aff;opacity:0.75;display:inline-block;margin-bottom:12px;">'
    '📍 Открыть в Яндекс Картах ↗</a>'
)
# index.html old-style yandex links in office cards
OLD_YANDEX_UFA_INDEX = (
    f'<a href="{YANDEX_UFA}" class="office-link" target="_blank" rel="noopener" '
    'style="opacity:0.65;font-size:13px;">Открыть в Яндекс Картах ↗</a>'
)
OLD_YANDEX_KAZAN_INDEX = (
    f'<a href="{YANDEX_KAZAN}" class="office-link" target="_blank" rel="noopener" '
    'style="opacity:0.65;font-size:13px;">Открыть в Яндекс Картах ↗</a>'
)


def restyle_yandex_buttons(html, page):
    if page == 'ufa.html':
        html = html.replace(OLD_YANDEX_UFA_LINK, YANDEX_BTN_UFA)
    elif page == 'kazan.html':
        html = html.replace(OLD_YANDEX_KAZAN_LINK, YANDEX_BTN_KAZAN)
    elif page == 'index.html':
        html = html.replace(OLD_YANDEX_UFA_INDEX, YANDEX_LINK_UFA_INDEX)
        html = html.replace(OLD_YANDEX_KAZAN_INDEX, YANDEX_LINK_KAZAN_INDEX)
    return html


# ── Apply ──────────────────────────────────────────────────────────────────────

# Gallery CSS fix: ufa + kazan (they have the gallery carousel)
for fname in ['ufa.html', 'kazan.html']:
    with open(fname, encoding='utf-8') as f:
        html = f.read()
    html = fix_gallery_css(html)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} gallery css done')

# Add crypto + restyle yandex on subdomains
for fname in SUBDOMAIN_PAGES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()
    html = add_crypto_subdomain(html)
    html = restyle_yandex_buttons(html, fname)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} crypto + yandex done')

# Restyle yandex on index.html
with open('index.html', encoding='utf-8') as f:
    html = f.read()
html = restyle_yandex_buttons(html, 'index.html')
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html yandex restyled')

print('All done.')
