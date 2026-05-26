import re

TG_BANAEV = 'https://t.me/Banaev_as'
TG_MAIN   = 'https://t.me/atomexchange_manager'

YANDEX_UFA   = 'https://yandex.com/maps/org/atom_exchange/158423731194/?ll=55.944020%2C54.724120&z=17.63'
YANDEX_KAZAN = 'https://yandex.com/maps/org/atom_exchange/29547548182/?ll=49.110706%2C55.792893&z=17.63'

ALL_PAGES = [
    'index.html', 'ufa.html', 'kazan.html', 'ekb.html',
    'rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html'
]

# ── 1. Fix Alexander TG link (index.html only – founder section) ───────────────
def fix_alexander_tg(html):
    # Only the "Связаться с Александром" button, not other TG links
    return html.replace(
        f'<a href="{TG_MAIN}" class="btn-primary" target="_blank" rel="noopener">Связаться с Александром</a>',
        f'<a href="{TG_BANAEV}" class="btn-primary" target="_blank" rel="noopener">Связаться с Александром</a>',
        1
    )


# ── 2. Add Yandex Maps links to office cards in index.html ────────────────────
def add_yandex_maps_index(html):
    if YANDEX_UFA in html:
        return html
    html = html.replace(
        '<a href="ufa.html" class="office-link">Страница офиса →</a>',
        '<a href="ufa.html" class="office-link">Страница офиса →</a>\n'
        f'            <a href="{YANDEX_UFA}" class="office-link" target="_blank" rel="noopener" style="opacity:0.65;font-size:13px;">Открыть в Яндекс Картах ↗</a>',
        1
    )
    html = html.replace(
        '<a href="kazan.html" class="office-link">Страница офиса →</a>',
        '<a href="kazan.html" class="office-link">Страница офиса →</a>\n'
        f'            <a href="{YANDEX_KAZAN}" class="office-link" target="_blank" rel="noopener" style="opacity:0.65;font-size:13px;">Открыть в Яндекс Картах ↗</a>',
        1
    )
    return html


# ── 2b. Add Yandex Maps link inside ufa.html gallery section ──────────────────
def add_yandex_maps_ufa(html):
    if YANDEX_UFA in html:
        return html
    html = html.replace(
        '<div class="gallery-address">',
        '<div class="gallery-address" style="display:flex;align-items:center;gap:16px;flex-wrap:wrap;">',
        1
    )
    # Insert link after the address div closing tag
    html = re.sub(
        r'(</div>\s*\n\s*<div style="position:relative;">)',
        f'</div>\n        <a href="{YANDEX_UFA}" target="_blank" rel="noopener" style="font-size:13px;color:#5b8aff;opacity:0.75;display:inline-block;margin-bottom:12px;">📍 Открыть в Яндекс Картах ↗</a>\n        <div style="position:relative;">',
        html, count=1
    )
    return html


# ── 2c. Add Yandex Maps link inside kazan.html gallery section ────────────────
def add_yandex_maps_kazan(html):
    if YANDEX_KAZAN in html:
        return html
    html = re.sub(
        r'(</div>\s*\n\s*<div style="position:relative;">)',
        f'</div>\n        <a href="{YANDEX_KAZAN}" target="_blank" rel="noopener" style="font-size:13px;color:#5b8aff;opacity:0.75;display:inline-block;margin-bottom:12px;">📍 Открыть в Яндекс Картах ↗</a>\n        <div style="position:relative;">',
        html, count=1
    )
    return html


# ── 3. Add more crypto cards to services grid ─────────────────────────────────
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

def add_crypto_cards(html):
    if 'Обмен XRP' in html:
        return html
    # Keep SOL card's </div>, insert new cards after it, then close the grid
    html = html.replace(
        '          </div>\n        </div>\n        </div>\n      </div>\n<div style="text-align:center',
        '          </div>\n' + NEW_CRYPTO_CARDS + '\n        </div>\n        </div>\n      </div>\n<div style="text-align:center',
        1
    )
    return html


# ── 4. Fix carousel: use dynamic image width for reliable scrolling ────────────
BETTER_CAROUSEL_JS = """  <script>
    function reviewsScroll(dir) {
      var t = document.getElementById('reviews-track');
      if (!t) return;
      var card = t.querySelector('.review-card');
      var step = card ? card.offsetWidth + 16 : 320;
      t.scrollLeft += dir * step;
    }
    function galleryScroll(dir) {
      var t = document.getElementById('gallery-track');
      if (!t) return;
      var img = t.querySelector('img');
      var step = img ? img.offsetWidth + 12 : 300;
      t.scrollLeft += dir * step;
    }
    function articlesScroll(dir) {
      var t = document.getElementById('articles-track');
      if (!t) return;
      var card = t.querySelector('.article-card');
      var step = card ? card.offsetWidth + 16 : 280;
      t.scrollLeft += dir * step;
    }
    function officeScroll(dir) {
      var t = document.getElementById('office-photo-track');
      if (!t) return;
      var img = t.querySelector('img');
      var step = img ? img.offsetWidth + 12 : 320;
      t.scrollLeft += dir * step;
    }
  </script>"""

def upgrade_carousel_js(html):
    # Remove all old carousel script blocks
    html = re.sub(
        r'\s*<script>\s*function reviewsScroll.*?</script>',
        '', html, flags=re.DOTALL
    )
    html = re.sub(
        r'\s*<script>\s*function galleryScroll.*?</script>',
        '', html, flags=re.DOTALL
    )
    html = re.sub(
        r'\s*<script>\s*function officeScroll.*?</script>',
        '', html, flags=re.DOTALL
    )
    # Inject new consolidated block before script.js
    html = html.replace(
        '  <script src="script.js"></script>',
        BETTER_CAROUSEL_JS + '\n  <script src="script.js"></script>',
        1
    )
    return html


# ── Apply ──────────────────────────────────────────────────────────────────────
# All pages: upgrade carousel JS
for fname in ALL_PAGES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()
    html = upgrade_carousel_js(html)
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} js done')

# index.html: Alexander TG, Yandex Maps, extra crypto cards
with open('index.html', encoding='utf-8') as f:
    html = f.read()
html = fix_alexander_tg(html)
html = add_yandex_maps_index(html)
html = add_crypto_cards(html)
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html extras done')

# ufa.html: Yandex Maps
with open('ufa.html', encoding='utf-8') as f:
    html = f.read()
html = add_yandex_maps_ufa(html)
with open('ufa.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('ufa.html yandex done')

# kazan.html: Yandex Maps
with open('kazan.html', encoding='utf-8') as f:
    html = f.read()
html = add_yandex_maps_kazan(html)
with open('kazan.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('kazan.html yandex done')

print('All done.')
