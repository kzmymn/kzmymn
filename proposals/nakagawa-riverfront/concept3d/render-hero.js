// Usage: node render-hero.js <hero.html> <three.module.js> <out.png|out.svg> [three/examples/jsm dir]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const [html, three, out, addons] = process.argv.slice(2);
  const src = fs.readFileSync(html, 'utf8').replace('THREE_PATH', 'file://' + path.resolve(three)).replace('ADDONS_PATH', addons ? 'file://' + path.resolve(addons) + '/' : '');
  const tmp = path.join(path.dirname(path.resolve(html)), '.hero_run.html'); fs.writeFileSync(tmp, src);
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--allow-file-access-from-files'] });
  const p = await b.newPage(); p.on('console', m => console.log('page:', m.text())); p.on('pageerror', e => console.log('err:', e.message));
  await p.goto('file://' + tmp); await p.waitForFunction(() => window.done, null, { timeout: 60000 });
  const d = await p.evaluate(() => window.done); fs.writeFileSync(out, d.startsWith('data:') ? Buffer.from(d.split(',')[1], 'base64') : d);
  await b.close(); fs.unlinkSync(tmp);
})();
