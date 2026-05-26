import re

TG = 'https://t.me/atomexchange_manager'

REVIEWS_SECTION = f"""
    <!-- REVIEWS -->
    <section class="section" id="reviews">
      <div class="container">
        <div class="section-head">
          <h2 class="section-title">Отзывы клиентов</h2>
        </div>
        <div class="reviews-carousel-wrap">
          <div class="reviews-scroll-track" id="reviews-track">
            <div class="review-card">
              <div class="review-stars">★★★★★</div>
              <p class="review-text">«Отзыв появится здесь»</p>
              <div class="review-author">— Клиент</div>
            </div>
            <div class="review-card">
              <div class="review-stars">★★★★★</div>
              <p class="review-text">«Отзыв появится здесь»</p>
              <div class="review-author">— Клиент</div>
            </div>
            <div class="review-card">
              <div class="review-stars">★★★★★</div>
              <p class="review-text">«Отзыв появится здесь»</p>
              <div class="review-author">— Клиент</div>
            </div>
          </div>
          <div class="reviews-nav">
            <button class="carousel-btn" onclick="reviewsScroll(-1)">←</button>
            <a href="{TG}" class="btn-ask-rate" target="_blank" rel="noopener">Написать нам →</a>
            <button class="carousel-btn" onclick="reviewsScroll(1)">→</button>
          </div>
        </div>
      </div>
    </section>"""

ARTICLES_SECTION = """
    <!-- ARTICLES -->
    <section class="section" id="articles">
      <div class="container">
        <div class="section-head">
          <h2 class="section-title">Наши статьи</h2>
        </div>
        <div class="articles-scroll-track" id="articles-track">
          <div class="article-card">
            <div class="article-tag">Скоро</div>
            <h3 class="article-title">Статья появится здесь</h3>
            <p class="article-desc">Материал готовится к публикации.</p>
          </div>
          <div class="article-card">
            <div class="article-tag">Скоро</div>
            <h3 class="article-title">Статья появится здесь</h3>
            <p class="article-desc">Материал готовится к публикации.</p>
          </div>
          <div class="article-card">
            <div class="article-tag">Скоро</div>
            <h3 class="article-title">Статья появится здесь</h3>
            <p class="article-desc">Материал готовится к публикации.</p>
          </div>
        </div>
      </div>
    </section>"""

# New CSS – fix track class names to match new IDs
CAROUSEL_CSS_FIX = """
    /* carousel-fix v4 */
    .reviews-scroll-track { display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 8px; scrollbar-width: none; }
    .reviews-scroll-track::-webkit-scrollbar { display: none; }
    .articles-scroll-track { display: flex; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding-bottom: 8px; scrollbar-width: none; }
    .articles-scroll-track::-webkit-scrollbar { display: none; }
    /* gallery carousel explicit */
    #gallery-track { display: flex !important; gap: 12px; overflow-x: auto !important; scroll-snap-type: x mandatory; scrollbar-width: none; -webkit-overflow-scrolling: touch; }
    #gallery-track::-webkit-scrollbar { display: none; }
    .gallery-carousel-img { flex: 0 0 calc(50% - 6px) !important; scroll-snap-align: start; border-radius: 16px; aspect-ratio: 3/4; object-fit: cover; display: block; }
    @media (max-width: 600px) { .gallery-carousel-img { flex: 0 0 85% !important; } }
    /* hero full-width fix */
    .hero-content-solo { display: flex !important; justify-content: center; grid-template-columns: unset !important; }
    .hero-content-solo .hero-panel { max-width: 100% !important; width: 100% !important; }
"""

CAROUSEL_JS = """  <script>
    function reviewsScroll(dir) {
      var t = document.getElementById('reviews-track');
      if (t) { t.scrollLeft += dir * 320; }
    }
    function galleryScroll(dir) {
      var t = document.getElementById('gallery-track');
      if (t) { t.scrollLeft += dir * 360; }
    }
    function articlesScroll(dir) {
      var t = document.getElementById('articles-track');
      if (t) { t.scrollLeft += dir * 300; }
    }
  </script>"""

ALL_PAGES = [
    'index.html', 'ufa.html', 'kazan.html', 'ekb.html',
    'rieltory.html', 'ved.html', 'biznes.html', 'perestanovka.html', 'perevody.html'
]


def inject_css_fix(html):
    if 'carousel-fix v4' not in html:
        html = html.replace('</head>', f'  <style>{CAROUSEL_CSS_FIX}  </style>\n</head>', 1)
    return html


def inject_js(html):
    # Remove any old scroll functions and inject fresh consolidated ones
    html = re.sub(r'\s*<script>\s*function reviewsScroll.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'\s*<script>\s*function galleryScroll.*?</script>', '', html, flags=re.DOTALL)
    html = re.sub(r'\s*<script>\s*function officeScroll.*?</script>', '', html, flags=re.DOTALL)
    html = html.replace(
        '  <script src="script.js"></script>',
        CAROUSEL_JS + '\n  <script src="script.js"></script>',
        1
    )
    return html


def fix_hero_width(html):
    # Patch the hero-panel max-width in any inline style block
    html = html.replace(
        '.hero-content-solo .hero-panel { max-width: 680px; width: 100%; }',
        '.hero-content-solo .hero-panel { max-width: 100%; width: 100%; }'
    )
    return html


def insert_reviews_articles(html):
    if 'id="reviews-track"' in html:
        return html  # already has real reviews HTML

    # Remove any duplicate stale sections that have no real content
    html = re.sub(r'\n    <!-- REVIEWS -->.*?</section>', '', html, count=1, flags=re.DOTALL)
    html = re.sub(r'\n    <!-- ARTICLES -->.*?</section>', '', html, count=1, flags=re.DOTALL)

    # Insert before cta-section (works on all pages)
    html = html.replace(
        '\n    <section class="cta-section"',
        REVIEWS_SECTION + '\n' + ARTICLES_SECTION + '\n\n    <section class="cta-section"',
        1
    )
    return html


# ── Apply to all pages ────────────────────────────────────────────────────────
for fname in ALL_PAGES:
    with open(fname, encoding='utf-8') as f:
        html = f.read()

    html = inject_css_fix(html)
    html = inject_js(html)
    html = fix_hero_width(html)
    html = insert_reviews_articles(html)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'{fname} done')

print('All done.')
