import re

TG = 'https://t.me/atomexchange_manager'

# ── CSS additions ──────────────────────────────────────────────────────────────
OFFICES_CSS = """
    /* office photo carousel */
    .office-photo-carousel { position: relative; margin-bottom: 32px; }
    .office-photo-track { display: flex; gap: 12px; overflow-x: auto; scroll-snap-type: x mandatory; scrollbar-width: none; border-radius: 16px; }
    .office-photo-track::-webkit-scrollbar { display: none; }
    .office-photo-slide { flex: 0 0 calc(50% - 6px); scroll-snap-align: start; border-radius: 16px; aspect-ratio: 4/3; object-fit: cover; display: block; }
    .office-photo-nav { display: flex; justify-content: center; gap: 12px; margin-top: 14px; }
    /* office features */
    .office-features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 32px; }
    .office-feature { background: #0c0c0c; border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 18px 16px; display: flex; align-items: center; gap: 12px; }
    .office-feature-icon { font-size: 22px; flex-shrink: 0; }
    .office-feature-text { font-size: 13px; font-weight: 600; color: rgba(240,240,240,0.8); line-height: 1.4; }
    @media (max-width: 700px) {
      .office-photo-slide { flex: 0 0 85%; }
      .office-features { grid-template-columns: 1fr 1fr; }
    }
"""

NEW_OFFICES_SECTION = f"""    <!-- ═══════════════════════════════════════ OFFICES ═══ -->
    <section class="section offices" id="offices" aria-labelledby="offices-title">
      <div class="container">
        <div class="section-head">
          <h2 class="section-title" id="offices-title">Наши офисы</h2>
        </div>

        <!-- Photo carousel -->
        <div class="office-photo-carousel">
          <div class="office-photo-track" id="office-photo-track">
            <img class="office-photo-slide" src="photos/ufa/office_1.png" alt="Офис Уфа" loading="lazy">
            <img class="office-photo-slide" src="photos/ufa/office_2.png" alt="Офис Уфа" loading="lazy">
            <img class="office-photo-slide" src="photos/ufa/office_3.png" alt="Офис Уфа" loading="lazy">
            <img class="office-photo-slide" src="photos/ufa/office_4.png" alt="Офис Уфа" loading="lazy">
            <img class="office-photo-slide" src="photos/ufa/office_5.png" alt="Офис Уфа" loading="lazy">
            <img class="office-photo-slide" src="photos/ufa/office_6.png" alt="Офис Уфа" loading="lazy">
            <img class="office-photo-slide" src="photos/kazan/office_1.png" alt="Офис Казань" loading="lazy">
            <img class="office-photo-slide" src="photos/kazan/office_2.png" alt="Офис Казань" loading="lazy">
            <img class="office-photo-slide" src="photos/kazan/office_3.png" alt="Офис Казань" loading="lazy">
            <img class="office-photo-slide" src="photos/kazan/office_4.png" alt="Офис Казань" loading="lazy">
            <img class="office-photo-slide" src="photos/kazan/office_5.png" alt="Офис Казань" loading="lazy">
            <img class="office-photo-slide" src="photos/kazan/office_6.png" alt="Офис Казань" loading="lazy">
          </div>
          <div class="office-photo-nav">
            <button class="carousel-btn" onclick="officeScroll(-1)">←</button>
            <button class="carousel-btn" onclick="officeScroll(1)">→</button>
          </div>
        </div>

        <!-- Feature teasers -->
        <div class="office-features">
          <div class="office-feature">
            <span class="office-feature-icon">👥</span>
            <span class="office-feature-text">Подходим всем: новичкам и опытным</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">🔒</span>
            <span class="office-feature-text">Безопасно и конфиденциально</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">💰</span>
            <span class="office-feature-text">С нами выгодно</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">⏱</span>
            <span class="office-feature-text">С заботой о времени</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">🏆</span>
            <span class="office-feature-text">Большая команда с отлаженными процессами</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">⭐</span>
            <span class="office-feature-text">Высокий сервис</span>
          </div>
        </div>

        <!-- Office address cards -->
        <div class="office-cards">
          <article class="office-card">
            <h3 class="office-city">Уфа</h3>
            <p class="office-detail">Пн–Сб: 10:00–19:00</p>
            <p class="office-detail">Верхнеторговая площадь, 6, офис 2.5</p>
            <p class="office-note">Прямой обмен · без посредников</p>
            <a href="ufa.html" class="office-link">Страница офиса →</a>
          </article>
          <article class="office-card">
            <h3 class="office-city">Казань</h3>
            <p class="office-detail">Пн–Сб: 10:00–19:00</p>
            <p class="office-detail">ул. Баумана 9А, офис 207</p>
            <p class="office-note">Прямой обмен · без посредников</p>
            <a href="kazan.html" class="office-link">Страница офиса →</a>
          </article>
          <article class="office-card">
            <h3 class="office-city">Екатеринбург</h3>
            <p class="office-detail">Пн–Сб: 10:00–19:00</p>
            <p class="office-detail">Радищева 6А, офис 21103</p>
            <p class="office-note">Прямой обмен · без посредников</p>
            <a href="ekb.html" class="office-link">Страница офиса →</a>
          </article>
        </div>
      </div>
    </section>"""

OFFICE_JS = """  <script>
    function officeScroll(dir) {
      var t = document.getElementById('office-photo-track');
      if (t) t.scrollBy({ left: dir * 320, behavior: 'smooth' });
    }
  </script>"""

FEATURE_TEASERS_HTML = """        <!-- Feature teasers -->
        <div class="office-features">
          <div class="office-feature">
            <span class="office-feature-icon">👥</span>
            <span class="office-feature-text">Подходим всем: новичкам и опытным</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">🔒</span>
            <span class="office-feature-text">Безопасно и конфиденциально</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">💰</span>
            <span class="office-feature-text">С нами выгодно</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">⏱</span>
            <span class="office-feature-text">С заботой о времени</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">🏆</span>
            <span class="office-feature-text">Большая команда с отлаженными процессами</span>
          </div>
          <div class="office-feature">
            <span class="office-feature-icon">⭐</span>
            <span class="office-feature-text">Высокий сервис</span>
          </div>
        </div>
"""


def inject_offices_css(html):
    if 'office-photo-carousel' not in html:
        html = html.replace('</head>', f'  <style>{OFFICES_CSS}  </style>\n</head>', 1)
    return html


def rebuild_index_offices(html):
    # Replace the old canvas-map offices section entirely
    html = re.sub(
        r'    <!-- ═══════════════════════════════════════ OFFICES / MAP ═══ -->.*?</section>',
        NEW_OFFICES_SECTION,
        html, count=1, flags=re.DOTALL
    )
    return html


def inject_office_js(html):
    if 'officeScroll' not in html:
        html = html.replace(
            '  <script src="script.js"></script>',
            OFFICE_JS + '\n  <script src="script.js"></script>',
            1
        )
    return html


def add_features_to_subdomain(html):
    # Insert feature teasers after the gallery-grid closing div
    if '<span class="office-feature-icon">' not in html:
        html = html.replace(
            '        </div>\n      </div>\n    </section>\n    <section class="sub-steps">',
            '        </div>\n' + FEATURE_TEASERS_HTML + '      </div>\n    </section>\n    <section class="sub-steps">',
            1
        )
    return html


def add_features_ekb(html):
    if '<span class="office-feature-icon">' not in html:
        # Insert feature grid as its own section before sub-steps
        FEATURES_SECTION = (
            '\n    <section class="section">\n      <div class="container">\n'
            + FEATURE_TEASERS_HTML
            + '      </div>\n    </section>\n'
        )
        html = html.replace(
            '\n\n    <section class="sub-steps">',
            FEATURES_SECTION + '\n    <section class="sub-steps">',
            1
        )
    return html


# ── index.html ──────────────────────────────────────────────────────────────────
with open('index.html', encoding='utf-8') as f:
    html = f.read()

html = inject_offices_css(html)
html = rebuild_index_offices(html)
html = inject_office_js(html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('index.html done')


# ── ufa.html ────────────────────────────────────────────────────────────────────
with open('ufa.html', encoding='utf-8') as f:
    html = f.read()

html = inject_offices_css(html)
html = add_features_to_subdomain(html)

with open('ufa.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('ufa.html done')


# ── kazan.html ──────────────────────────────────────────────────────────────────
with open('kazan.html', encoding='utf-8') as f:
    html = f.read()

html = inject_offices_css(html)
html = add_features_to_subdomain(html)

with open('kazan.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('kazan.html done')


# ── ekb.html ────────────────────────────────────────────────────────────────────
with open('ekb.html', encoding='utf-8') as f:
    html = f.read()

html = inject_offices_css(html)
html = add_features_ekb(html)

with open('ekb.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('ekb.html done')

print('All done.')
