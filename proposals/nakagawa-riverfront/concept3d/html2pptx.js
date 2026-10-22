// Convert a single-page HTML slide into an editable PPTX (shapes + text boxes + images).
// Usage: node html2pptx.js <slide.html> <out.pptx> <pptxgenjs dir> <work dir>
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path'); const { execFileSync } = require('child_process');
const [html, out, pgDir, work] = process.argv.slice(2);
const pptxgen = require(path.join(pgDir, 'node_modules/pptxgenjs'));
fs.mkdirSync(work, { recursive: true });
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1123, height: 794 } });
  await p.goto('file://' + path.resolve(html), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  const data = await p.evaluate(() => {
    const page = document.querySelector('.page'), P = page.getBoundingClientRect();
    const hex = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const v = m[1].split(',').map(s => parseFloat(s)); if (v.length > 3 && v[3] === 0) return null; return { hex: v.slice(0, 3).map(x => Math.round(x).toString(16).padStart(2, '0')).join('').toUpperCase(), a: v.length > 3 ? v[3] : 1 }; };
    const rel = r => ({ x: r.left - P.left, y: r.top - P.top, w: r.width, h: r.height });
    const shapes = [], lines = [], images = [], texts = [];
    const inlineD = d => d === 'inline';
    for (const el of page.querySelectorAll('*')) {
      const cs = getComputedStyle(el); const r = el.getBoundingClientRect(); if (!r.width || !r.height) continue;
      const bg = hex(cs.backgroundColor);
      if (bg) shapes.push({ ...rel(r), fill: bg.hex, a: bg.a, z: shapes.length });
      for (const side of ['Top', 'Right', 'Bottom', 'Left']) {
        const w = parseFloat(cs['border' + side + 'Width']); const c = hex(cs['border' + side + 'Color']);
        if (w > 0 && c && cs['border' + side + 'Style'] !== 'none') {
          const R = rel(r); let x1, y1, x2, y2;
          if (side === 'Top') { x1 = R.x; y1 = R.y + w / 2; x2 = R.x + R.w; y2 = y1; }
          if (side === 'Bottom') { x1 = R.x; y1 = R.y + R.h - w / 2; x2 = R.x + R.w; y2 = y1; }
          if (side === 'Left') { x1 = R.x + w / 2; y1 = R.y; x2 = x1; y2 = R.y + R.h; }
          if (side === 'Right') { x1 = R.x + R.w - w / 2; y1 = R.y; x2 = x1; y2 = R.y + R.h; }
          lines.push({ x1, y1, x2, y2, w, color: c.hex });
        }
      }
      if (el.tagName === 'IMG') images.push({ ...rel(r), src: el.src, fit: cs.objectFit });
      if (inlineD(cs.display) || el.tagName === 'IMG' || el.tagName === 'BR') continue;
      // text container: has direct text or only inline children
      const kids = [...el.childNodes];
      const hasText = kids.some(n => n.nodeType === 3 && n.textContent.trim()) || kids.some(n => n.nodeType === 1 && inlineD(getComputedStyle(n).display) && n.textContent.trim());
      const blockKidsWithText = kids.some(n => n.nodeType === 1 && !inlineD(getComputedStyle(n).display) && n.tagName !== 'BR' && n.textContent.trim());
      if (!hasText) continue;
      if (blockKidsWithText) {
        // anonymous text runs that sit beside block children: place each by its own range rect
        for (const n of kids) {
          if (!n.textContent.trim()) continue;
          if (n.nodeType === 1 && !inlineD(getComputedStyle(n).display)) continue;
          if (n.nodeType === 1 && n.tagName === 'BR') continue;
          const rg = document.createRange(); rg.selectNodeContents(n); const rr = rg.getBoundingClientRect();
          if (n.nodeType === 1) {
            const c = getComputedStyle(n); const R2 = rel(rr);
            texts.push({ x: R2.x, y: R2.y, w: R2.w, h: R2.h, align: 'left', lh: c.lineHeight === 'normal' ? 1.3 : parseFloat(c.lineHeight) / parseFloat(c.fontSize), va: 'top',
              runs: [{ t: n.textContent.replace(/\s+/g, ' ').trim(), size: parseFloat(c.fontSize), bold: parseInt(c.fontWeight) >= 600, color: hex(c.color)?.hex || '000000', font: c.fontFamily.split(',')[0].replace(/["']/g, '').trim(), ls: parseFloat(c.letterSpacing) || 0, hl: null }] });
            continue;
          }
          const R2 = rel(rr);
          texts.push({ x: R2.x, y: R2.y, w: R2.w, h: R2.h, align: 'left', lh: cs.lineHeight === 'normal' ? 1.3 : parseFloat(cs.lineHeight) / parseFloat(cs.fontSize), va: 'top',
            runs: [{ t: n.textContent.replace(/\s+/g, ' ').trim(), size: parseFloat(cs.fontSize), bold: parseInt(cs.fontWeight) >= 600, color: hex(cs.color)?.hex || '000000', font: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(), ls: parseFloat(cs.letterSpacing) || 0, hl: null }] });
        }
        continue;
      }
      const runs = [];
      const walk = (node, st) => {
        for (const n of node.childNodes) {
          if (n.nodeType === 3) { const t = n.textContent.replace(/\s+/g, ' '); if (t.trim() || (t === ' ' && runs.length)) runs.push({ t, ...st }); }
          else if (n.tagName === 'BR') runs.push({ br: true });
          else if (n.nodeType === 1) {
            const c = getComputedStyle(n);
            const pad = hex(c.backgroundColor) && !c.backgroundImage.includes('gradient');
            if (pad) runs.push({ t: '\u2002', size: parseFloat(c.fontSize), bold: false, color: 'FFFFFF', font: c.fontFamily.split(',')[0].replace(/["']/g, '').trim(), ls: 0 });
            walk(n, { size: parseFloat(c.fontSize), bold: parseInt(c.fontWeight) >= 600, color: hex(c.color)?.hex || '000000', font: c.fontFamily.split(',')[0].replace(/["']/g, '').trim(), ls: parseFloat(c.letterSpacing) || 0, hl: c.backgroundImage.includes('gradient') ? 'CDEBE6' : null, tf: c.textTransform });
            if (pad) runs.push({ t: '\u2002\u2002', size: parseFloat(c.fontSize), bold: false, color: 'FFFFFF', font: c.fontFamily.split(',')[0].replace(/["']/g, '').trim(), ls: 0 });
          }
        }
      };
      walk(el, { size: parseFloat(cs.fontSize), bold: parseInt(cs.fontWeight) >= 600, color: hex(cs.color)?.hex || '000000', font: cs.fontFamily.split(',')[0].replace(/["']/g, '').trim(), ls: parseFloat(cs.letterSpacing) || 0, hl: null });
      // trim leading/trailing spaces
      if (runs.length && runs[0].t && runs[0].t !== '\u2002') runs[0].t = runs[0].t.replace(/^[ \t\n]+/, ''); const lr = [...runs].reverse().find(r => r.t); if (lr) lr.t = lr.t.replace(/[ \t\n]+$/, '');
      const pl = parseFloat(cs.paddingLeft), pr = parseFloat(cs.paddingRight), pt = parseFloat(cs.paddingTop), pb = parseFloat(cs.paddingBottom);
      const R = rel(r);
      const lh = cs.lineHeight === 'normal' ? 1.3 : parseFloat(cs.lineHeight) / parseFloat(cs.fontSize);
      texts.push({ x: R.x + pl, y: R.y + pt, w: R.w - pl - pr, h: R.h - pt - pb, align: cs.textAlign === 'center' ? 'center' : (cs.textAlign === 'right' || cs.textAlign === 'end') ? 'right' : 'left', lh, runs, va: (cs.display.includes('flex') && cs.alignItems === 'center') ? 'middle' : 'top' });
    }
    return { W: P.width, H: P.height, shapes, lines, images, texts };
  });
  await b.close();
  const px = v => v / 96;               // CSS px -> inch
  const pt = v => v * 0.75;             // CSS px -> pt
  const pres = new pptxgen(); pres.defineLayout({ name: 'A4L', width: px(data.W), height: px(data.H) }); pres.layout = 'A4L';
  pres.title = path.basename(out, '.pptx');
  const s = pres.addSlide(); s.background = { color: 'FFFFFF' };
  for (const r of data.shapes) s.addShape(pres.shapes.RECTANGLE, { x: px(r.x), y: px(r.y), w: px(r.w), h: px(r.h), fill: { color: r.fill, transparency: Math.round((1 - r.a) * 100) }, line: { type: 'none' } });
  let k = 0;
  for (const im of data.images) {
    const src = decodeURIComponent(im.src.replace('file://', '')); const o = path.join(work, `img${k++}.jpg`);
    const W = Math.round(im.w * 3), H = Math.round(im.h * 3);
    execFileSync('convert', [src, '-resize', `${W}x${H}^`, '-gravity', 'center', '-extent', `${W}x${H}`, '-quality', '88', o]);
    s.addImage({ path: o, x: px(im.x), y: px(im.y), w: px(im.w), h: px(im.h) });
  }
  for (const l of data.lines) {
    const horiz = Math.abs(l.y1 - l.y2) < 0.01;
    s.addShape(pres.shapes.LINE, { x: px(Math.min(l.x1, l.x2)), y: px(Math.min(l.y1, l.y2)), w: horiz ? px(Math.abs(l.x2 - l.x1)) : 0, h: horiz ? 0 : px(Math.abs(l.y2 - l.y1)), line: { color: l.color, width: Math.max(0.25, pt(l.w)) } });
  }
  for (const t of data.texts) {
    const arr = []; const runs = t.runs;
    for (let i = 0; i < runs.length; i++) {
      const r = runs[i]; if (r.br) { if (arr.length) arr[arr.length - 1].options.breakLine = true; else arr.push({ text: '', options: { breakLine: true } }); continue; }
      const o = { fontFace: r.font, fontSize: +pt(r.size).toFixed(1), bold: r.bold, color: r.color, charSpacing: +(pt(r.ls)).toFixed(2) };
      if (r.hl) o.highlight = r.hl;
      arr.push({ text: r.t, options: o });
    }
    if (!arr.length) continue;
    const extra = t.align === 'left' ? Math.min(t.w * 0.03, 6) : 0;
    s.addText(arr, { x: px(t.x), y: px(t.y), w: px(t.w + extra), h: px(Math.max(t.h, 4)), margin: 0, align: t.align, valign: t.va, lineSpacingMultiple: +t.lh.toFixed(2), isTextBox: true, fit: 'none', wrap: true });
  }
  await pres.writeFile({ fileName: out });
  console.log(`shapes ${data.shapes.length} lines ${data.lines.length} images ${data.images.length} texts ${data.texts.length}`);
})();
