import re

FILES = ['rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html']

BACK_NAV_JS = """  <script>
    (function() {
      var from = new URLSearchParams(window.location.search).get('from');
      var map = {ufa: 'ufa.html', kazan: 'kazan.html', ekb: 'ekb.html'};
      if (from && map[from]) {
        var dest = map[from];
        document.querySelectorAll('a').forEach(function(a) {
          var h = a.getAttribute('href') || '';
          if (h === 'index.html' || h.startsWith('index.html#') || h === '/') {
            a.setAttribute('href', h.replace('index.html', dest).replace(/^\/$/, dest));
          }
        });
      }
    })();
  </script>
"""

def first_sentence(s):
    s = s.strip()
    m = re.search(r'.+?[.!?]', s, re.DOTALL)
    return m.group(0).strip() if m else s


for fname in FILES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()

    # 1. Logo
    html = html.replace(
        '<span class="logo-text">Atom<span class="logo-accent">EX</span></span>',
        '<img src="Logo_Atom.png" alt="Atom Exchange" class="logo-img">'
    )
    # Also update if already set to .jpg
    html = html.replace('src="Logo_Atom.jpg"', 'src="Logo_Atom.png"')

    # 2. Remove dead nav/footer links
    html = html.replace('\n        <a href="index.html#how-it-works" class="nav-link">Как работает</a>', '')
    html = html.replace('\n        <a href="index.html#faq" class="nav-link">FAQ</a>', '')
    html = html.replace('\n          <a href="index.html#how-it-works" class="footer-link">Как работает</a>', '')
    html = html.replace('\n          <a href="index.html#faq" class="footer-link">FAQ</a>', '')

    # 3. Remove "Как проходит обмен" section
    html = re.sub(r'\s*<!-- HOW IT WORKS -->.*?</section>', '', html, count=1, flags=re.DOTALL)

    # 4. Remove FAQ section
    html = re.sub(r'\s*<!-- FAQ -->.*?</section>', '', html, count=1, flags=re.DOTALL)

    # 5. Shorten text
    # Remove section-sub subtitles (generic filler under H2 headings)
    html = re.sub(r'<p class="section-sub">.*?</p>', '', html, flags=re.DOTALL)

    # Shorten hero-sub to 1 sentence
    html = re.sub(
        r'(<p class="hero-sub">)(.*?)(</p>)',
        lambda m: m.group(1) + first_sentence(m.group(2)) + m.group(3),
        html, flags=re.DOTALL
    )

    # Shorten adv-card descriptions to 1 sentence
    html = re.sub(
        r'(<p class="adv-text">)(.*?)(</p>)',
        lambda m: m.group(1) + first_sentence(m.group(2)) + m.group(3),
        html, flags=re.DOTALL
    )

    # Simplify for-whom items: keep only the bold heading, remove explanation after em-dash
    html = re.sub(
        r'(<p>)(<strong>[^<]+</strong>)[^<]*(</p>)',
        r'\1\2\3',
        html
    )

    # 6. Inject back-nav JS before </body>
    if BACK_NAV_JS.strip() not in html:
        html = html.replace('</body>', BACK_NAV_JS + '</body>')

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} OK')

print('Done.')
