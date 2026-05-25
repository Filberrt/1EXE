import re

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
    },
}

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

    # Schema.org — keep only city-specific entry
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

    # First chip → city-specific
    html = html.replace(
        '<span class="hero-chip">VIP-офисы: Уфа, Казань, Екб</span>',
        f'<span class="hero-chip">{c["chip"]}</span>',
        1
    )

    # Remove map section (map-wrap) from subdomain pages
    html = re.sub(r'\s*<!-- Map -->.*?</div>\s*(?=\s*<!-- Office cards)', '', html, count=1, flags=re.DOTALL)

    # Office cards on subdomains: link back to the city guide page
    html = html.replace(
        '<a href="https://ufa.atom-exchange.ru" class="office-link">Страница офиса →</a>',
        f'<a href="{c["guide_link"]}" class="office-link">Как пройти в офис →</a>'
    )
    html = html.replace(
        '<a href="https://kazan.atom-exchange.ru" class="office-link">Страница офиса →</a>',
        f'<a href="{c["guide_link"]}" class="office-link">Как пройти в офис →</a>'
    )
    html = html.replace(
        '<a href="https://ekb.atom-exchange.ru" class="office-link">Страница офиса →</a>',
        f'<a href="{c["guide_link"]}" class="office-link">Как пройти в офис →</a>'
    )

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{filename} OK')

print('Done.')
