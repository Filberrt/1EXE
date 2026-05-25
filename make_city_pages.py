import re
import shutil
import os

PHOTO_DIRS = {
    'ufa':   'Офис_Уфа',
    'kazan': 'Офис_казань',
}

def copy_photos(city_key):
    src_dir = PHOTO_DIRS.get(city_key)
    if not src_dir or not os.path.exists(src_dir):
        return []
    dst_dir = os.path.join('photos', city_key)
    os.makedirs(dst_dir, exist_ok=True)
    files = sorted([f for f in os.listdir(src_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))])
    paths = []
    for i, fname in enumerate(files):
        ext = os.path.splitext(fname)[1].lower()
        dst_name = f'office_{i + 1}{ext}'
        shutil.copy2(os.path.join(src_dir, fname), os.path.join(dst_dir, dst_name))
        paths.append(f'photos/{city_key}/{dst_name}')
    return paths


GALLERY_STEPS_CSS = """
    /* OFFICE GALLERY */
    .office-gallery-section { padding: 64px 0 0; }
    .sub-kicker { font-size: 11px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase; color: #5b8aff; margin: 0 0 10px; }
    .sub-big-title { font-family: 'Manrope', sans-serif; font-size: clamp(28px, 4vw, 44px); font-weight: 800; color: #f0f0f0; margin: 0 0 32px; text-transform: uppercase; letter-spacing: -1px; }
    .gallery-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
    .gallery-img { width: 100%; aspect-ratio: 3/4; object-fit: cover; border-radius: 16px; display: block; transition: transform 0.3s; }
    .gallery-img:hover { transform: scale(1.02); }

    /* HOW TO GET THERE */
    .sub-steps { padding: 72px 0 64px; }
    .sub-step-card {
      border-radius: 20px; overflow: hidden;
      background: #0c0c0c; border: 1px solid rgba(255,255,255,0.07);
      transition: border-color 0.25s, transform 0.25s;
      position: relative; display: flex; flex-direction: column;
    }
    .sub-step-card::before {
      content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
      background: linear-gradient(90deg, #5b8aff, #9b87ff);
      opacity: 0; transition: opacity 0.25s; z-index: 2;
    }
    .sub-step-card:hover { border-color: rgba(91,138,255,0.30); transform: translateY(-4px); }
    .sub-step-card:hover::before { opacity: 1; }
    .sub-step-photo { position: relative; flex-shrink: 0; }
    .sub-step-photo img { width: 100%; height: 320px; object-fit: cover; display: block; }
    .sub-step-overlay {
      position: absolute; bottom: 0; left: 0; right: 0;
      padding: 60px 16px 14px;
      background: linear-gradient(to top, rgba(0,0,0,0.94) 0%, rgba(0,0,0,0.4) 60%, transparent 100%);
      display: flex; align-items: flex-end; justify-content: space-between;
    }
    .sub-step-badge {
      display: inline-flex; align-items: center;
      background: rgba(91,138,255,0.18); border: 1px solid rgba(91,138,255,0.35);
      backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      border-radius: 8px; padding: 5px 12px;
      font-size: 14px; font-weight: 700; color: #5b8aff;
    }
    .sub-step-tag {
      font-size: 10px; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase;
      color: rgba(240,240,240,0.72); background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.12); border-radius: 6px; padding: 4px 10px;
    }
    .sub-step-body { padding: 20px 20px 24px; flex: 1; }
    .sub-step-title { font-family: 'Manrope', sans-serif; font-size: 14px; font-weight: 700; color: #f0f0f0; margin: 0 0 8px; line-height: 1.45; }
    .sub-step-text { font-size: 12px; color: rgba(240,240,240,0.38); margin: 0; line-height: 1.6; }

    @media (max-width: 700px) {
      .gallery-grid { grid-template-columns: repeat(2, 1fr); }
      .sub-steps { padding: 48px 0 48px; }
      .sub-step-photo img { height: 220px; }
      .sub-steps-grid { grid-template-columns: 1fr !important; }
    }
"""


def make_gallery_html(photo_paths, city_name):
    if not photo_paths:
        return ''
    imgs = '\n'.join(
        f'        <img class="gallery-img" src="{p}" alt="Офис {city_name} — фото {i+1}" loading="lazy">'
        for i, p in enumerate(photo_paths)
    )
    return f"""
    <section class="office-gallery-section">
      <div class="container">
        <p class="sub-kicker">Фото офиса</p>
        <h2 class="sub-big-title">Наш офис</h2>
        <div class="gallery-grid">
{imgs}
        </div>
      </div>
    </section>"""


def make_steps_html(steps, photo_paths, cols):
    if not steps or not photo_paths:
        return ''
    cards = ''
    for num, tag, title, text, photo_idx in steps:
        img_src = photo_paths[photo_idx] if photo_idx < len(photo_paths) else ''
        img_html = f'<img src="{img_src}" alt="Шаг {num}" loading="lazy">' if img_src else ''
        text_html = f'\n              <p class="sub-step-text">{text}</p>' if text else ''
        cards += f"""
          <div class="sub-step-card">
            <div class="sub-step-photo">
              {img_html}
              <div class="sub-step-overlay">
                <span class="sub-step-badge">{num}</span>
                <span class="sub-step-tag">{tag}</span>
              </div>
            </div>
            <div class="sub-step-body">
              <h3 class="sub-step-title">{title}</h3>{text_html}
            </div>
          </div>"""

    return f"""
    <section class="sub-steps">
      <div class="container">
        <p class="sub-kicker">Фотоинструкция</p>
        <h2 class="sub-big-title">Как пройти</h2>
        <div class="sub-steps-grid" style="display: grid; gap: 18px; grid-template-columns: {cols};">
{cards}
        </div>
      </div>
    </section>"""


CITIES = {
    'ufa.html': {
        'name': 'Уфа',
        'name_in': 'в Уфе',
        'subdomain': 'ufa.atom-exchange.ru',
        'address': 'Верхнеторговая площадь, 6',
        'region': 'RU-BA',
        'geo': '54.7388;55.9721',
        'icbm': '54.7388, 55.9721',
        'title': 'Обмен криптовалюты в Уфе | Atom Exchange — VIP-офис',
        'description': 'Обмен USDT, Bitcoin и криптовалюты на рубли в Уфе. VIP-офис на Верхнеторговой площади, 6. Живой менеджер, фиксация курса на 3 часа, сделки от 100 USDT.',
        'keywords': 'обмен криптовалюты Уфа, купить USDT Уфа, продать Bitcoin Уфа, криптообменник Уфа, обмен крипты на рубли Уфа',
        'hero_title': 'Обмен криптовалюты<br><span class="hero-title-accent">в Уфе — VIP‑офис<br>Верхнеторговая пл., 6</span>',
        'chip': 'VIP-офис в Уфе · Верхнеторговая пл.',
        'guide_link': 'Уфа.html',
        'schema_index': 0,
        'photos_key': 'ufa',
        # photo_idx is the 0-based index in the sorted photo list
        'steps': [
            ('01', 'ВХОД',     'Заходим в бизнес-центр.', 'Верхнеторговая площадь, 6 — вход с главного фасада, стеклянные двери.', 5),
            ('02', 'РЕСЕПШЕН', 'Покажите документ и скажите, что вам нужно в офис 2.5.', '', 1),
            ('03', 'ОФИС 2.5', 'Найдите дверь в офис 2.5. Вывеска Atom Exchange на двери.', 'Менеджер встретит вас.', 0),
        ],
        'steps_cols': 'repeat(3, 1fr)',
    },
    'kazan.html': {
        'name': 'Казань',
        'name_in': 'в Казани',
        'subdomain': 'kazan.atom-exchange.ru',
        'address': 'ул. Баумана 9А, офис 207',
        'region': 'RU-TA',
        'geo': '55.7887;49.1221',
        'icbm': '55.7887, 49.1221',
        'title': 'Обмен криптовалюты в Казани | Atom Exchange — VIP-офис',
        'description': 'Обмен USDT, Bitcoin и криптовалюты на рубли в Казани. VIP-офис на ул. Баумана 9А. Живой менеджер, фиксация курса на 3 часа, сделки от 100 USDT.',
        'keywords': 'обмен криптовалюты Казань, купить USDT Казань, продать Bitcoin Казань, криптообменник Казань, обмен крипты на рубли Казань',
        'hero_title': 'Обмен криптовалюты<br><span class="hero-title-accent">в Казани — VIP‑офис<br>ул. Баумана 9А</span>',
        'chip': 'VIP-офис в Казани · ул. Баумана 9А',
        'guide_link': 'Казань.html',
        'schema_index': 1,
        'photos_key': 'kazan',
        'steps': [
            ('01', 'ВХОД',     'Заходим в бизнес-центр.', 'ул. Баумана 9А — пешеходная зона в центре Казани.', 2),
            ('02', 'РЕСЕПШЕН', 'Покажите документ и скажите, что вам нужно в офис 207.', '', 3),
            ('03', 'ОФИС 207', 'Найдите вход в офис 207.', 'По указателям на 2 этаже, вывеска Atom Exchange на двери.', 0),
        ],
        'steps_cols': 'repeat(3, 1fr)',
    },
    'ekb.html': {
        'name': 'Екатеринбург',
        'name_in': 'в Екатеринбурге',
        'subdomain': 'ekb.atom-exchange.ru',
        'address': 'Радищева 6А, офис 21103',
        'region': 'RU-SVE',
        'geo': '56.8389;60.6057',
        'icbm': '56.8389, 60.6057',
        'title': 'Обмен криптовалюты в Екатеринбурге | Atom Exchange — VIP-офис',
        'description': 'Обмен USDT, Bitcoin и криптовалюты на рубли в Екатеринбурге. VIP-офис на Радищева 6А. Живой менеджер, фиксация курса на 3 часа, сделки от 100 USDT.',
        'keywords': 'обмен криптовалюты Екатеринбург, купить USDT Екатеринбург, продать Bitcoin Екатеринбург, криптообменник Екатеринбург, обмен крипты на рубли Екб',
        'hero_title': 'Обмен криптовалюты<br><span class="hero-title-accent">в Екатеринбурге — VIP‑офис<br>Радищева 6А</span>',
        'chip': 'VIP-офис в Екб · Радищева 6А',
        'guide_link': 'Екатеринбург.html',
        'schema_index': 2,
        'photos_key': 'ekb',  # no photos yet — folder doesn't exist
        'steps': [],
        'steps_cols': 'repeat(3, 1fr)',
    },
}

INJECT_BEFORE = '    <!-- ══════════════════════════════════════ SEGMENTS ═══ -->'

with open('index.html', encoding='utf-8') as f:
    base = f.read()

for filename, c in CITIES.items():
    html = base

    # Title
    html = re.sub(r'<title>.*?</title>', f'<title>{c["title"]}</title>', html, flags=re.DOTALL)
    # Description
    html = re.sub(r'<meta name="description"[^>]+>', f'<meta name="description" content="{c["description"]}" />', html)
    # Keywords
    html = re.sub(r'<meta name="keywords"[^>]+>', f'<meta name="keywords" content="{c["keywords"]}" />', html)
    # Canonical
    html = html.replace('href="https://atom-exchange.ru/"', f'href="https://{c["subdomain"]}/"', 1)
    # OG url
    html = html.replace('<meta property="og:url" content="https://atom-exchange.ru/" />', f'<meta property="og:url" content="https://{c["subdomain"]}/" />', 1)
    # OG title
    name_in = c['name_in']
    html = re.sub(r'<meta property="og:title"[^>]+>', f'<meta property="og:title" content="Atom Exchange — Обмен криптовалюты {name_in}" />', html)
    # Geo
    html = html.replace('content="RU-BA"', f'content="{c["region"]}"', 1)
    html = html.replace('content="Уфа, Казань, Екатеринбург"', f'content="{c["name"]}"', 1)
    html = html.replace('content="54.7388;55.9721"', f'content="{c["geo"]}"', 1)
    html = html.replace('content="54.7388, 55.9721"', f'content="{c["icbm"]}"', 1)
    # Schema.org
    schemas = re.findall(r'\{[^{}]*"LocalBusiness"[^{}]*\}', html, re.DOTALL)
    if schemas and len(schemas) > c['schema_index']:
        schema_single = schemas[c['schema_index']]
        html = re.sub(r'<script type="application/ld\+json">.*?</script>',
            f'<script type="application/ld+json">\n  {schema_single}\n  </script>',
            html, count=1, flags=re.DOTALL)
    # Hero title
    html = re.sub(
        r'<h1 class="hero-title" id="hero-title">.*?</h1>',
        f'<h1 class="hero-title" id="hero-title">{c["hero_title"]}</h1>',
        html, count=1, flags=re.DOTALL
    )
    # First chip
    html = html.replace(
        '<span class="hero-chip">VIP-офисы: Уфа, Казань, Екб</span>',
        f'<span class="hero-chip">{c["chip"]}</span>',
        1
    )
    # Remove map section
    html = re.sub(r'\s*<!-- Map -->.*?</div>\s*(?=\s*<!-- Office cards)', '', html, count=1, flags=re.DOTALL)
    # Office card links
    html = html.replace(
        '<a href="ufa.html" class="office-link">Страница офиса →</a>',
        f'<a href="{c["guide_link"]}" class="office-link">Как пройти в офис →</a>'
    )
    html = html.replace(
        '<a href="kazan.html" class="office-link">Страница офиса →</a>',
        f'<a href="{c["guide_link"]}" class="office-link">Как пройти в офис →</a>'
    )
    html = html.replace(
        '<a href="ekb.html" class="office-link">Страница офиса →</a>',
        f'<a href="{c["guide_link"]}" class="office-link">Как пройти в офис →</a>'
    )

    # Copy photos and build sections
    photos = copy_photos(c['photos_key'])
    gallery_html = make_gallery_html(photos, c['name'])
    steps_html = make_steps_html(c['steps'], photos, c['steps_cols'])

    # Inject CSS before </head>
    css_block = f'  <style>{GALLERY_STEPS_CSS}  </style>\n</head>'
    html = html.replace('</head>', css_block, 1)

    # Inject gallery + steps before segments section
    new_sections = gallery_html + steps_html + '\n'
    if INJECT_BEFORE in html:
        html = html.replace(INJECT_BEFORE, new_sections + '\n' + INJECT_BEFORE, 1)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{filename} OK ({len(photos)} photos)')

print('Done.')
