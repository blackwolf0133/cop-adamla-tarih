import puppeteer from 'puppeteer-core'; import fs from 'node:fs';
import { startServer } from './serve.mjs'; import { findChrome } from './chrome.mjs';
const { server, port } = await startServer();
const b = await puppeteer.launch({ executablePath: findChrome(), headless: 'new' });
const p = await b.newPage(); p.on('pageerror', e => console.log('PAGEERROR', e.message));
await p.goto(`http://127.0.0.1:${port}/engine/profil.html`); await p.waitForFunction(() => window.__ready);
const url = await p.evaluate(() => document.getElementById('sheet').toDataURL('image/png'));
fs.writeFileSync(process.argv[2] || '/tmp/profil.png', Buffer.from(url.split(',')[1], 'base64')); await b.close(); server.close();
