import re

FILES = ['rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html']

for fname in FILES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()

    # 1. Logo
    html = html.replace(
        '<span class="logo-text">Atom<span class="logo-accent">EX</span></span>',
        '<img src="Logo_Atom.jpg" alt="Atom Exchange" class="logo-img">'
    )

    # 2. Remove dead nav/footer links
    html = html.replace(
        '\n        <a href="index.html#how-it-works" class="nav-link">Как работает</a>',
        ''
    )
    html = html.replace(
        '\n        <a href="index.html#faq" class="nav-link">FAQ</a>',
        ''
    )
    html = html.replace(
        '\n          <a href="index.html#how-it-works" class="footer-link">Как работает</a>',
        ''
    )
    html = html.replace(
        '\n          <a href="index.html#faq" class="footer-link">FAQ</a>',
        ''
    )

    # 3. Remove "Как проходит обмен" section
    html = re.sub(
        r'\s*<!-- HOW IT WORKS -->.*?</section>',
        '',
        html, count=1, flags=re.DOTALL
    )

    # 4. Remove FAQ section
    html = re.sub(
        r'\s*<!-- FAQ -->.*?</section>',
        '',
        html, count=1, flags=re.DOTALL
    )

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} OK')

print('Done.')
