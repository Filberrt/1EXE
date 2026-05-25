import re

# ── CSS additions ──────────────────────────────────────────────────────────────
EXTRA_CSS = """
    .btn-ask-rate {
      display: inline-flex; align-items: center; gap: 8px;
      padding: 11px 26px;
      background: rgba(34,197,94,0.10);
      border: 1px solid rgba(34,197,94,0.35);
      color: #22c55e; border-radius: 10px;
      font-weight: 600; font-size: 15px;
      text-decoration: none; transition: all 0.2s;
      white-space: nowrap;
    }
    .btn-ask-rate:hover { background: rgba(34,197,94,0.2); border-color: rgba(34,197,94,0.6); }
    .section-cta-row { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; margin-top: 32px; }
    .hero-content-solo { display: flex !important; justify-content: center; grid-template-columns: unset !important; }
    .hero-content-solo .hero-panel { max-width: 680px; width: 100%; }
"""

# ── Reusable HTML blocks ───────────────────────────────────────────────────────
RATE_BTN = '<div style="text-align:center;margin-top:28px;"><a href="https://t.me/danila_exchange" class="btn-ask-rate" target="_blank" rel="noopener">Узнать актуальный курс →</a></div>'

SECTION_CTA = '<div class="section-cta-row"><a href="https://t.me/danila_exchange" class="btn-primary" target="_blank" rel="noopener">Написать в Telegram</a><button class="btn-outline call-trigger">Позвонить</button></div>'

HERO_BTNS = '''            <div style="margin-top:28px;display:flex;gap:12px;flex-wrap:wrap;">
              <a href="https://t.me/danila_exchange" class="btn-primary" target="_blank" rel="noopener">Написать в Telegram</a>
              <button class="btn-outline call-trigger">Позвонить</button>
            </div>'''

FOUNDER_BLOCK = '''
    <!-- ═══════════════════════════════════════ FOUNDER QUOTE ═══ -->
    <section class="section founder-section">
      <div class="container">
        <div class="founder-card">
          <img src="man.jpg" alt="Александр Банаев" class="founder-photo">
          <div class="founder-body">
            <p class="founder-quote">«Мы строим не криптообменник — мы строим сеть криптобанков. Живой менеджер, VIP-офис, юридическая защита в каждом городе.»</p>
            <div class="founder-sig">
              <span class="founder-name">Александр Банаев</span>
              <span class="founder-role">Основатель Atom Exchange</span>
            </div>
            <div style="margin-top:20px;">
              <a href="https://t.me/danila_exchange" class="btn-primary" target="_blank" rel="noopener">Связаться с Александром</a>
            </div>
          </div>
        </div>
      </div>
    </section>'''


def inject_css(html):
    if 'btn-ask-rate' not in html:
        html = html.replace('</head>', f'  <style>{EXTRA_CSS}  </style>\n</head>', 1)
    return html


def remove_section_subs(html):
    return re.sub(r'\n?\s*<p class="section-sub">.*?</p>', '', html, flags=re.DOTALL)


# ── MAIN + SUBDOMAIN pages ─────────────────────────────────────────────────────
MAIN_PAGES = ['index.html', 'ufa.html', 'kazan.html', 'ekb.html']

for fname in MAIN_PAGES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()

    # CSS
    html = inject_css(html)

    # Hide widget
    html = html.replace(
        '<div class="widget" id="widget">',
        '<div class="widget" id="widget" style="display:none">', 1
    )

    # Hero single-column
    html = html.replace('<div class="hero-content">', '<div class="hero-content hero-content-solo">', 1)

    # Hero CTA buttons after chips (before hero-panel closing)
    html = html.replace(
        '            </div>\n          </div>\n\n          <!-- ─── RIGHT PANEL',
        HERO_BTNS + '\n            </div>\n          </div>\n\n          <!-- ─── RIGHT PANEL'
    )

    # Move founder section: remove from current position, insert before services
    founder_pat = r'\n\n    <!-- ═══════════════════════════════════════ FOUNDER QUOTE ═══ -->.*?</section>'
    m = re.search(founder_pat, html, re.DOTALL)
    if m:
        existing_founder = m.group(0)
        # Build updated founder block with "Связаться" button
        new_founder = re.sub(
            r'(</div>\n          </div>\n        </div>)',
            '</div>\n            <div style="margin-top:20px;"><a href="https://t.me/danila_exchange" class="btn-primary" target="_blank" rel="noopener">Связаться с Александром</a></div>\n          </div>\n        </div>',
            existing_founder, count=1
        )
        # Shorten quote
        new_founder = re.sub(
            r'«[^»]+»',
            '«Мы строим не криптообменник — мы строим сеть криптобанков. Живой менеджер, VIP-офис, юридическая защита в каждом городе.»',
            new_founder, count=1
        )
        html = html.replace(existing_founder, '', 1)
        # Insert before services
        services_marker = '    <!-- ══════════════════════════════════════ SERVICES'
        if services_marker in html:
            html = html.replace(services_marker, new_founder + '\n\n    <!-- ══════════════════════════════════════ SERVICES')

    # "Узнать курс" after services grid (before segments)
    segments_marker = '    <!-- ══════════════════════════════════════ SEGMENTS'
    if segments_marker in html:
        html = html.replace(
            '      </div>\n    </section>\n\n    <!-- ══════════════════════════════════════ SEGMENTS',
            '      </div>\n' + RATE_BTN + '\n    </section>\n\n    <!-- ══════════════════════════════════════ SEGMENTS'
        )

    # CTA after segments
    advantages_marker = '    <!-- ══════════════════════════════════════ ADVANTAGES'
    if advantages_marker in html:
        html = html.replace(
            '      </div>\n    </section>\n\n    <!-- ══════════════════════════════════════ ADVANTAGES',
            '      </div>\n' + SECTION_CTA + '\n    </section>\n\n    <!-- ══════════════════════════════════════ ADVANTAGES'
        )

    # CTA after advantages (before reserves)
    reserves_marker = '    <!-- ═══════════════════════════════════════ RESERVES'
    if reserves_marker in html:
        html = html.replace(
            '        </div>\n      </div>\n    </section>\n\n    <!-- ═══════════════════════════════════════ RESERVES',
            '        </div>\n      </div>\n' + SECTION_CTA + '\n    </section>\n\n    <!-- ═══════════════════════════════════════ RESERVES'
        )

    # Remove all section subtitles
    html = remove_section_subs(html)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} OK')


# ── DIRECTION pages ────────────────────────────────────────────────────────────
DIR_PAGES = ['rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html']

for fname in DIR_PAGES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()

    # CSS
    html = inject_css(html)

    # Add founder block after hero section (after </section> following seg-hero)
    if 'founder-section' not in html:
        html = re.sub(
            r'(</section>\n\n    <!-- FOR WHOM)',
            FOUNDER_BLOCK + r'\n\n    <!-- FOR WHOM',
            html, count=1
        )

    # "Связаться с Александром" button in existing founder if already there
    if 'Связаться с Александром' not in html and 'founder-section' in html:
        html = html.replace(
            '<span class="founder-role">Основатель Atom Exchange</span>\n            </div>\n          </div>',
            '<span class="founder-role">Основатель Atom Exchange</span>\n            </div>\n            <div style="margin-top:20px;"><a href="https://t.me/danila_exchange" class="btn-primary" target="_blank" rel="noopener">Связаться с Александром</a></div>\n          </div>'
        )

    # "Узнать курс" button after for-whom section
    if 'btn-ask-rate' not in html:
        html = re.sub(
            r'(</section>\n\n    <!-- ADVANTAGES)',
            r'</section>\n' + RATE_BTN + '\n\n    <!-- ADVANTAGES',
            html, count=1
        )

    # CTA after advantages
    html = re.sub(
        r'(</div>\n      </div>\n    </section>\n\n    <!-- FINAL CTA)',
        r'</div>\n      </div>\n' + SECTION_CTA + '\n    </section>\n\n    <!-- FINAL CTA',
        html, count=1
    )

    # Remove section subtitles
    html = remove_section_subs(html)

    # Simplify for-whom text block (remove long paragraph, keep h2 + items)
    html = re.sub(
        r'(<div class="seg-for-whom-text">\s*<h2[^>]*>[^<]+</h2>)\s*<p>.*?</p>(\s*</div>)',
        r'\1\2',
        html, flags=re.DOTALL
    )

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} OK')

print('Done.')
