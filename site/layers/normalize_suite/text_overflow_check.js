() => {
  const TOL = 2;
  const INK_TOL = 5;
  const skipSel = '[aria-hidden="true"],svg,script,style,noscript,dialog:not([open]),[hidden],.vh,.sr,.sr-only,.skip,.f-skip';
  const vis = e => {
    const s = getComputedStyle(e);
    if (s.visibility === 'hidden' || s.display === 'none' || +s.opacity === 0) return false;
    if (s.position === 'absolute' && s.clip !== 'auto' && e.getBoundingClientRect().width <= 1) return false;
    const r = e.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  };
  const isCutOff = e => {
    const s = getComputedStyle(e);
    const r = e.getBoundingClientRect();
    const clipped = s.clip && s.clip !== 'auto' && !/^rect\(\s*auto/i.test(s.clip);
    if (clipped && (s.overflow === 'hidden' || s.overflowX === 'hidden') && r.width <= 2) return true;
    if ((s.position === 'absolute' || s.position === 'fixed') && (s.overflow === 'hidden' || s.overflowX === 'hidden') && r.width <= 1 && r.height <= 1) return true;
    return false;
  };
  const inCutOff = e => { let x = e; while (x && x !== document.body) { if (isCutOff(x)) return true; x = x.parentElement; } return false; };
  const inHScroll = e => {
    let x = e;
    while (x && x !== document.body) {
      const s = getComputedStyle(x);
      const ox = s.overflowX;
      if ((ox === 'auto' || ox === 'scroll') && x.scrollWidth > x.clientWidth + 1) return true;
      x = x.parentElement;
    }
    return false;
  };
  const clipped = e => {
    const s = getComputedStyle(e);
    return (s.overflowX === 'hidden' || s.overflow === 'hidden') && (s.textOverflow === 'ellipsis' || s.whiteSpace === 'nowrap');
  };
  const nm = e => {
    const id = e.id ? '#' + e.id : '';
    return (e.tagName + id + '.' + [...e.classList].slice(0, 3).join('.')).replace(/\.$/, '');
  };
  const issues = [];
  const seen = new Set();
  const add = o => {
    const k = [o.kind, o.el, o.t, o.w].join('|');
    if (seen.has(k)) return;
    seen.add(k);
    issues.push(o);
  };

  for (const e of document.querySelectorAll('body *')) {
    if (!vis(e) || e.closest(skipSel) || inHScroll(e) || inCutOff(e) || clipped(e)) continue;
    const s = getComputedStyle(e);
    if (s.position === 'fixed') continue;
    if (e.scrollWidth > e.clientWidth + TOL) {
      add({
        kind: 'scrollWidth',
        el: nm(e),
        t: (e.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 60),
        scroll: e.scrollWidth,
        client: e.clientWidth,
        over: e.scrollWidth - e.clientWidth,
        w: innerWidth
      });
    }
  }

  const borderBox = e => {
    const r = e.getBoundingClientRect();
    return {l: r.left, r: r.right, t: r.top, b: r.bottom, el: e};
  };
  const cardOf = e => e.closest('a,button,li,article,figure,td,th,.card,.wrl a,.steps li,.gc,.pst,.rx-t,.band > div,label,h1,h2,h3,h4,p,dt,dd,blockquote,aside');

  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  let n;
  while ((n = walker.nextNode())) {
    const t = n.textContent;
    if (!t || !t.trim()) continue;
    const p = n.parentElement;
    if (!p || !vis(p) || p.closest(skipSel) || inHScroll(p) || inCutOff(p) || clipped(p) || clipped(p.parentElement || p)) continue;
    const cs = getComputedStyle(p);
    if (cs.position === 'fixed') continue;
    const range = document.createRange();
    range.selectNodeContents(n);
    const rects = range.getClientRects();
    if (!rects.length) continue;
    const selfBox = borderBox(p);
    const card = cardOf(p);
    const cardBox = card && card !== p ? borderBox(card) : null;
    for (const r of rects) {
      if (r.width < 1 || r.height < 1) continue;
      const check = (box, kind) => {
        const spillL = box.l - r.left, spillR = r.right - box.r, spillT = box.t - r.top, spillB = r.bottom - box.b;
        // Vertical glyph overflow from a tight line-height is normal typography.
        // This gate fails on horizontal overflow (text escaping a card or container).
        if (spillL > INK_TOL || spillR > INK_TOL) {
          add({
            kind,
            el: nm(box.el),
            t: t.trim().replace(/\s+/g, ' ').slice(0, 60),
            spill: {
              L: Math.round(Math.max(0, spillL)),
              R: Math.round(Math.max(0, spillR)),
              T: Math.round(Math.max(0, spillT)),
              B: Math.round(Math.max(0, spillB))
            },
            w: innerWidth
          });
        }
      };
      check(selfBox, 'spillSelf');
      if (cardBox) check(cardBox, 'spillCard');
    }
  }

  return {
    n: issues.length,
    issues: issues.slice(0, 40),
    pageOverflow: document.documentElement.scrollWidth > innerWidth + 1
  };
}
