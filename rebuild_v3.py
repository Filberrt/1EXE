import re

ALL_PAGES = [
    'index.html', 'ufa.html', 'kazan.html', 'ekb.html',
    'rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html'
]

MAP_HTML = """        <!-- Map -->
        <div class="map-wrap" role="img" aria-label="Карта офисов Atom Exchange в России">
          <canvas id="map-canvas" aria-hidden="true"></canvas>

          <div class="map-pin p-ufa" data-city="ufa" tabindex="0" role="button" aria-label="Офис в Уфе">
            <span class="pin-dot"></span>
            Уфа
          </div>
          <div class="map-pin p-kzn" data-city="kazan" tabindex="0" role="button" aria-label="Офис в Казани">
            <span class="pin-dot"></span>
            Казань
          </div>
          <div class="map-pin p-ekb" data-city="ekb" tabindex="0" role="button" aria-label="Офис в Екатеринбурге">
            <span class="pin-dot"></span>
            Екатеринбург
          </div>

          <div class="map-popup" id="popup-ufa" role="dialog" aria-label="Офис Уфа">
            <div class="popup-city">Уфа</div>
            <div class="popup-addr">Верхнеторговая площадь, 6, офис 2.5</div>
            <div class="popup-hours" id="status-ufa">
              <span class="hours-dot"></span>
              <span class="hours-text">Пн–Сб: 10:00–19:00</span>
            </div>
            <a href="ufa.html" class="popup-link">Перейти на страницу →</a>
          </div>
          <div class="map-popup" id="popup-kazan" role="dialog" aria-label="Офис Казань">
            <div class="popup-city">Казань</div>
            <div class="popup-addr">ул. Баумана 9А, 2 этаж, офис 207</div>
            <div class="popup-hours" id="status-kazan">
              <span class="hours-dot"></span>
              <span class="hours-text">Пн–Сб: 10:00–19:00</span>
            </div>
            <a href="kazan.html" class="popup-link">Перейти на страницу →</a>
          </div>
          <div class="map-popup" id="popup-ekb" role="dialog" aria-label="Офис Екатеринбург">
            <div class="popup-city">Екатеринбург</div>
            <div class="popup-addr">Радищева 6А, 11 этаж, офис 21103</div>
            <div class="popup-hours" id="status-ekb">
              <span class="hours-dot"></span>
              <span class="hours-text">Пн–Сб: 10:00–19:00</span>
            </div>
            <a href="ekb.html" class="popup-link">Перейти на страницу →</a>
          </div>
        </div>

"""

GALLERY_CAROUSEL_CSS = """
    /* gallery carousel v3 */
    .gallery-carousel-track { display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; border-radius: 16px; }
    .gallery-carousel-track::-webkit-scrollbar { display: none; }
    .gallery-carousel-img { flex: 0 0 calc(50% - 6px); scroll-snap-align: start; border-radius: 16px; aspect-ratio: 3/4; object-fit: cover; display: block; }
    .gallery-carousel-nav { display: flex; justify-content: center; gap: 12px; margin-top: 14px; }
    @media (max-width: 600px) { .gallery-carousel-img { flex: 0 0 85%; } }
"""

GALLERY_JS = """  <script>
    function galleryScroll(dir) {
      var t = document.getElementById('gallery-track');
      if (t) t.scrollBy({ left: dir * 360, behavior: 'smooth' });
    }
  </script>"""


# ── 1. Remove desktop nav dropdown (Клиентам) ─────────────────────────────────
def remove_nav_dropdown(html):
    return re.sub(
        r'\n\s{8}<div class="nav-dropdown"[^>]*>.*?\n\s{8}</div>',
        '',
        html, count=1, flags=re.DOTALL
    )


# ── 2. Remove mobile nav direction links + divider ────────────────────────────
def remove_mobile_nav_directions(html):
    return re.sub(
        r'\n\s*<div class="mobile-nav-divider">[^<]+</div>.*?<a href="perevody\.html[^"]*"[^>]*>[^<]*</a>',
        '',
        html, count=1, flags=re.DOTALL
    )


# ── 3. Remove section-cta-row (Написать + Позвонить buttons below sections) ──
def remove_section_cta_rows(html):
    return re.sub(
        r'\n?<div class="section-cta-row">.*?</div>',
        '',
        html, flags=re.DOTALL
    )


# ── 4. Remove footer Клиентам nav section ────────────────────────────────────
def remove_footer_clients_nav(html):
    return re.sub(
        r'\n\s*<nav class="footer-nav"[^>]*aria-label="[Кк]лиентам"[^>]*>.*?</nav>',
        '',
        html, count=1, flags=re.DOTALL
    )


# ── 5. Restore Russia map in index.html offices section ───────────────────────
def restore_map_in_index(html):
    # Replace the photo carousel block (between section-head and feature teasers)
    html = re.sub(
        r'(\s*<!-- Photo carousel -->.*?)(?=\s*<!-- Feature teasers -->)',
        '\n' + MAP_HTML,
        html, count=1, flags=re.DOTALL
    )
    return html


# ── 6. Convert gallery grid to carousel in subdomain pages ───────────────────
def make_gallery_carousel(html):
    def replace_grid(m):
        inner = m.group(1)
        return (
            '<div style="position:relative;">'
            '<div class="gallery-carousel-track" id="gallery-track">'
            + inner +
            '</div>'
            '<div class="gallery-carousel-nav">'
            '<button class="carousel-btn" onclick="galleryScroll(-1)">←</button>'
            '<button class="carousel-btn" onclick="galleryScroll(1)">→</button>'
            '</div></div>'
        )
    html = re.sub(r'<div class="gallery-grid">(.*?)</div>', replace_grid, html, count=1, flags=re.DOTALL)
    html = html.replace('class="gallery-img"', 'class="gallery-carousel-img"')
    return html


def inject_gallery_css(html):
    if 'gallery-carousel-track' not in html:
        html = html.replace('</head>', f'  <style>{GALLERY_CAROUSEL_CSS}  </style>\n</head>', 1)
    return html


def inject_gallery_js(html):
    if 'galleryScroll' not in html:
        html = html.replace(
            '  <script src="script.js"></script>',
            GALLERY_JS + '\n  <script src="script.js"></script>',
            1
        )
    return html


# ── Apply base changes to all pages ───────────────────────────────────────────
for fname in ALL_PAGES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()

    html = remove_nav_dropdown(html)
    html = remove_mobile_nav_directions(html)
    html = remove_section_cta_rows(html)
    html = remove_footer_clients_nav(html)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} base done')


# ── index.html: restore canvas map ────────────────────────────────────────────
with open('index.html', encoding='utf-8') as f:
    html = f.read()

html = restore_map_in_index(html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html map restored')


# ── ufa.html, kazan.html: gallery carousel ────────────────────────────────────
for fname in ['ufa.html', 'kazan.html']:
    with open(fname, encoding='utf-8') as f:
        html = f.read()

    html = inject_gallery_css(html)
    html = make_gallery_carousel(html)
    html = inject_gallery_js(html)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} gallery done')

print('All done.')
