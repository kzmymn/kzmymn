// Usage: node capture.js <mg.html> <ring_dir> <out_dir> [start end]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [html, ringDir, out, s = '0', e = '449'] = process.argv.slice(2);
  fs.mkdirSync(out, { recursive: true });
  const src = fs.readFileSync(html, 'utf8').replace(/RING\//g, 'file://' + path.resolve(ringDir) + '/');
  const tmp = path.join(path.dirname(path.resolve(html)), '.mg_run.html'); fs.writeFileSync(tmp, src);
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] }); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + tmp); await p.evaluate(() => window.ready);
  for (let f = +s; f <= +e; f++) {
    await p.evaluate(f => window.drawFrame(f), f);
    await p.locator('#c').screenshot({ path: path.join(out, `m_${String(f + 1).padStart(4, '0')}.png`) });
  }
  await b.close(); fs.unlinkSync(tmp);
})();
