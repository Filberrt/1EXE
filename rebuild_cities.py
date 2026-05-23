import re

NEW_CSS = """
    /* HERO */
    .city-hero {
      padding: 130px 0 80px;
      background: #000;
      position: relative;
      overflow: hidden;
    }
    /* ── Челка: glow + dot grid, точная копия главной страницы ── */
    .city-hero-bg {
      position: absolute;
      inset: 0;
      z-index: 0;
      pointer-events: none;
    }
    .city-hero-glow {
      position: absolute;
      top: -10%;
      left: 50%;
      transform: translateX(-50%);
      width: 900px;
      height: 600px;
      background: radial-gradient(ellipse at center, rgba(91,138,255,0.18) 0%, transparent 65%);
      pointer-events: none;
    }
    .city-hero-dots {
      position: absolute;
      inset: 0;
      background-image: radial-gradient(circle, rgba(255,255,255,0.15) 1px, transparent 1px);
      background-size: 28px 28px;
      mask-image: radial-gradient(ellipse at center, black 40%, transparent 85%);
      -webkit-mask-image: radial-gradient(ellipse at center, black 40%, transparent 85%);
      pointer-events: none;
    }
    /* ВСЁ в одном блоке */
    .city-hero-block {
      position: relative; z-index: 1;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 28px;
      background: rgba(0,0,0,0.30);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      padding: 40px 40px 36px;
      max-width: 680px;
      display: flex; flex-direction: column; align-items: flex-start;
    }
    /* status badge */
    .city-tag {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 6px 16px; border-radius: 100px;
      border: 1px solid rgba(91,138,255,0.22);
      background: rgba(91,138,255,0.07);
      font-size: 13px; font-weight: 600; color: rgba(240,240,240,0.75);
      margin-bottom: 20px;
    }
    .city-dot {
      width: 7px; height: 7px; border-radius: 50%;
      background: #22c55e; box-shadow: 0 0 8px rgba(34,197,94,0.8);
      flex-shrink: 0; transition: background 0.4s, box-shadow 0.4s;
    }
    /* city name крупный */
    .city-location {
      font-size: 32px; font-weight: 700; letter-spacing: 3px;
      text-transform: uppercase; color: #5b8aff;
      margin: 0 0 14px;
    }
    .city-h1 {
      font-family: 'Manrope', sans-serif;
      font-size: clamp(52px, 10vw, 92px);
      font-weight: 800; color: #fff; text-transform: uppercase;
      line-height: 0.92; letter-spacing: -2px; margin: 0 0 20px;
    }
    .city-lead {
      font-size: 15px; color: rgba(240,240,240,0.45);
      margin: 0 0 28px; line-height: 1.5;
      white-space: nowrap;
    }
    .city-block-divider {
      width: 100%; border: none;
      border-top: 1px solid rgba(255,255,255,0.07); margin: 0 0 24px;
    }
    .city-address {
      display: flex; align-items: flex-start; gap: 16px; margin-bottom: 24px;
    }
    .city-address-icon {
      width: 44px; height: 44px; border-radius: 11px;
      background: rgba(91,138,255,0.10);
      border: 1px solid rgba(91,138,255,0.22);
      display: flex; align-items: center; justify-content: center;
      flex-shrink: 0; color: #5b8aff;
    }
    .city-address-label {
      font-size: 10px; font-weight: 700; letter-spacing: 1.2px;
      text-transform: uppercase; color: rgba(240,240,240,0.30); margin: 0 0 6px;
    }
    .city-address-text {
      font-family: 'Manrope', sans-serif; font-size: 20px; font-weight: 700;
      color: #f0f0f0; margin: 0; line-height: 1.3;
    }
    .city-map-btns { display: flex; gap: 12px; flex-wrap: wrap; }
    .city-map-btn {
      display: inline-flex; align-items: center; gap: 8px;
      height: 46px; padding: 0 22px; border-radius: 10px;
      font-size: 14px; font-weight: 600; text-decoration: none;
      transition: all 0.2s; white-space: nowrap;
    }
    .city-map-btn--primary { background: #5b8aff; color: #fff; }
    .city-map-btn--primary:hover { background: #4a76f0; }
    .city-map-btn--outline {
      background: transparent; color: rgba(240,240,240,0.8);
      border: 1px solid rgba(255,255,255,0.15);
    }
    .city-map-btn--outline:hover { border-color: rgba(91,138,255,0.5); color: #fff; }

    /* STEPS SECTION */
    .city-steps { padding: 72px 0 96px; }
    .city-steps-head { margin-bottom: 40px; }
    .city-steps-kicker {
      font-size: 11px; font-weight: 700; letter-spacing: 1.5px;
      text-transform: uppercase; color: #5b8aff; margin: 0 0 10px;
    }
    .city-steps-title {
      font-family: 'Manrope', sans-serif;
      font-size: clamp(28px, 4vw, 44px); font-weight: 800;
      color: #f0f0f0; margin: 0; text-transform: uppercase; letter-spacing: -1px;
    }
    .city-steps-grid {
      display: grid; gap: 18px; align-items: stretch;
    }

    /* STEP CARD */
    .city-step-card {
      border-radius: 20px; overflow: hidden;
      background: #0c0c0c; border: 1px solid rgba(255,255,255,0.07);
      transition: border-color 0.25s, transform 0.25s;
      position: relative; display: flex; flex-direction: column;
    }
    .city-step-card::before {
      content: '';
      position: absolute; top: 0; left: 0; right: 0; height: 2px;
      background: linear-gradient(90deg, #5b8aff, #9b87ff);
      opacity: 0; transition: opacity 0.25s; z-index: 2;
    }
    .city-step-card:hover { border-color: rgba(91,138,255,0.30); transform: translateY(-4px); }
    .city-step-card:hover::before { opacity: 1; }
    .city-step-photo { position: relative; flex-shrink: 0; }
    .city-step-photo img {
      width: 100%; height: 470px; object-fit: cover; display: block;
    }
    .city-step-overlay {
      position: absolute; bottom: 0; left: 0; right: 0;
      padding: 60px 16px 14px;
      background: linear-gradient(to top, rgba(0,0,0,0.94) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
      display: flex; align-items: flex-end; justify-content: space-between;
    }
    .city-step-badge {
      display: inline-flex; align-items: center;
      background: rgba(91,138,255,0.18);
      border: 1px solid rgba(91,138,255,0.35);
      backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      border-radius: 8px; padding: 5px 12px;
      font-size: 14px; font-weight: 700; color: #5b8aff;
    }
    .city-step-tag-pill {
      font-size: 10px; font-weight: 800; letter-spacing: 0.8px;
      text-transform: uppercase; color: rgba(240,240,240,0.72);
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 6px; padding: 4px 10px;
    }
    .city-step-body { padding: 20px 20px 24px; flex: 1; }
    .city-step-title {
      font-family: 'Manrope', sans-serif; font-size: 14px; font-weight: 700;
      color: #f0f0f0; margin: 0 0 8px; line-height: 1.45;
    }
    .city-step-text {
      font-size: 12px; color: rgba(240,240,240,0.38); margin: 0; line-height: 1.6;
    }

    /* CTA */
    .city-cta {
      background: rgba(91,138,255,0.04);
      border: 1px solid rgba(91,138,255,0.15);
      border-radius: 24px; padding: 56px 48px; text-align: center; margin-bottom: 80px;
    }
    .city-cta-title {
      font-family: 'Manrope', sans-serif; font-size: clamp(22px, 3vw, 34px);
      font-weight: 800; color: #f0f0f0; margin: 0 0 10px;
    }
    .city-cta-sub { font-size: 15px; color: rgba(240,240,240,0.45); margin: 0 0 32px; }
    .city-cta-btns { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }

    /* MOBILE */
    @media (max-width: 700px) {
      .city-hero { padding: 100px 0 52px; }
      .city-hero-block { padding: 24px 20px; max-width: 100%; border-radius: 20px; }
      .city-h1 { letter-spacing: -1px; }
      .city-lead { white-space: normal; font-size: 13px; }
      .city-location { font-size: 20px; letter-spacing: 2px; }
      .city-address-text { font-size: 17px; }
      .city-steps { padding: 48px 0 68px; }
      .city-steps-grid { grid-template-columns: 1fr !important; }
      .city-step-photo img { height: 290px; }
      .city-cta { padding: 36px 20px; }
      .city-map-btns { flex-direction: column; }
      .city-map-btn { justify-content: center; }
    }
"""

HOURS_SCRIPT = """  <script>
    (function() {
      var now = new Date();
      var utc = now.getTime() + now.getTimezoneOffset() * 60000;
      var msk = new Date(utc + 3600000 * 3);
      var isOpen = msk.getDay() >= 1 && msk.getDay() <= 6 && msk.getHours() >= 10 && msk.getHours() < 19;
      var dot = document.getElementById('city-status-dot');
      var text = document.getElementById('city-status-text');
      if (dot) {
        dot.style.background = isOpen ? '#22c55e' : '#ef4444';
        dot.style.boxShadow = isOpen ? '0 0 8px rgba(34,197,94,0.8)' : '0 0 8px rgba(239,68,68,0.8)';
      }
      if (text) text.textContent = isOpen ? 'Открыто · Пн–Сб 10:00–19:00' : 'Закрыто · Открываемся в 10:00';
    })();
  </script>
"""

CITY_DATA = {
    'Уфа.html': {
        'city': 'Уфа',
        'lead': 'Маршрут: бизнес-центр → ресепшен → 1 этаж → офис 2.5',
        'address': 'Верхнеторговая площадь, 6<br>1 этаж, офис 2.5',
        'cols': 'repeat(3, 1fr)',
        'img_order': [0, 1, 2],
        'steps': [
            ('01', 'ВХОД',     'Заходим в бизнес-центр.',                               'Верхнеторговая площадь, 6 — вход с главного фасада, стеклянные двери.'),
            ('02', 'РЕСЕПШЕН', 'Покажите документ и скажите, что вам нужно в офис 2.5.',''),
            ('03', 'ОФИС 2.5', 'Найдите дверь в офис 2.5.',                              'Вывеска 1Ex на двери. Менеджер встретит вас.'),
        ],
    },
    'Казань.html': {
        'city': 'Казань',
        'lead': 'Маршрут: парковка → вход → 2 этаж → офис 207',
        'address': 'ул. Баумана 9А<br>2 этаж, офис 207',
        'cols': 'repeat(2, 1fr)',
        'img_order': [3, 0, 1, 2],
        'steps': [
            ('00', 'ПАРКОВКА', 'Парковка.',                                                  'Пропуск и видеоинструкцию по паркингу уточните у менеджера заранее.'),
            ('01', 'ВХОД',     'Заходим в бизнес-центр.',                                   'ул. Баумана 9А — пешеходная зона в центре Казани.'),
            ('02', 'РЕСЕПШЕН', 'Покажите документ и скажите, что вам нужно в офис 207.',    ''),
            ('03', 'ОФИС 207', 'Найдите вход в офис 207.',                                  'По указателям на 2 этаже, вывеска 1Ex на двери.'),
        ],
    },
    'Екатеринбург.html': {
        'city': 'Екатеринбург',
        'lead': 'Маршрут: 2-й подъезд → ресепшен → 11 этаж → офис 21103',
        'address': 'Радищева 6А<br>2 подъезд, 11 этаж, офис 21103',
        'cols': 'repeat(3, 1fr)',
        'img_order': [0, 1, 2],
        'steps': [
            ('01', 'ПОДЪЕЗД',  'Заходим во второй подъезд.',                                              'Радищева 6А — найдите второй подъезд здания.'),
            ('02', 'РЕСЕПШЕН', 'Покажите документ, нужен пропуск на 11 этаж в офис 21103.',''),
            ('03', 'ОФИС',     'После лифта направо, через проход, налево до конца.',       'Позвоните в домофон и продиктуйте код заявки менеджеру.'),
        ],
    },
}


def make_hero(data, url_2gis, url_yandex):
    return '\n'.join([
        '    <section class="city-hero">',
        '      <div class="city-hero-bg">',
        '        <div class="city-hero-glow"></div>',
        '        <div class="city-hero-dots"></div>',
        '      </div>',
        '      <div class="container">',
        '        <a href="index.html#offices" class="seg-back-link" style="position:relative;z-index:1;">← Все офисы</a>',
        '        <div class="city-hero-block" style="margin-top: 20px;">',
        '          <div class="city-tag">',
        '            <span class="city-dot" id="city-status-dot"></span>',
        '            <span id="city-status-text">Пн–Сб: 10:00–19:00 МСК</span>',
        '          </div>',
        '          <p class="city-location">' + data['city'] + '</p>',
        '          <h1 class="city-h1">КАК<br>ПРОЙТИ<br>В ОФИС</h1>',
        '          <p class="city-lead">' + data['lead'] + '</p>',
        '          <hr class="city-block-divider">',
        '          <div class="city-address">',
        '            <div class="city-address-icon">',
        '              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
        '            </div>',
        '            <div>',
        '              <div class="city-address-label">Адрес</div>',
        '              <div class="city-address-text">' + data['address'] + '</div>',
        '            </div>',
        '          </div>',
        '          <div class="city-map-btns">',
        '            <a href="' + url_2gis + '" class="city-map-btn city-map-btn--primary" target="_blank" rel="noopener">',
        '              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 11 22 2l-9 19-2-8-8-2Z"/></svg>',
        '              Открыть в 2ГИС',
        '            </a>',
        '            <a href="' + url_yandex + '" class="city-map-btn city-map-btn--outline" target="_blank" rel="noopener">',
        '              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m14.5 4.5-5-2.5L3 5v17l6.5-3 5 2.5 6.5-3V2l-6.5 2.5Z"/><path d="M9.5 2v17"/><path d="M14.5 4.5v17"/></svg>',
        '              Яндекс Карты',
        '            </a>',
        '          </div>',
        '        </div>',
        '      </div>',
        '    </section>',
    ])


def make_steps_section(data, all_imgs):
    img_order = data.get('img_order', list(range(len(data['steps']))))
    ordered_imgs = [all_imgs[i] if i < len(all_imgs) else '' for i in img_order]
    cols = data['cols']

    cards = ''
    for i, (num, tag, title, text) in enumerate(data['steps']):
        img_src = ordered_imgs[i] if i < len(ordered_imgs) else ''
        img_html = '<img src="' + img_src + '" alt="Шаг ' + num + '" loading="lazy">' if img_src else ''
        text_html = '\n              <p class="city-step-text">' + text + '</p>' if text else ''
        cards += (
            '\n          <div class="city-step-card">'
            '\n            <div class="city-step-photo">'
            '\n              ' + img_html +
            '\n              <div class="city-step-overlay">'
            '\n                <span class="city-step-badge">' + num + '</span>'
            '\n                <span class="city-step-tag-pill">' + tag + '</span>'
            '\n              </div>'
            '\n            </div>'
            '\n            <div class="city-step-body">'
            '\n              <h3 class="city-step-title">' + title + '</h3>' + text_html +
            '\n            </div>'
            '\n          </div>'
        )

    return '\n'.join([
        '    <section class="city-steps">',
        '      <div class="container">',
        '        <div class="city-steps-head">',
        '          <p class="city-steps-kicker">Фотоинструкция</p>',
        '          <h2 class="city-steps-title">Как пройти</h2>',
        '        </div>',
        '        <div class="city-steps-grid" style="grid-template-columns: ' + cols + ';">' + cards,
        '        </div>',
        '      </div>',
        '    </section>',
    ])


for filename, data in CITY_DATA.items():
    with open(filename, encoding='utf-8') as f:
        html = f.read()

    orig_file = filename.replace('.html', '_оригинал.html')
    try:
        with open(orig_file, encoding='utf-8') as f:
            img_html = f.read()
    except FileNotFoundError:
        img_html = html
    imgs = re.findall(r'src="(data:image/jpeg[^"]+|data:image/png[^"]+)"', img_html)
    print(f'{filename}: {len(imgs)} photos')

    m2 = re.search(r'href="(https://2gis[^"]+)"', html)
    my = re.search(r'href="(https://yandex\.ru/maps[^"]+)"', html)
    url_2gis   = m2.group(1) if m2 else '#'
    url_yandex = my.group(1) if my else '#'

    html = re.sub(r'<style>.*?</style>', '<style>' + NEW_CSS + '  </style>', html, count=1, flags=re.DOTALL)
    html = re.sub(r'<section class="city-hero">.*?</section>', make_hero(data, url_2gis, url_yandex), html, count=1, flags=re.DOTALL)
    html = re.sub(r'<section class="city-steps">.*?</section>', make_steps_section(data, imgs), html, count=1, flags=re.DOTALL)
    html = re.sub(r'<script>\s*\(function\(\).*?</script>\s*', '', html, count=1, flags=re.DOTALL)
    html = html.replace('  <script src="script.js"></script>', HOURS_SCRIPT + '  <script src="script.js"></script>')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'  -> OK')

print('Done.')
