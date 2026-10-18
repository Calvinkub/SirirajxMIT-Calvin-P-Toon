import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { resolve, extname, sep } from 'node:path';

const root = resolve(fileURLToPath(new URL('../', import.meta.url)));
const types = { '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml' };
createServer(async (req, res) => {
  try {
    const path = resolve(root, '.' + decodeURIComponent(new URL(req.url, 'http://localhost').pathname));
    if (!path.startsWith(root + sep) && path !== root) throw new Error('Invalid path');
    const target = path === root ? resolve(root, 'index.html') : path;
    if (!['index.html', 'styles.css', 'app.js', 'safety.js', 'runtime.js', 'access.js', 'demo/agent-flow-demo.html'].includes(target.slice(root.length + 1))) {
      res.writeHead(404).end('Not found'); return;
    }
    res.writeHead(200, { 'Content-Type': `${types[extname(target)]}; charset=utf-8`, 'Cache-Control': 'no-store' });
    res.end(await readFile(target));
  } catch { res.writeHead(404).end('Not found'); }
}).listen(Number(process.env.PORT || 5173), '127.0.0.1', () => console.log(`Local: http://127.0.0.1:${process.env.PORT || 5173}`));
