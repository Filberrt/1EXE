/* ═══════════════════════════════════════════════════════════
   1EX — Main Script
   ═══════════════════════════════════════════════════════════ */

document.addEventListener('DOMContentLoaded', () => {

  /* ─── HEADER: scroll effect ─── */
  const header = document.getElementById('header');
  const onScroll = () => {
    header.classList.toggle('scrolled', window.scrollY > 40);
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();


  /* ─── BURGER / MOBILE NAV ─── */
  const burger    = document.getElementById('burger');
  const mobileNav = document.getElementById('mobile-nav');
  const siteHeader = document.querySelector('.header');

  const closeMobileNav = () => {
    mobileNav.classList.remove('open');
    burger.classList.remove('open');
    burger.setAttribute('aria-expanded', 'false');
    siteHeader.classList.remove('mobile-open');
  };

  burger.addEventListener('click', () => {
    const open = mobileNav.classList.toggle('open');
    burger.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
    siteHeader.classList.toggle('mobile-open', open);
  });

  mobileNav.querySelectorAll('a, button').forEach(el => {
    el.addEventListener('click', closeMobileNav);
  });


  /* ─── NAV DROPDOWN ─── */
  const navDropdown    = document.getElementById('nav-dropdown');
  const navDropdownBtn = document.getElementById('nav-dropdown-btn');

  if (navDropdown && navDropdownBtn) {
    navDropdownBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = navDropdown.classList.toggle('open');
      navDropdownBtn.setAttribute('aria-expanded', String(isOpen));
    });

    document.addEventListener('click', () => {
      navDropdown.classList.remove('open');
      navDropdownBtn.setAttribute('aria-expanded', 'false');
    });

    navDropdown.addEventListener('click', e => e.stopPropagation());

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        navDropdown.classList.remove('open');
        navDropdownBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }


  /* ─── EXCHANGE CALCULATOR ─── */
  const inputGive    = document.getElementById('input-give');
  const inputGet     = document.getElementById('input-get');
  const rateDisplay  = document.getElementById('rate-display');
  const rateTimer    = document.getElementById('rate-timer');
  const currencyBtn  = document.getElementById('currency-btn');
  const currencyName = document.getElementById('currency-name');
  const currencyIcon = document.getElementById('currency-icon');
  const dropdown     = document.getElementById('currency-dropdown');

  if (inputGive && inputGet && currencyBtn && dropdown) {
    let currentRate = 92.40;
    let currentCode = 'USDT';
    let rateMinutes = 0;
    let lastEdited  = 'give';

    const fmt = (n) => {
      if (isNaN(n) || n === 0) return '';
      return Math.round(n).toLocaleString('ru-RU');
    };

    const fmtCrypto = (n) => {
      if (isNaN(n) || n <= 0) return '';
      const dec = currentCode === 'BTC' ? 6 : currentCode === 'ETH' ? 4 : 2;
      return parseFloat(n.toFixed(dec)).toString();
    };

    const recalc = () => {
      if (lastEdited === 'give') {
        const give = parseFloat(inputGive.value.replace(/\s/g, '')) || 0;
        inputGet.value = give > 0 ? fmt(give * currentRate) : '';
      } else {
        const rub = parseFloat(inputGet.value.replace(/\s/g, '')) || 0;
        inputGive.value = rub > 0 ? fmtCrypto(rub / currentRate) : '';
      }
    };

    inputGive.addEventListener('input', () => { lastEdited = 'give'; recalc(); });
    inputGet.addEventListener('input',  () => { lastEdited = 'get';  recalc(); });

    inputGive.addEventListener('focus', () => inputGive.select());
    inputGet.addEventListener('focus',  () => inputGet.select());

    const updateTimer = () => {
      rateMinutes++;
      if (rateTimer) rateTimer.textContent = rateMinutes === 1
        ? 'обновлён 1 мин назад'
        : `обновлён ${rateMinutes} мин назад`;
    };
    setInterval(updateTimer, 60_000);

    currencyBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      const isOpen = dropdown.classList.toggle('open');
      currencyBtn.setAttribute('aria-expanded', String(isOpen));
    });

    document.addEventListener('click', () => {
      dropdown.classList.remove('open');
      currencyBtn.setAttribute('aria-expanded', 'false');
    });
    dropdown.addEventListener('click', e => e.stopPropagation());

    dropdown.querySelectorAll('.currency-option').forEach(opt => {
      opt.addEventListener('click', () => {
        dropdown.querySelectorAll('.currency-option').forEach(o => o.classList.remove('active'));
        opt.classList.add('active');
        currentCode = opt.dataset.code;
        currentRate = parseFloat(opt.dataset.rate);
        if (currencyName) currencyName.textContent = currentCode;
        if (currencyIcon) currencyIcon.textContent = opt.dataset.symbol;
        if (rateDisplay)  rateDisplay.textContent  = `1 ${currentCode} = ${currentRate.toLocaleString('ru-RU')} ₽`;
        rateMinutes = 0;
        if (rateTimer) rateTimer.textContent = 'обновлён только что';
        dropdown.classList.remove('open');
        currencyBtn.setAttribute('aria-expanded', 'false');
        recalc();
      });
    });


    /* ─── LIVE RATES ─── */
    const CG_URL   = 'https://api.coingecko.com/api/v3/simple/price?ids=tether,bitcoin,ethereum&vs_currencies=rub';
    const MEXC_URL = 'https://api.mexc.com/api/v3/ticker/price?symbols=%5B%22USDTRUB%22%2C%22BTCRUB%22%2C%22ETHRUB%22%5D';
    const FIAT_URL = 'https://open.er-api.com/v6/latest/USD';

    const liveRates = { USDT: null, BTC: null, ETH: null, USD: null };
    let rateSource = '';

    const fetchFromCoinGecko = async () => {
      const res = await fetch(CG_URL, { cache: 'no-store', signal: AbortSignal.timeout(7000) });
      if (!res.ok) throw new Error('cg');
      const d = await res.json();
      liveRates.USDT = d?.tether?.rub   || null;
      liveRates.BTC  = d?.bitcoin?.rub  || null;
      liveRates.ETH  = d?.ethereum?.rub || null;
      if (!liveRates.USDT) throw new Error('cg empty');
      rateSource = 'CoinGecko';
    };

    const fetchFromMEXC = async () => {
      const res = await fetch(MEXC_URL, { cache: 'no-store', signal: AbortSignal.timeout(6000) });
      if (!res.ok) throw new Error('mexc');
      const arr = await res.json();
      if (!Array.isArray(arr)) throw new Error('mexc fmt');
      const map = Object.fromEntries(arr.map(x => [x.symbol, parseFloat(x.price)]));
      liveRates.USDT = map['USDTRUB'] || null;
      liveRates.BTC  = map['BTCRUB']  || null;
      liveRates.ETH  = map['ETHRUB']  || null;
      if (!liveRates.USDT) throw new Error('mexc empty');
      rateSource = 'MEXC';
    };

    const fetchCryptoRates = async () => {
      try { await fetchFromCoinGecko(); return true; } catch { /* fallback */ }
      try { await fetchFromMEXC();      return true; } catch { /* all failed */ }
      return false;
    };

    const fetchUSDRate = async () => {
      const res = await fetch(FIAT_URL, { cache: 'no-store', signal: AbortSignal.timeout(6000) });
      if (!res.ok) throw new Error('fiat');
      const d = await res.json();
      const rate = d?.rates?.RUB;
      if (!rate) throw new Error('fiat empty');
      liveRates.USD = rate;
    };

    const applyLiveRate = () => {
      dropdown.querySelectorAll('.currency-option').forEach(opt => {
        const live = liveRates[opt.dataset.code];
        if (live) opt.dataset.rate = String(live);
      });
      const live = liveRates[currentCode];
      if (!live) return;
      currentRate = live;
      if (rateDisplay) rateDisplay.textContent = `1 ${currentCode} = ${Math.round(live).toLocaleString('ru-RU')} ₽`;
      if (rateTimer)   rateTimer.textContent   = `обновлён · ${rateSource}`;
      rateMinutes = 0;
      recalc();
    };

    const rateRefreshBtn   = document.getElementById('rate-refresh');
    const REFRESH_COOLDOWN = 45_000;
    let lastRefreshAt  = 0;
    let cooldownId     = null;
    const rateCdEl = document.getElementById('rate-refresh-cd');

    const startCooldownDisplay = () => {
      if (cooldownId) clearInterval(cooldownId);
      rateRefreshBtn && rateRefreshBtn.classList.add('on-cooldown');
      const tick = () => {
        const rem = Math.ceil((REFRESH_COOLDOWN - (Date.now() - lastRefreshAt)) / 1000);
        if (rem <= 0) {
          clearInterval(cooldownId);
          cooldownId = null;
          if (rateCdEl) rateCdEl.textContent = '';
          rateRefreshBtn && rateRefreshBtn.classList.remove('on-cooldown');
        } else {
          if (rateCdEl) rateCdEl.textContent = `${rem}с`;
        }
      };
      tick();
      cooldownId = setInterval(tick, 1000);
    };

    const refreshAll = async () => {
      const [cryptoOk] = await Promise.all([
        fetchCryptoRates(),
        fetchUSDRate().catch(() => {
          if (liveRates.USDT) liveRates.USD = liveRates.USDT;
        })
      ]);
      if (cryptoOk) {
        lastRefreshAt = Date.now();
        applyLiveRate();
        startCooldownDisplay();
      }
      return cryptoOk;
    };

    refreshAll();
    setInterval(refreshAll, 3 * 60 * 1000);

    if (rateRefreshBtn) {
      rateRefreshBtn.addEventListener('click', async () => {
        const now = Date.now();
        if (now - lastRefreshAt < REFRESH_COOLDOWN) return;
        rateRefreshBtn.classList.add('spinning');
        rateRefreshBtn.disabled = true;
        const ok = await refreshAll();
        setTimeout(() => {
          rateRefreshBtn.classList.remove('spinning');
          rateRefreshBtn.disabled = false;
          if (!ok && !liveRates.USDT && rateTimer) {
            rateTimer.textContent = 'нет соединения — попробуйте позже';
          }
        }, 600);
      });
    }
  } /* end calculator block */

  /* ─── CITY PILLS ─── */
  document.querySelectorAll('.city-pill').forEach(pill => {
    pill.addEventListener('click', () => {
      document.querySelectorAll('.city-pill').forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
    });
  });


  /* ═══════════════════════════════════════════════════════════
     INTERACTIVE DOT MAP — exact dot positions from 1ex.ru
     ═══════════════════════════════════════════════════════════ */
  (function () {
    var wrap   = document.getElementById('map-wrap') || document.querySelector('.map-wrap');
    var canvas = document.getElementById('map-canvas');
    if (!wrap || !canvas) return;

    var ctx = canvas.getContext('2d');
    var mouseX = -1e4, mouseY = -1e4;
    var RADIUS = 100, DOT_R = 2.5, PUSH = 14, GROW = 3.5;
    var animating = false;
    var dots = [];

    /* Exact dot coordinates (normalized 0-1) traced from Russia map */
    var ND = [[0.0,0.0],[0.01961,0.0],[0.03922,0.0],[0.05882,0.0],[0.07843,0.0],[0.11765,0.0],[0.13725,0.0],[0.15686,0.0],[0.2549,0.12903],[0.27451,0.12903],[0.29412,0.12903],[0.62745,0.12903],[0.07843,0.16129],[0.09804,0.16129],[0.11765,0.16129],[0.13725,0.16129],[0.15686,0.16129],[0.2549,0.16129],[0.27451,0.16129],[0.29412,0.16129],[0.31373,0.16129],[0.33333,0.16129],[0.35294,0.16129],[0.56863,0.16129],[0.58824,0.16129],[0.60784,0.16129],[0.62745,0.16129],[0.64706,0.16129],[0.05882,0.19355],[0.07843,0.19355],[0.09804,0.19355],[0.11765,0.19355],[0.13725,0.19355],[0.15686,0.19355],[0.2549,0.19355],[0.27451,0.19355],[0.29412,0.19355],[0.31373,0.19355],[0.33333,0.19355],[0.35294,0.19355],[0.37255,0.19355],[0.39216,0.19355],[0.56863,0.19355],[0.58824,0.19355],[0.60784,0.19355],[0.62745,0.19355],[0.64706,0.19355],[0.03922,0.22581],[0.05882,0.22581],[0.07843,0.22581],[0.09804,0.22581],[0.11765,0.22581],[0.13725,0.22581],[0.15686,0.22581],[0.2549,0.22581],[0.27451,0.22581],[0.29412,0.22581],[0.31373,0.22581],[0.33333,0.22581],[0.35294,0.22581],[0.37255,0.22581],[0.39216,0.22581],[0.41176,0.22581],[0.56863,0.22581],[0.58824,0.22581],[0.60784,0.22581],[0.62745,0.22581],[0.03922,0.25806],[0.05882,0.25806],[0.07843,0.25806],[0.09804,0.25806],[0.11765,0.25806],[0.13725,0.25806],[0.27451,0.25806],[0.29412,0.25806],[0.31373,0.25806],[0.33333,0.25806],[0.35294,0.25806],[0.37255,0.25806],[0.39216,0.25806],[0.41176,0.25806],[0.43137,0.25806],[0.45098,0.25806],[0.56863,0.25806],[0.58824,0.25806],[0.60784,0.25806],[0.62745,0.25806],[0.64706,0.25806],[0.66667,0.25806],[0.68627,0.25806],[0.70588,0.25806],[0.78431,0.25806],[0.80392,0.25806],[0.84314,0.25806],[0.86275,0.25806],[0.88235,0.25806],[0.90196,0.25806],[0.92157,0.25806],[0.94118,0.25806],[0.96078,0.25806],[0.98039,0.25806],[1.0,0.25806],[0.29412,0.29032],[0.31373,0.29032],[0.33333,0.29032],[0.35294,0.29032],[0.37255,0.29032],[0.39216,0.29032],[0.41176,0.29032],[0.43137,0.29032],[0.45098,0.29032],[0.52941,0.29032],[0.54902,0.29032],[0.56863,0.29032],[0.58824,0.29032],[0.60784,0.29032],[0.62745,0.29032],[0.64706,0.29032],[0.66667,0.29032],[0.68627,0.29032],[0.70588,0.29032],[0.72549,0.29032],[0.7451,0.29032],[0.76471,0.29032],[0.78431,0.29032],[0.80392,0.29032],[0.82353,0.29032],[0.84314,0.29032],[0.86275,0.29032],[0.88235,0.29032],[0.90196,0.29032],[0.92157,0.29032],[0.94118,0.29032],[0.96078,0.29032],[0.98039,0.29032],[1.0,0.29032],[0.17647,0.32258],[0.2549,0.32258],[0.27451,0.32258],[0.29412,0.32258],[0.31373,0.32258],[0.33333,0.32258],[0.35294,0.32258],[0.37255,0.32258],[0.39216,0.32258],[0.41176,0.32258],[0.43137,0.32258],[0.45098,0.32258],[0.47059,0.32258],[0.4902,0.32258],[0.5098,0.32258],[0.52941,0.32258],[0.54902,0.32258],[0.56863,0.32258],[0.58824,0.32258],[0.60784,0.32258],[0.62745,0.32258],[0.64706,0.32258],[0.66667,0.32258],[0.68627,0.32258],[0.70588,0.32258],[0.72549,0.32258],[0.7451,0.32258],[0.76471,0.32258],[0.78431,0.32258],[0.80392,0.32258],[0.82353,0.32258],[0.84314,0.32258],[0.86275,0.32258],[0.88235,0.32258],[0.90196,0.32258],[0.92157,0.32258],[0.94118,0.32258],[0.96078,0.32258],[0.98039,0.32258],[1.0,0.32258],[0.15686,0.35484],[0.17647,0.35484],[0.2549,0.35484],[0.27451,0.35484],[0.29412,0.35484],[0.31373,0.35484],[0.33333,0.35484],[0.35294,0.35484],[0.37255,0.35484],[0.39216,0.35484],[0.41176,0.35484],[0.43137,0.35484],[0.45098,0.35484],[0.47059,0.35484],[0.4902,0.35484],[0.5098,0.35484],[0.52941,0.35484],[0.54902,0.35484],[0.56863,0.35484],[0.58824,0.35484],[0.60784,0.35484],[0.62745,0.35484],[0.64706,0.35484],[0.66667,0.35484],[0.68627,0.35484],[0.70588,0.35484],[0.72549,0.35484],[0.7451,0.35484],[0.76471,0.35484],[0.78431,0.35484],[0.80392,0.35484],[0.82353,0.35484],[0.84314,0.35484],[0.86275,0.35484],[0.88235,0.35484],[0.90196,0.35484],[0.92157,0.35484],[0.94118,0.35484],[0.96078,0.35484],[0.98039,0.35484],[1.0,0.35484],[0.13725,0.3871],[0.15686,0.3871],[0.17647,0.3871],[0.2549,0.3871],[0.27451,0.3871],[0.29412,0.3871],[0.31373,0.3871],[0.33333,0.3871],[0.35294,0.3871],[0.37255,0.3871],[0.39216,0.3871],[0.41176,0.3871],[0.43137,0.3871],[0.45098,0.3871],[0.47059,0.3871],[0.4902,0.3871],[0.5098,0.3871],[0.52941,0.3871],[0.54902,0.3871],[0.56863,0.3871],[0.58824,0.3871],[0.60784,0.3871],[0.62745,0.3871],[0.64706,0.3871],[0.66667,0.3871],[0.68627,0.3871],[0.70588,0.3871],[0.72549,0.3871],[0.7451,0.3871],[0.76471,0.3871],[0.78431,0.3871],[0.80392,0.3871],[0.82353,0.3871],[0.84314,0.3871],[0.86275,0.3871],[0.88235,0.3871],[0.90196,0.3871],[0.92157,0.3871],[0.94118,0.3871],[0.96078,0.3871],[0.98039,0.3871],[0.13725,0.41935],[0.15686,0.41935],[0.17647,0.41935],[0.21569,0.41935],[0.23529,0.41935],[0.2549,0.41935],[0.27451,0.41935],[0.29412,0.41935],[0.31373,0.41935],[0.33333,0.41935],[0.35294,0.41935],[0.37255,0.41935],[0.39216,0.41935],[0.41176,0.41935],[0.43137,0.41935],[0.45098,0.41935],[0.47059,0.41935],[0.4902,0.41935],[0.5098,0.41935],[0.52941,0.41935],[0.54902,0.41935],[0.56863,0.41935],[0.58824,0.41935],[0.60784,0.41935],[0.62745,0.41935],[0.64706,0.41935],[0.66667,0.41935],[0.68627,0.41935],[0.70588,0.41935],[0.72549,0.41935],[0.7451,0.41935],[0.76471,0.41935],[0.78431,0.41935],[0.80392,0.41935],[0.82353,0.41935],[0.84314,0.41935],[0.86275,0.41935],[0.88235,0.41935],[0.90196,0.41935],[0.92157,0.41935],[0.94118,0.41935],[0.96078,0.41935],[0.98039,0.41935],[1.0,0.41935],[0.21569,0.45161],[0.23529,0.45161],[0.2549,0.45161],[0.27451,0.45161],[0.29412,0.45161],[0.31373,0.45161],[0.33333,0.45161],[0.35294,0.45161],[0.37255,0.45161],[0.39216,0.45161],[0.41176,0.45161],[0.43137,0.45161],[0.45098,0.45161],[0.47059,0.45161],[0.4902,0.45161],[0.5098,0.45161],[0.52941,0.45161],[0.54902,0.45161],[0.56863,0.45161],[0.58824,0.45161],[0.60784,0.45161],[0.62745,0.45161],[0.64706,0.45161],[0.66667,0.45161],[0.68627,0.45161],[0.70588,0.45161],[0.72549,0.45161],[0.7451,0.45161],[0.76471,0.45161],[0.78431,0.45161],[0.80392,0.45161],[0.82353,0.45161],[0.84314,0.45161],[0.86275,0.45161],[0.88235,0.45161],[0.90196,0.45161],[0.92157,0.45161],[0.94118,0.45161],[0.96078,0.45161],[0.98039,0.45161],[1.0,0.45161],[0.21569,0.48387],[0.23529,0.48387],[0.2549,0.48387],[0.27451,0.48387],[0.29412,0.48387],[0.31373,0.48387],[0.33333,0.48387],[0.35294,0.48387],[0.37255,0.48387],[0.39216,0.48387],[0.41176,0.48387],[0.43137,0.48387],[0.45098,0.48387],[0.47059,0.48387],[0.4902,0.48387],[0.5098,0.48387],[0.52941,0.48387],[0.54902,0.48387],[0.56863,0.48387],[0.58824,0.48387],[0.60784,0.48387],[0.62745,0.48387],[0.64706,0.48387],[0.66667,0.48387],[0.68627,0.48387],[0.70588,0.48387],[0.72549,0.48387],[0.7451,0.48387],[0.76471,0.48387],[0.78431,0.48387],[0.80392,0.48387],[0.82353,0.48387],[0.84314,0.48387],[0.86275,0.48387],[0.88235,0.48387],[0.90196,0.48387],[0.92157,0.48387],[0.94118,0.48387],[0.96078,0.48387],[0.98039,0.48387],[0.11765,0.51613],[0.13725,0.51613],[0.15686,0.51613],[0.17647,0.51613],[0.19608,0.51613],[0.21569,0.51613],[0.23529,0.51613],[0.2549,0.51613],[0.27451,0.51613],[0.29412,0.51613],[0.31373,0.51613],[0.33333,0.51613],[0.35294,0.51613],[0.37255,0.51613],[0.39216,0.51613],[0.41176,0.51613],[0.43137,0.51613],[0.45098,0.51613],[0.47059,0.51613],[0.4902,0.51613],[0.5098,0.51613],[0.52941,0.51613],[0.54902,0.51613],[0.56863,0.51613],[0.58824,0.51613],[0.60784,0.51613],[0.62745,0.51613],[0.64706,0.51613],[0.66667,0.51613],[0.68627,0.51613],[0.70588,0.51613],[0.72549,0.51613],[0.7451,0.51613],[0.76471,0.51613],[0.78431,0.51613],[0.80392,0.51613],[0.82353,0.51613],[0.84314,0.51613],[0.86275,0.51613],[0.88235,0.51613],[0.90196,0.51613],[0.92157,0.51613],[0.94118,0.51613],[0.96078,0.51613],[0.98039,0.51613],[0.0,0.54839],[0.01961,0.54839],[0.03922,0.54839],[0.05882,0.54839],[0.07843,0.54839],[0.09804,0.54839],[0.11765,0.54839],[0.13725,0.54839],[0.15686,0.54839],[0.17647,0.54839],[0.19608,0.54839],[0.21569,0.54839],[0.23529,0.54839],[0.2549,0.54839],[0.27451,0.54839],[0.29412,0.54839],[0.31373,0.54839],[0.33333,0.54839],[0.35294,0.54839],[0.37255,0.54839],[0.39216,0.54839],[0.41176,0.54839],[0.43137,0.54839],[0.45098,0.54839],[0.47059,0.54839],[0.4902,0.54839],[0.5098,0.54839],[0.52941,0.54839],[0.54902,0.54839],[0.56863,0.54839],[0.58824,0.54839],[0.60784,0.54839],[0.62745,0.54839],[0.64706,0.54839],[0.66667,0.54839],[0.68627,0.54839],[0.70588,0.54839],[0.72549,0.54839],[0.7451,0.54839],[0.76471,0.54839],[0.78431,0.54839],[0.80392,0.54839],[0.82353,0.54839],[0.84314,0.54839],[0.86275,0.54839],[0.88235,0.54839],[0.90196,0.54839],[0.92157,0.54839],[0.94118,0.54839],[0.0,0.58065],[0.01961,0.58065],[0.03922,0.58065],[0.05882,0.58065],[0.07843,0.58065],[0.09804,0.58065],[0.11765,0.58065],[0.13725,0.58065],[0.15686,0.58065],[0.17647,0.58065],[0.19608,0.58065],[0.21569,0.58065],[0.23529,0.58065],[0.2549,0.58065],[0.27451,0.58065],[0.29412,0.58065],[0.31373,0.58065],[0.33333,0.58065],[0.35294,0.58065],[0.37255,0.58065],[0.39216,0.58065],[0.41176,0.58065],[0.43137,0.58065],[0.45098,0.58065],[0.47059,0.58065],[0.4902,0.58065],[0.5098,0.58065],[0.52941,0.58065],[0.54902,0.58065],[0.56863,0.58065],[0.58824,0.58065],[0.60784,0.58065],[0.62745,0.58065],[0.64706,0.58065],[0.66667,0.58065],[0.68627,0.58065],[0.70588,0.58065],[0.72549,0.58065],[0.7451,0.58065],[0.76471,0.58065],[0.78431,0.58065],[0.80392,0.58065],[0.82353,0.58065],[0.84314,0.58065],[0.86275,0.58065],[0.88235,0.58065],[0.90196,0.58065],[0.92157,0.58065],[0.94118,0.58065],[0.0,0.6129],[0.01961,0.6129],[0.03922,0.6129],[0.05882,0.6129],[0.07843,0.6129],[0.09804,0.6129],[0.11765,0.6129],[0.13725,0.6129],[0.15686,0.6129],[0.17647,0.6129],[0.19608,0.6129],[0.21569,0.6129],[0.23529,0.6129],[0.2549,0.6129],[0.27451,0.6129],[0.29412,0.6129],[0.31373,0.6129],[0.33333,0.6129],[0.35294,0.6129],[0.37255,0.6129],[0.39216,0.6129],[0.41176,0.6129],[0.43137,0.6129],[0.45098,0.6129],[0.47059,0.6129],[0.4902,0.6129],[0.5098,0.6129],[0.52941,0.6129],[0.54902,0.6129],[0.56863,0.6129],[0.58824,0.6129],[0.60784,0.6129],[0.62745,0.6129],[0.64706,0.6129],[0.66667,0.6129],[0.68627,0.6129],[0.70588,0.6129],[0.72549,0.6129],[0.7451,0.6129],[0.76471,0.6129],[0.78431,0.6129],[0.80392,0.6129],[0.82353,0.6129],[0.84314,0.6129],[0.86275,0.6129],[0.88235,0.6129],[0.90196,0.6129],[0.92157,0.6129],[0.94118,0.6129],[0.0,0.64516],[0.01961,0.64516],[0.03922,0.64516],[0.05882,0.64516],[0.07843,0.64516],[0.09804,0.64516],[0.11765,0.64516],[0.13725,0.64516],[0.15686,0.64516],[0.17647,0.64516],[0.19608,0.64516],[0.21569,0.64516],[0.23529,0.64516],[0.2549,0.64516],[0.27451,0.64516],[0.29412,0.64516],[0.31373,0.64516],[0.33333,0.64516],[0.35294,0.64516],[0.37255,0.64516],[0.39216,0.64516],[0.41176,0.64516],[0.43137,0.64516],[0.45098,0.64516],[0.47059,0.64516],[0.4902,0.64516],[0.5098,0.64516],[0.52941,0.64516],[0.54902,0.64516],[0.56863,0.64516],[0.58824,0.64516],[0.60784,0.64516],[0.62745,0.64516],[0.64706,0.64516],[0.66667,0.64516],[0.68627,0.64516],[0.70588,0.64516],[0.72549,0.64516],[0.7451,0.64516],[0.76471,0.64516],[0.78431,0.64516],[0.80392,0.64516],[0.82353,0.64516],[0.84314,0.64516],[0.86275,0.64516],[0.88235,0.64516],[0.90196,0.64516],[0.92157,0.64516],[0.94118,0.64516],[0.96078,0.64516],[0.98039,0.64516],[0.01961,0.67742],[0.03922,0.67742],[0.05882,0.67742],[0.07843,0.67742],[0.09804,0.67742],[0.11765,0.67742],[0.13725,0.67742],[0.15686,0.67742],[0.17647,0.67742],[0.19608,0.67742],[0.21569,0.67742],[0.23529,0.67742],[0.2549,0.67742],[0.27451,0.67742],[0.29412,0.67742],[0.31373,0.67742],[0.33333,0.67742],[0.35294,0.67742],[0.37255,0.67742],[0.39216,0.67742],[0.41176,0.67742],[0.43137,0.67742],[0.45098,0.67742],[0.47059,0.67742],[0.4902,0.67742],[0.5098,0.67742],[0.52941,0.67742],[0.54902,0.67742],[0.56863,0.67742],[0.58824,0.67742],[0.60784,0.67742],[0.62745,0.67742],[0.64706,0.67742],[0.66667,0.67742],[0.68627,0.67742],[0.70588,0.67742],[0.72549,0.67742],[0.7451,0.67742],[0.76471,0.67742],[0.78431,0.67742],[0.80392,0.67742],[0.82353,0.67742],[0.84314,0.67742],[0.86275,0.67742],[0.88235,0.67742],[0.90196,0.67742],[0.92157,0.67742],[0.94118,0.67742],[0.96078,0.67742],[0.98039,0.67742],[1.0,0.67742],[0.01961,0.70968],[0.03922,0.70968],[0.05882,0.70968],[0.07843,0.70968],[0.09804,0.70968],[0.11765,0.70968],[0.13725,0.70968],[0.15686,0.70968],[0.17647,0.70968],[0.19608,0.70968],[0.21569,0.70968],[0.23529,0.70968],[0.2549,0.70968],[0.27451,0.70968],[0.29412,0.70968],[0.31373,0.70968],[0.33333,0.70968],[0.35294,0.70968],[0.37255,0.70968],[0.39216,0.70968],[0.41176,0.70968],[0.43137,0.70968],[0.45098,0.70968],[0.47059,0.70968],[0.4902,0.70968],[0.5098,0.70968],[0.52941,0.70968],[0.54902,0.70968],[0.56863,0.70968],[0.58824,0.70968],[0.60784,0.70968],[0.62745,0.70968],[0.64706,0.70968],[0.66667,0.70968],[0.68627,0.70968],[0.70588,0.70968],[0.72549,0.70968],[0.7451,0.70968],[0.76471,0.70968],[0.78431,0.70968],[0.80392,0.70968],[0.82353,0.70968],[0.84314,0.70968],[0.86275,0.70968],[0.88235,0.70968],[0.90196,0.70968],[0.92157,0.70968],[0.94118,0.70968],[0.96078,0.70968],[0.0,0.74194],[0.01961,0.74194],[0.03922,0.74194],[0.05882,0.74194],[0.07843,0.74194],[0.09804,0.74194],[0.11765,0.74194],[0.13725,0.74194],[0.15686,0.74194],[0.17647,0.74194],[0.19608,0.74194],[0.21569,0.74194],[0.23529,0.74194],[0.2549,0.74194],[0.27451,0.74194],[0.29412,0.74194],[0.31373,0.74194],[0.33333,0.74194],[0.35294,0.74194],[0.37255,0.74194],[0.39216,0.74194],[0.41176,0.74194],[0.43137,0.74194],[0.45098,0.74194],[0.47059,0.74194],[0.4902,0.74194],[0.5098,0.74194],[0.52941,0.74194],[0.54902,0.74194],[0.56863,0.74194],[0.58824,0.74194],[0.60784,0.74194],[0.62745,0.74194],[0.64706,0.74194],[0.66667,0.74194],[0.68627,0.74194],[0.70588,0.74194],[0.72549,0.74194],[0.7451,0.74194],[0.76471,0.74194],[0.78431,0.74194],[0.80392,0.74194],[0.82353,0.74194],[0.84314,0.74194],[0.86275,0.74194],[0.88235,0.74194],[0.90196,0.74194],[0.92157,0.74194],[0.94118,0.74194],[0.96078,0.74194],[0.0,0.77419],[0.01961,0.77419],[0.03922,0.77419],[0.05882,0.77419],[0.07843,0.77419],[0.09804,0.77419],[0.11765,0.77419],[0.13725,0.77419],[0.15686,0.77419],[0.17647,0.77419],[0.19608,0.77419],[0.21569,0.77419],[0.23529,0.77419],[0.2549,0.77419],[0.27451,0.77419],[0.29412,0.77419],[0.31373,0.77419],[0.33333,0.77419],[0.35294,0.77419],[0.37255,0.77419],[0.39216,0.77419],[0.41176,0.77419],[0.43137,0.77419],[0.45098,0.77419],[0.47059,0.77419],[0.4902,0.77419],[0.5098,0.77419],[0.52941,0.77419],[0.54902,0.77419],[0.56863,0.77419],[0.58824,0.77419],[0.60784,0.77419],[0.62745,0.77419],[0.64706,0.77419],[0.66667,0.77419],[0.68627,0.77419],[0.70588,0.77419],[0.72549,0.77419],[0.7451,0.77419],[0.76471,0.77419],[0.78431,0.77419],[0.80392,0.77419],[0.82353,0.77419],[0.84314,0.77419],[0.86275,0.77419],[0.88235,0.77419],[0.90196,0.77419],[0.92157,0.77419],[0.94118,0.77419],[0.96078,0.77419],[0.0,0.80645],[0.01961,0.80645],[0.03922,0.80645],[0.05882,0.80645],[0.07843,0.80645],[0.09804,0.80645],[0.11765,0.80645],[0.13725,0.80645],[0.15686,0.80645],[0.17647,0.80645],[0.19608,0.80645],[0.21569,0.80645],[0.23529,0.80645],[0.2549,0.80645],[0.27451,0.80645],[0.29412,0.80645],[0.31373,0.80645],[0.33333,0.80645],[0.35294,0.80645],[0.37255,0.80645],[0.39216,0.80645],[0.41176,0.80645],[0.43137,0.80645],[0.45098,0.80645],[0.47059,0.80645],[0.4902,0.80645],[0.5098,0.80645],[0.52941,0.80645],[0.54902,0.80645],[0.56863,0.80645],[0.58824,0.80645],[0.60784,0.80645],[0.62745,0.80645],[0.64706,0.80645],[0.66667,0.80645],[0.68627,0.80645],[0.70588,0.80645],[0.72549,0.80645],[0.7451,0.80645],[0.76471,0.80645],[0.78431,0.80645],[0.80392,0.80645],[0.82353,0.80645],[0.84314,0.80645],[0.86275,0.80645],[0.88235,0.80645],[0.90196,0.80645],[0.92157,0.80645],[0.94118,0.80645],[0.0,0.83871],[0.01961,0.83871],[0.03922,0.83871],[0.05882,0.83871],[0.07843,0.83871],[0.09804,0.83871],[0.11765,0.83871],[0.13725,0.83871],[0.15686,0.83871],[0.17647,0.83871],[0.19608,0.83871],[0.21569,0.83871],[0.23529,0.83871],[0.2549,0.83871],[0.27451,0.83871],[0.29412,0.83871],[0.35294,0.83871],[0.37255,0.83871],[0.39216,0.83871],[0.41176,0.83871],[0.43137,0.83871],[0.45098,0.83871],[0.47059,0.83871],[0.4902,0.83871],[0.5098,0.83871],[0.52941,0.83871],[0.54902,0.83871],[0.56863,0.83871],[0.58824,0.83871],[0.60784,0.83871],[0.62745,0.83871],[0.64706,0.83871],[0.66667,0.83871],[0.72549,0.83871],[0.7451,0.83871],[0.76471,0.83871],[0.78431,0.83871],[0.80392,0.83871],[0.82353,0.83871],[0.84314,0.83871],[0.86275,0.83871],[0.88235,0.83871],[0.90196,0.83871],[0.92157,0.83871],[0.94118,0.83871],[0.03922,0.87097],[0.05882,0.87097],[0.07843,0.87097],[0.09804,0.87097],[0.11765,0.87097],[0.13725,0.87097],[0.15686,0.87097],[0.17647,0.87097],[0.19608,0.87097],[0.21569,0.87097],[0.23529,0.87097],[0.2549,0.87097],[0.39216,0.87097],[0.41176,0.87097],[0.43137,0.87097],[0.45098,0.87097],[0.47059,0.87097],[0.4902,0.87097],[0.5098,0.87097],[0.52941,0.87097],[0.60784,0.87097],[0.62745,0.87097],[0.76471,0.87097],[0.78431,0.87097],[0.80392,0.87097],[0.82353,0.87097],[0.84314,0.87097],[0.86275,0.87097],[0.88235,0.87097],[0.90196,0.87097],[0.92157,0.87097],[0.07843,0.90323],[0.09804,0.90323],[0.11765,0.90323],[0.13725,0.90323],[0.15686,0.90323],[0.17647,0.90323],[0.19608,0.90323],[0.21569,0.90323],[0.23529,0.90323],[0.2549,0.90323],[0.78431,0.90323],[0.80392,0.90323],[0.82353,0.90323],[0.84314,0.90323],[0.88235,0.90323],[0.90196,0.90323],[0.92157,0.90323],[0.09804,0.93548],[0.11765,0.93548],[0.13725,0.93548],[0.15686,0.93548],[0.17647,0.93548],[0.78431,0.93548],[0.80392,0.93548],[0.82353,0.93548],[0.88235,0.93548],[0.90196,0.93548],[0.09804,0.96774],[0.11765,0.96774],[0.13725,0.96774],[0.15686,0.96774],[0.17647,0.96774],[0.78431,0.96774],[0.80392,0.96774],[0.82353,0.96774],[0.09804,1.0],[0.11765,1.0],[0.13725,1.0],[0.15686,1.0],[0.17647,1.0]];

    function resize() {
      var rect = wrap.getBoundingClientRect();
      if (rect.width < 10 || rect.height < 10) return;
      var dpr = window.devicePixelRatio || 1;
      canvas.width  = rect.width  * dpr;
      canvas.height = rect.height * dpr;
      canvas.style.width  = rect.width  + 'px';
      canvas.style.height = rect.height + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var w = rect.width, h = rect.height;
      var mapW = w * 0.95, mapH = mapW / 1.82;
      if (mapH > h * 0.92) { mapH = h * 0.92; mapW = mapH * 1.82; }
      var ox = (w - mapW) / 2, oy = (h - mapH) / 2;
      dots = [];
      for (var i = 0; i < ND.length; i++) {
        var px = ox + ND[i][0] * mapW;
        var py = oy + ND[i][1] * mapH;
        dots.push({ hx: px, hy: py, x: px, y: py, r: DOT_R, a: 0.2 });
      }
      draw();
    }

    function draw() {
      var w = parseFloat(canvas.style.width);
      var h = parseFloat(canvas.style.height);
      ctx.clearRect(0, 0, w, h);
      var needAnim = false;
      for (var i = 0; i < dots.length; i++) {
        var d = dots[i];
        var dx = d.hx - mouseX, dy = d.hy - mouseY;
        var dist = Math.sqrt(dx * dx + dy * dy);
        var tx = d.hx, ty = d.hy, tr = DOT_R, ta = 0.2;
        if (dist < RADIUS && dist > 0.1) {
          var t = 1 - dist / RADIUS, t2 = t * t;
          tx = d.hx + (dx / dist) * PUSH * t2;
          ty = d.hy + (dy / dist) * PUSH * t2;
          tr = DOT_R + GROW * t2;
          ta = 0.2 + 0.8 * t;
        }
        d.x += (tx - d.x) * 0.16;
        d.y += (ty - d.y) * 0.16;
        d.r += (tr - d.r) * 0.16;
        d.a += (ta - d.a) * 0.16;
        if (Math.abs(d.x - tx) > 0.1 || Math.abs(d.y - ty) > 0.1 || Math.abs(d.r - tr) > 0.05) needAnim = true;
        ctx.fillStyle = 'rgba(180,160,110,' + d.a.toFixed(3) + ')';
        ctx.beginPath();
        ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2);
        ctx.fill();
      }
      if (needAnim) requestAnimationFrame(draw);
      else animating = false;
    }

    function startAnim() { if (!animating) { animating = true; requestAnimationFrame(draw); } }

    wrap.addEventListener('mousemove', function(e) {
      var rect = canvas.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
      startAnim();
    });
    wrap.addEventListener('mouseleave', function() {
      mouseX = -1e4; mouseY = -1e4;
      startAnim();
    });
    wrap.addEventListener('touchmove', function(e) {
      var rect = canvas.getBoundingClientRect();
      mouseX = e.touches[0].clientX - rect.left;
      mouseY = e.touches[0].clientY - rect.top;
      startAnim();
    }, { passive: true });
    wrap.addEventListener('touchend', function() {
      mouseX = -1e4; mouseY = -1e4;
      startAnim();
    });

    window.addEventListener('resize', function() { resize(); });
    setTimeout(resize, 100);
    setTimeout(resize, 500);
    if (document.readyState === 'complete') resize();
    else window.addEventListener('load', resize);
  })();


  /* ─── MAP PINS & POPUPS ─── */
  const pins = document.querySelectorAll('.map-pin');

  const checkOpen = () => {
    const now = new Date();
    const utc = now.getTime() + now.getTimezoneOffset() * 60000;
    const msk = new Date(utc + 3600000 * 3);
    const day  = msk.getDay();
    const hour = msk.getHours();
    return day >= 1 && day <= 6 && hour >= 10 && hour < 19;
  };

  const isOpen = checkOpen();

  /* Hero badge + CTA badge */
  const heroBadgeStatus = document.getElementById('hero-badge-status');
  const heroBadgeDot    = document.getElementById('hero-badge-dot');
  const ctaBadgeStatus  = document.getElementById('cta-badge-status');
  const ctaBadgeDot     = document.getElementById('cta-badge-dot');

  const heroBadgeEl  = document.getElementById('hero-badge');
  const ctaBadgeEl   = document.getElementById('cta-badge');
  const ctaBadgeHours = document.getElementById('cta-badge-hours');

  if (isOpen) {
    if (ctaBadgeStatus) ctaBadgeStatus.textContent = 'Менеджер онлайн · ответит в течение минуты';
  } else {
    if (heroBadgeEl)     heroBadgeEl.classList.add('offline');
    if (ctaBadgeEl)      ctaBadgeEl.classList.add('offline');
    if (heroBadgeStatus) heroBadgeStatus.textContent  = 'Менеджер недоступен';
    if (heroBadgeDot)    heroBadgeDot.style.background = '#ef4444';
    if (ctaBadgeDot)     ctaBadgeDot.style.background  = '#ef4444';
    if (ctaBadgeStatus)  ctaBadgeStatus.textContent   = 'Менеджер недоступен';
    if (ctaBadgeHours)   ctaBadgeHours.textContent    = 'Пн–Сб 10:00–19:00 МСК';
  }

  ['ufa', 'kazan', 'ekb'].forEach(city => {
    const statusEl = document.getElementById(`status-${city}`);
    if (!statusEl) return;
    const dot  = statusEl.querySelector('.hours-dot');
    const text = statusEl.querySelector('.hours-text');
    if (isOpen) {
      dot.style.background = '#22c55e';
      text.textContent = 'Открыто · Пн–Сб: 10:00–19:00';
    } else {
      dot.style.background = '#ef4444';
      text.textContent = 'Закрыто · Открываемся в 10:00';
    }
  });

  let activePin = null;

  const closeAllPopups = () => {
    document.querySelectorAll('.map-popup').forEach(p => p.classList.remove('active'));
    pins.forEach(p => p.classList.remove('active'));
    activePin = null;
  };

  pins.forEach(pin => {
    const city  = pin.dataset.city;
    const popup = document.getElementById(`popup-${city}`);

    const toggle = () => {
      if (activePin === pin) { closeAllPopups(); return; }
      closeAllPopups();
      pin.classList.add('active');
      popup && popup.classList.add('active');
      activePin = pin;
    };

    pin.addEventListener('click', toggle);
    pin.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(); }
    });
  });

  document.addEventListener('click', (e) => {
    if (!e.target.closest('.map-pin') && !e.target.closest('.map-popup')) {
      closeAllPopups();
    }
  });


  /* ─── FAQ ACCORDION ─── */
  document.querySelectorAll('.faq-q').forEach(btn => {
    btn.addEventListener('click', () => {
      const item   = btn.closest('.faq-item');
      const answer = item.querySelector('.faq-a');
      const wasOpen = btn.getAttribute('aria-expanded') === 'true';

      document.querySelectorAll('.faq-q').forEach(b => {
        b.setAttribute('aria-expanded', 'false');
        b.closest('.faq-item').querySelector('.faq-a').classList.remove('open');
      });

      if (!wasOpen) {
        btn.setAttribute('aria-expanded', 'true');
        answer.classList.add('open');
      }
    });
  });


  /* ─── CALL MODAL ─── */
  const callModal    = document.getElementById('call-modal');
  const callBackdrop = document.getElementById('call-modal-backdrop');
  const callClose    = document.getElementById('call-modal-close');

  const openCallModal = () => {
    callModal.classList.add('open');
    callModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
    callClose.focus();
  };

  const closeCallModal = () => {
    callModal.classList.remove('open');
    callModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  };

  document.querySelectorAll('.call-trigger').forEach(btn => {
    btn.addEventListener('click', openCallModal);
  });

  callClose.addEventListener('click', closeCallModal);
  callBackdrop.addEventListener('click', closeCallModal);

  callModal.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeCallModal();
  });


  /* ─── SMOOTH ANCHOR SCROLL ─── */
  document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', (e) => {
      const id = link.getAttribute('href').slice(1);
      const el = document.getElementById(id);
      if (!el) return;
      e.preventDefault();
      const offset = header.offsetHeight + 16;
      const top    = el.getBoundingClientRect().top + window.scrollY - offset;
      window.scrollTo({ top, behavior: 'smooth' });
    });
  });


  /* ─── ACTIVE NAV DROPDOWN ITEM ─── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-dropdown-item').forEach(item => {
    const href = item.getAttribute('href') || '';
    const base = href.replace('.html', '');
    if (currentPath.endsWith(href) || (base && currentPath.endsWith(base))) {
      item.classList.add('active');
    }
  });


  /* ─── SCROLL REVEAL ─── */
  const revealEls = document.querySelectorAll(
    '.adv-card, .step-item, .trust-card, .office-card, .faq-item, .seg-for-whom-item'
  );

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity   = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12 });

  revealEls.forEach((el, i) => {
    el.style.opacity    = '0';
    el.style.transform  = 'translateY(20px)';
    el.style.transition = `opacity 0.45s ease ${(i % 6) * 0.07}s, transform 0.45s ease ${(i % 6) * 0.07}s`;
    observer.observe(el);
  });

});
