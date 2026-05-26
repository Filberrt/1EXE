import re

TG_OLD = 'https://t.me/danila_exchange'
TG_NEW = 'https://t.me/atomexchange_manager'

NEW_QUOTE = '«Крупный финансовый бизнес строится не на шуме, а на доверии. Мы создаём криптобанк №1 в России: с понятным курсом, реальными офисами, прозрачными условиями и ответственностью перед каждым клиентом.»'

RATE_BTN_SM = f'<a href="{TG_NEW}" class="btn-ask-rate btn-ask-rate--sm" target="_blank" rel="noopener">Узнать курс в моменте</a>'
CONSULT_BTN_SM = f'<a href="{TG_NEW}" class="btn-ask-rate btn-ask-rate--sm" target="_blank" rel="noopener">Получить консультацию</a>'

NEW_SERVICES_GRID = f"""        <div class="services-grid">
          <div class="service-card">
            <span class="service-icon">₮</span>
            <span class="service-name">Обмен USDT</span>
            <span class="service-tag">RUB ↔ USDT · TRC-20 · ERC-20</span>
            {RATE_BTN_SM}
          </div>
          <div class="service-card">
            <span class="service-icon">₿</span>
            <span class="service-name">Обмен Bitcoin</span>
            <span class="service-tag">RUB ↔ BTC</span>
            {RATE_BTN_SM}
          </div>
          <div class="service-card">
            <span class="service-icon">Ξ</span>
            <span class="service-name">Обмен Ethereum</span>
            <span class="service-tag">RUB ↔ ETH</span>
            {RATE_BTN_SM}
          </div>
          <div class="service-card">
            <span class="service-icon">\U0001f48e</span>
            <span class="service-name">Обмен TON</span>
            <span class="service-tag">RUB ↔ TON</span>
            {RATE_BTN_SM}
          </div>
          <div class="service-card">
            <span class="service-icon">\U0001f536</span>
            <span class="service-name">Обмен BNB</span>
            <span class="service-tag">RUB ↔ BNB</span>
            {RATE_BTN_SM}
          </div>
          <div class="service-card">
            <span class="service-icon">\U0001f30a</span>
            <span class="service-name">Обмен SOL</span>
            <span class="service-tag">RUB ↔ SOL</span>
            {RATE_BTN_SM}
          </div>
        </div>"""

NEW_SEG_GRID = f"""        <div class="seg-grid">
          <div class="seg-card">
            <div class="seg-card-icon">₮</div>
            <h3 class="seg-card-title">Обмен криптовалюты</h3>
            <p class="seg-card-text">USDT, BTC, ETH и другие — меняем на рубли по курсу рынка.</p>
            {CONSULT_BTN_SM}
          </div>
          <div class="seg-card">
            <div class="seg-card-icon">\U0001f3e0</div>
            <h3 class="seg-card-title">Оплата недвижимости</h3>
            <p class="seg-card-text">Крупный нал, ДКП, конфиденциальность.</p>
            {CONSULT_BTN_SM}
          </div>
          <div class="seg-card">
            <div class="seg-card-icon">\U0001f310</div>
            <h3 class="seg-card-title">ВЭД</h3>
            <p class="seg-card-text">Платежи поставщикам через USDT вместо SWIFT.</p>
            {CONSULT_BTN_SM}
          </div>
          <div class="seg-card">
            <div class="seg-card-icon">\U0001f4bc</div>
            <h3 class="seg-card-title">Бизнесу</h3>
            <p class="seg-card-text">B2B операции, регулярные сделки, индивидуальные условия.</p>
            {CONSULT_BTN_SM}
          </div>
          <div class="seg-card">
            <div class="seg-card-icon">\U0001f504</div>
            <h3 class="seg-card-title">Перестановка средств</h3>
            <p class="seg-card-text">Нал в Уфе — USDT в Дубае. Координируем оба конца.</p>
            {CONSULT_BTN_SM}
          </div>
          <div class="seg-card">
            <div class="seg-card-icon">✈️</div>
            <h3 class="seg-card-title">Переводы за рубеж</h3>
            <p class="seg-card-text">Без SWIFT и международных карт.</p>
            {CONSULT_BTN_SM}
          </div>
        </div>"""

REVIEWS_SECTION = f"""
    <!-- ═══════════════════════════════════════ REVIEWS ═══ -->
    <section class="section" id="reviews">
      <div class="container">
        <div class="section-head">
          <h2 class="section-title">Отзывы клиентов</h2>
        </div>
        <div class="reviews-carousel-wrap">
          <div class="reviews-track" id="reviews-track">
            <div class="review-card">
              <div class="review-stars">★★★★★</div>
              <p class="review-text">«Обменивал USDT на рубли — всё чётко, курс зафиксировали, через час уже с кэшем. Рекомендую.»</p>
              <div class="review-author">Алексей М.</div>
            </div>
            <div class="review-card">
              <div class="review-stars">★★★★★</div>
              <p class="review-text">«Работаем с Atom Exchange уже полгода — надёжно, курс честный, менеджер всегда на связи.»</p>
              <div class="review-author">Наталья К.</div>
            </div>
            <div class="review-card">
              <div class="review-stars">★★★★★</div>
              <p class="review-text">«Перевели деньги за рубеж без SWIFT. Быстро, безопасно, всё как договаривались.»</p>
              <div class="review-author">Игорь Д.</div>
            </div>
            <div class="review-card">
              <div class="review-stars">★★★★★</div>
              <p class="review-text">«VIP-офис, приятная атмосфера, никаких очередей. Буду обращаться ещё.»</p>
              <div class="review-author">Светлана Р.</div>
            </div>
          </div>
          <div class="reviews-nav">
            <button class="carousel-btn" onclick="reviewsScroll(-1)">←</button>
            <a href="{TG_NEW}" class="btn-ask-rate" target="_blank" rel="noopener">Написать нам →</a>
            <button class="carousel-btn" onclick="reviewsScroll(1)">→</button>
          </div>
        </div>
      </div>
    </section>"""

ARTICLES_SECTION = """
    <!-- ═══════════════════════════════════════ ARTICLES ═══ -->
    <section class="section" id="articles">
      <div class="container">
        <div class="section-head">
          <h2 class="section-title">Наши статьи</h2>
        </div>
        <div class="articles-track" id="articles-track">
          <div class="article-card">
            <div class="article-tag">Скоро</div>
            <h3 class="article-title">Как безопасно обменять крипту на рубли</h3>
            <p class="article-desc">Подробный гид по работе с офисным криптобанком.</p>
          </div>
          <div class="article-card">
            <div class="article-tag">Скоро</div>
            <h3 class="article-title">AML-проверка: зачем она нужна</h3>
            <p class="article-desc">Рассказываем про скоринг транзакций и юридическую защиту.</p>
          </div>
          <div class="article-card">
            <div class="article-tag">Скоро</div>
            <h3 class="article-title">Фиксация курса на 3 часа</h3>
            <p class="article-desc">Почему это удобно и как это работает на практике.</p>
          </div>
        </div>
      </div>
    </section>"""

REVIEWS_JS = """  <script>
    function reviewsScroll(dir) {
      var t = document.getElementById('reviews-track');
      if (t) t.scrollBy({ left: dir * 320, behavior: 'smooth' });
    }
  </script>"""

EXTRA_CSS_V2 = """
    /* rebuild_v2 */
    .btn-ask-rate--sm { font-size: 13px !important; padding: 8px 16px !important; margin-top: 12px; width: 100%; justify-content: center; box-sizing: border-box; }
    .service-card { display: flex; flex-direction: column; }
    .seg-card { display: flex; flex-direction: column; cursor: default; }
    .adv-card { display: flex; flex-direction: column; }
    .reviews-carousel-wrap { position: relative; }
    .reviews-track { display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 8px; scrollbar-width: none; }
    .reviews-track::-webkit-scrollbar { display: none; }
    .review-card { flex: 0 0 300px; scroll-snap-align: start; background: #0c0c0c; border: 1px solid rgba(255,255,255,0.07); border-radius: 16px; padding: 24px; }
    .review-stars { color: #f5c842; font-size: 18px; margin-bottom: 12px; }
    .review-text { color: rgba(240,240,240,0.75); font-size: 14px; line-height: 1.6; margin: 0 0 16px; }
    .review-author { font-weight: 600; font-size: 13px; color: rgba(240,240,240,0.45); }
    .reviews-nav { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 20px; }
    .carousel-btn { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.12); color: #f0f0f0; border-radius: 8px; width: 40px; height: 40px; font-size: 16px; cursor: pointer; transition: background 0.2s; }
    .carousel-btn:hover { background: rgba(255,255,255,0.12); }
    .articles-track { display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 8px; scrollbar-width: none; }
    .articles-track::-webkit-scrollbar { display: none; }
    .article-card { flex: 0 0 280px; scroll-snap-align: start; background: #0c0c0c; border: 1px solid rgba(255,255,255,0.07); border-radius: 16px; padding: 24px; }
    .article-tag { display: inline-block; padding: 4px 10px; background: rgba(91,138,255,0.15); border: 1px solid rgba(91,138,255,0.3); color: #5b8aff; border-radius: 6px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 12px; }
    .article-title { font-size: 16px; font-weight: 700; color: #f0f0f0; margin: 0 0 10px; line-height: 1.4; }
    .article-desc { font-size: 13px; color: rgba(240,240,240,0.55); line-height: 1.5; margin: 0; }
"""


def inject_css_v2(html):
    if 'rebuild_v2' not in html:
        html = html.replace('</head>', f'  <style>{EXTRA_CSS_V2}  </style>\n</head>', 1)
    return html


def replace_contacts(html):
    html = html.replace(TG_OLD, TG_NEW)
    html = html.replace('+7 (937) 333-45-05', '+7 937 336 3357')
    html = html.replace('+79373334505', '+79373363357')
    return html


def update_founder_quote(html):
    html = re.sub(r'«[^»]+»', NEW_QUOTE, html, count=1)
    return html


def add_rate_btn_to_adv_cards(html):
    def inject(m):
        card = m.group(0)
        if 'btn-ask-rate--sm' not in card:
            card = re.sub(
                r'(<p class="adv-text">.*?</p>)',
                r'\1\n            ' + RATE_BTN_SM,
                card, count=1, flags=re.DOTALL
            )
        return card
    return re.sub(r'<article class="adv-card">.*?</article>', inject, html, flags=re.DOTALL)


def rebuild_services(html):
    html = re.sub(
        r'<div class="services-grid">.*?</div>(?=\s*\n\s*</div>)',
        NEW_SERVICES_GRID,
        html, count=1, flags=re.DOTALL
    )
    return html


def rebuild_segments(html):
    # Update title
    html = re.sub(
        r'(<h2 class="section-title"[^>]*>)Направления работы(</h2>)',
        r'\1Чем можем быть полезны\2',
        html
    )
    # Replace seg-grid
    html = re.sub(
        r'<div class="seg-grid">.*?</div>(?=\s*\n\s*</div>)',
        NEW_SEG_GRID,
        html, count=1, flags=re.DOTALL
    )
    return html


def remove_reserves(html):
    html = re.sub(
        r'\n\n    <!-- ═══════════════════════════════════════ RESERVES ═══ -->.*?</section>',
        '',
        html, count=1, flags=re.DOTALL
    )
    return html


def add_reviews_and_articles(html):
    # Insert before offices section on main pages, or before final CTA on dir pages
    offices_marker = '\n    <!-- ═══════════════════════════════════════ OFFICES'
    cta_marker = '\n    <!-- ═══════════════════════════════════════ FINAL CTA'
    cta_marker2 = '\n    <!-- FINAL CTA'

    if offices_marker in html and 'reviews-track' not in html:
        html = html.replace(offices_marker, REVIEWS_SECTION + '\n' + ARTICLES_SECTION + '\n' + offices_marker)
    elif cta_marker in html and 'reviews-track' not in html:
        html = html.replace(cta_marker, REVIEWS_SECTION + '\n' + ARTICLES_SECTION + '\n' + cta_marker)
    elif cta_marker2 in html and 'reviews-track' not in html:
        html = html.replace(cta_marker2, REVIEWS_SECTION + '\n' + ARTICLES_SECTION + '\n' + cta_marker2)
    return html


def inject_reviews_js(html):
    if 'reviewsScroll' not in html:
        html = html.replace('<script src="script.js"></script>', REVIEWS_JS + '\n  <script src="script.js"></script>', 1)
    return html


# ── ALL PAGES ──────────────────────────────────────────────────────────────────
ALL_PAGES = [
    'index.html', 'ufa.html', 'kazan.html', 'ekb.html',
    'rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html'
]

MAIN_PAGES = ['index.html', 'ufa.html', 'kazan.html', 'ekb.html']

for fname in ALL_PAGES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()

    html = inject_css_v2(html)
    html = replace_contacts(html)
    html = update_founder_quote(html)
    html = add_rate_btn_to_adv_cards(html)
    html = inject_reviews_js(html)

    if fname in MAIN_PAGES:
        html = rebuild_services(html)
        html = rebuild_segments(html)
        html = remove_reserves(html)
        html = add_reviews_and_articles(html)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} done')

print('All done.')
