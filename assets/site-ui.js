/*!
 * UAV-Survey — shared page UI (settings button + light/dark theme)
 * Loaded by every sub-page. Self-contained: never depends on the host page CSS.
 */

(function () {
  'use strict';

  var KEY = 'theme';                       // shared with the home page toggle
  var root = document.documentElement;

  /* ---------- 1. work out the page's own look ---------- */
  function parseLum(str) {
    str = (str || '').trim();
    var h = str.match(/^#([0-9a-f]{3}|[0-9a-f]{6})$/i);
    if (h) {
      var v = h[1];
      if (v.length === 3) v = v[0] + v[0] + v[1] + v[1] + v[2] + v[2];
      var r = parseInt(v.substr(0, 2), 16), g = parseInt(v.substr(2, 2), 16), b = parseInt(v.substr(4, 2), 16);
      return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
    }
    var m = str.match(/rgba?\(([^)]+)\)/i);
    if (m) {
      var p = m[1].split(/[,\s/]+/).map(parseFloat);
      if (p.length >= 3) {
        if (p.length > 3 && p[3] < 0.1) return null;
        return (0.2126 * p[0] + 0.7152 * p[1] + 0.0722 * p[2]) / 255;
      }
    }
    return null;
  }

  function cssVar(el, name) {
    try {
      var v = getComputedStyle(el).getPropertyValue(name);
      return v ? v.trim() : '';
    } catch (e) { return ''; }
  }

  function detectNatural() {
    var lum = parseLum(cssVar(root, '--bg'));
    if (lum === null) lum = parseLum(cssVar(document.body, '--bg'));
    if (lum === null) lum = parseLum(getComputedStyle(document.body).backgroundColor);
    if (lum === null) lum = parseLum(getComputedStyle(root).backgroundColor);
    if (lum === null) {
      // last resort: read the <style> text (works even without layout)
      var css = '';
      var sheets = document.querySelectorAll('style');
      for (var i = 0; i < sheets.length; i++) css += (sheets[i].textContent || '');
      var mv = css.match(/--bg\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([^)]*\))/);
      if (mv) lum = parseLum(mv[1]);
      if (lum === null) {
        var mb = css.match(/body\s*\{[^}]*background(?:-color)?\s*:\s*(#[0-9a-fA-F]{3,6}|rgba?\([^)]*\))/i);
        if (mb) lum = parseLum(mb[1]);
      }
    }
    return lum === null ? 'dark' : (lum > 0.5 ? 'light' : 'dark');
  }

  var nat = detectNatural();
  root.classList.add('uav-natural-' + nat);

  /* ---------- 2. theme application ---------- */
  function stored() {
    try {
      var v = localStorage.getItem(KEY);
      return v === 'light' || v === 'dark' ? v : null;
    } catch (e) { return null; }
  }

  var state = stored() || nat;

  function apply(mode) {
    state = mode;
    root.classList.remove('uav-theme-light', 'uav-theme-dark');
    root.classList.add('uav-theme-' + mode);
    root.setAttribute('data-theme', mode);
    if (document.body) document.body.classList.toggle('light', mode === 'light');
    var btns = document.querySelectorAll('[data-uav-pick]');
    for (var i = 0; i < btns.length; i++) {
      var on = btns[i].getAttribute('data-uav-pick') === mode;
      btns[i].classList.toggle('on', on);
      btns[i].setAttribute('aria-pressed', on ? 'true' : 'false');
    }
  }

  function save(mode) {
    try { localStorage.setItem(KEY, mode); } catch (e) {}
    apply(mode);
  }

  /* ---------- 3. UI ---------- */
  var btn, pop;

  function findNav() {
    var cands = ['nav.topbar', 'nav.topnav', 'nav', '.topbar', '.topnav'];
    for (var i = 0; i < cands.length; i++) {
      var el = document.querySelector(cands[i]);
      if (el && el.parentNode) return el;
    }
    return null;
  }

  function build() {
    btn = document.createElement('button');
    btn.type = 'button';
    btn.id = 'uavSetBtn';
    btn.className = 'uav-set-btn';
    btn.title = '设置 / Settings';
    btn.setAttribute('aria-label', '设置');
    btn.setAttribute('aria-haspopup', 'true');
    btn.innerHTML = '⚙️';

    var nav = findNav();
    if (nav) {
      btn.classList.add('uav-in-nav');
      nav.classList.add('uav-nav-host');
      nav.appendChild(btn);
    } else {
      btn.classList.add('uav-fab');
      document.body.appendChild(btn);
    }

    pop = document.createElement('div');
    pop.id = 'uavSetPop';
    pop.className = 'uav-set-pop';
    pop.setAttribute('role', 'dialog');
    pop.setAttribute('aria-label', '外观设置');
    pop.innerHTML =
      '<div class="uav-hd">外观 · Appearance</div>' +
      '<div class="uav-seg">' +
        '<button type="button" data-uav-pick="dark">🌙 深色</button>' +
        '<button type="button" data-uav-pick="light">☀️ 浅色</button>' +
      '</div>';
    document.body.appendChild(pop);

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      togglePop(!pop.classList.contains('open'));
    });

    pop.addEventListener('click', function (e) {
      var t = e.target.closest ? e.target.closest('[data-uav-pick]') : null;
      if (!t) return;
      save(t.getAttribute('data-uav-pick'));
      togglePop(false);
    });

    document.addEventListener('click', function (e) {
      if (!pop.classList.contains('open')) return;
      if (pop.contains(e.target) || btn.contains(e.target)) return;
      togglePop(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') togglePop(false);
    });
    window.addEventListener('resize', function () {
      if (pop.classList.contains('open')) place();
    });
  }

  function place() {
    var r = btn.getBoundingClientRect();
    var w = pop.offsetWidth || 200;
    var left = Math.min(Math.max(8, r.right - w), window.innerWidth - w - 8);
    var top = r.bottom + 8;
    if (top + pop.offsetHeight > window.innerHeight - 8) top = Math.max(8, r.top - pop.offsetHeight - 8);
    pop.style.left = left + 'px';
    pop.style.top = top + 'px';
  }

  function togglePop(open) {
    pop.classList.toggle('open', open);
    if (open) place();
  }

  function boot() {
    build();
    apply(state);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
