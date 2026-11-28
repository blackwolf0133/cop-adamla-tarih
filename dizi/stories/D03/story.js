// Çapkın Nihat · Bölüm 3 · "Vanilya"
// Setler: SALON PENCERESİ (x≈200, sabah), ANTRE (x≈100, sabah), APARTMAN MERDİVENİ (x≈300, akşam; ev.js'te yeni).
// Her şey satır saatlerine bağlı: Lb('L06') = satırın başı, Wd('L06', 3) = o satırın 4. kelimesinin başı (voice/words.json).
// İç ses satırlarında ağız oynamaz; yalnızca yüksek sesle konuşanın ağzı oynar (Ayça L08, L10; Nihat L09, L11).
import * as THREE from 'three';
import { Toon, Arm3D, flap, blinkAt } from '/engine/src/toon.js';
import { CamPath, smoother } from '/engine/src/camera.js';
import { Smoke } from '/engine/src/fx.js';
import { flat, D } from '/engine/src/paint.js';
import { LOOK as KADRO } from '/lib/kadro.js';
import { antre, salonPencere, merdiven, AN, SP, MD, V, HDR, texOf, shadows } from '/lib/ev.js';

export const NAME = 'capkin-nihat-03';
export const FPS = 30;
export let DUR = 50;
export const CUES = [];
export const LOOK = KADRO;
export const BOLUM = { no: 3, ad: 'Vanilya', soru: 'Sence vanilya kokan kadın kim?', sonraki: '4. BÖLÜM YARIN 20.00' };

const S = smoother;
const ramp = (t, a, b) => S((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
let C, LINES, WORDS, cast = {}, sets = {}, dyn = {};
const Lb = id => LINES.find(l => l.id === id).start;
const Le = id => LINES.find(l => l.id === id).end;
const Wd = (id, n) => WORDS.filter(w => w.line === id)[n].start;
const END = 3.2;

const AY = SP.aycaPos;                                   // salon: Ayça pencerenin önünde
const SEPET = V(199.35, 0, -1.3);
const GOMLEK_EL = V(200.44, 1.2, -.7), GOMLEK_BURUN = V(200.34, 1.42, -.74);
const PH = V(199.72, 1.2, -.2);
const NIHAT = V(98.98, 0, -1.75), AYCA_AN = V(101.0, 0, -1.0);
const AY_MD0 = V(299.1, 0, -1.6), AY_MD = V(300.4, 0, -.85);

// ---------------------------------------------------------------- kamera
function cameraPath() {
  const k = [];
  const key = (t, pos, look, fov, move = 'glide', dur = .6, extra = {}) => k.push({ t, pos, look, fov, move, dur, ...extra });
  // kanca: sepetten çıkan gömlek -> Ayça gömlekle
  key(0, [199.78, 1.3, -.2], [199.4, .55, -1.3], 36, 'cut', 0, { creep: .25, drift: .03 });
  key(Wd('L01', 2) - .1, [200.45, 1.5, 1.4], [200.2, 1.3, -1.0], 40, 'glide', .8, { creep: .12, drift: .04 });
  // vanilya: yaklaş
  key(Lb('L03') - .1, [200.4, 1.5, 1.15], [200.25, 1.3, -.9], 40, 'glide', .6, { creep: .1, drift: .03 });
  // silinen arama (elde telefon)
  key(Lb('L05') - .05, [PH.x + .08, PH.y + .1, PH.z + .6], [PH.x, PH.y, PH.z], 26, 'whip', .28, { creep: .12, drift: .01 });
  // yaka: saç teli (sert kesme)
  key(Lb('L06') - .05, [200.5, 1.2, -.15], [200.44, 1.14, -.7], 30, 'cut', 0, { creep: .2, drift: .01 });
  // Ayça'nın yüzü
  key(Lb('L07') - .05, [200.25, 1.5, 1.2], [200.1, 1.4, -1.0], 38, 'glide', .55, { creep: .1, drift: .03 });
  // antre: yüzleşme
  key(Lb('L08') - .1, [101.05, 1.5, 1.5], [101.25, 1.36, -1.0], 40, 'whip', .3, { creep: .1, drift: .03 });
  key(Lb('L09') - .1, [99.25, 1.64, .85], [99.0, 1.5, -1.75], 38, 'whip', .28, { creep: .1, drift: .03 });
  key(Lb('L10') - .1, [101.2, 1.5, 1.2], [101.0, 1.38, -1.0], 37, 'whip', .28, { creep: .1, drift: .03 });
  key(Lb('L11') - .1, [99.5, 1.62, 1.1], [99.2, 1.46, -1.75], 40, 'whip', .28, { creep: .1, drift: .03 });
  key(Lb('L12') - .05, [99.1, 1.64, .6], [99.0, 1.52, -1.75], 36, 'glide', .8, { creep: .1, drift: .02 });
  // merdiven (sert kesme): geniş -> alttan -> yakın
  key(Lb('L13') - .1, [299.9, 1.65, 2.2], [300.0, .95, -1.2], 46, 'cut', 0, { creep: .12, drift: .04 });
  key(Lb('L14') - .1, [299.9, 1.95, 2.0], [303.4, -.6, -1.7], 50, 'glide', 1.0, { creep: .1, drift: .03 });
  key(Lb('L15') - .15, [300.95, 1.6, 1.5], [300.42, 1.42, -.85], 38, 'whip', .3, { creep: .1, drift: .03 });
  key(Le('L15') + .3, [300.8, 1.56, 1.0], [300.4, 1.42, -.85], 36, 'glide', 1.6, { creep: .08, drift: .02 });
  return new CamPath(k, { fps: FPS });
}

// ---------------------------------------------------------------- nesneler
function shirtTex() {
  const c = document.createElement('canvas'); c.width = 420; c.height = 550; const g = c.getContext('2d');
  const ink = D('#2a1a2c'), base = D('#8a2a3a'), dark = D('#6a1c2c');
  g.lineJoin = 'round'; g.lineWidth = 9; g.strokeStyle = ink;
  const body = () => { g.beginPath(); g.moveTo(130, 40); g.lineTo(290, 40); g.lineTo(400, 120); g.lineTo(360, 210); g.lineTo(320, 180);
    g.lineTo(322, 530); g.lineTo(98, 530); g.lineTo(100, 180); g.lineTo(60, 210); g.lineTo(20, 120); g.closePath(); };
  body(); g.fillStyle = base; g.fill(); g.stroke();
  g.save(); body(); g.clip(); g.strokeStyle = dark; g.lineWidth = 6; for (const x of [150, 270]) { g.beginPath(); g.moveTo(x, 200); g.quadraticCurveTo(x + 20, 360, x - 10, 520); g.stroke(); } g.restore();
  g.strokeStyle = ink; g.lineWidth = 6; g.beginPath(); g.moveTo(210, 90); g.lineTo(210, 530); g.stroke();
  g.fillStyle = D('#f2e6d0'); for (let y = 150; y < 520; y += 70) { g.beginPath(); g.arc(225, y, 8, 0, 6.29); g.fill(); }
  // yaka
  g.fillStyle = D('#9a3446'); g.lineWidth = 8;
  for (const s of [-1, 1]) { g.beginPath(); g.moveTo(210, 92); g.lineTo(210 + s * 82, 34); g.lineTo(210 + s * 104, 64); g.lineTo(210 + s * 50, 140); g.closePath(); g.fill(); g.stroke(); }
  // uzun SARI saç teli: yakanın üstünde, kıvrılarak omza iner
  g.strokeStyle = D('#ffe06a'); g.lineWidth = 4.5; g.lineCap = 'round';
  g.beginPath(); g.moveTo(150, 52); g.bezierCurveTo(200, 30, 260, 70, 240, 110); g.bezierCurveTo(220, 150, 300, 160, 330, 140); g.bezierCurveTo(360, 120, 350, 200, 300, 230); g.stroke();
  g.strokeStyle = D('#fff6c0'); g.lineWidth = 1.6; g.stroke();
  // ruj izi yok (ima): yalnızca saç teli
  return texOf(c);
}
function makeShirt(scene) {
  const g = new THREE.Group(); scene.add(g);
  const geo = new THREE.PlaneGeometry(.42, .55, 10, 12);
  const p = geo.attributes.position; for (let i = 0; i < p.count; i++) p.setZ(i, Math.sin(p.getX(i) * 14) * .012 + Math.sin(p.getY(i) * 9) * .01);
  geo.computeVertexNormals();
  const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ map: shirtTex(), color: HDR(.92, .9, .95), transparent: true, alphaTest: .3, side: THREE.DoubleSide })); m.position.y = -.25; m.layers.set(1); g.add(m);
  return { g };
}
function makeBasket(scene) {
  const g = new THREE.Group(); g.position.copy(SEPET); scene.add(g);
  const c = document.createElement('canvas'); c.width = 256; c.height = 128; const x = c.getContext('2d');
  x.fillStyle = D('#c8a06a'); x.fillRect(0, 0, 256, 128); x.strokeStyle = D('#8a6438'); x.lineWidth = 4;
  for (let y = 8; y < 128; y += 16) { x.beginPath(); for (let i = 0; i <= 256; i += 16) x.lineTo(i, y + ((i / 16) % 2 ? 5 : -5)); x.stroke(); }
  const m = new THREE.MeshLambertMaterial({ map: texOf(c, [3, 2]), side: THREE.DoubleSide });
  const b = new THREE.Mesh(new THREE.CylinderGeometry(.24, .19, .48, 24, 1, true), m); b.position.y = .24; g.add(b);
  const bot = new THREE.Mesh(new THREE.CircleGeometry(.19, 24), flat('#8a6438')); bot.rotation.x = -Math.PI / 2; bot.position.y = .02; g.add(bot);
  const rim = new THREE.Mesh(new THREE.TorusGeometry(.24, .018, 6, 28), flat('#a8804a')); rim.rotation.x = Math.PI / 2; rim.position.y = .48; g.add(rim);
  for (const [c2, px, pz] of [['#e8e2f0', -.07, .05], ['#5a7ab8', .08, -.06], ['#f2d0a0', .02, .08]]) { const s = new THREE.Mesh(new THREE.SphereGeometry(.12, 12, 8), flat(c2)); s.scale.set(1, .5, 1); s.position.set(px, .38, pz); g.add(s); }
  shadows(g);
  return { g };
}
function makeBag(scene) {                     // çöp poşeti
  const g = new THREE.Group(); scene.add(g);
  const m = flat('#2c2a3c');
  const b = new THREE.Mesh(new THREE.SphereGeometry(.17, 16, 12), m); b.scale.set(1, 1.15, .9); b.position.y = -.24; g.add(b);
  const n = new THREE.Mesh(new THREE.CylinderGeometry(.02, .07, .1, 10), m); n.position.y = -.06; g.add(n);
  for (const s of [-1, 1]) { const e = new THREE.Mesh(new THREE.TorusGeometry(.035, .012, 6, 12), flat('#3a384c')); e.position.set(s * .03, 0, 0); g.add(e); }
  shadows(g);
  return { g };
}
function makeHandPhone(scene) {
  const g = new THREE.Group(); scene.add(g);
  const b = new THREE.Mesh(new THREE.BoxGeometry(.08, .16, .009), flat('#2a2632')); b.position.z = -.006; g.add(b);
  const c = document.createElement('canvas'); c.width = 360; c.height = 720; const tex = texOf(c);
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(.07, .14), new THREE.MeshBasicMaterial({ map: tex, color: HDR(1.1, 1.1, 1.1) })); scr.layers.set(1); g.add(scr);
  g.visible = false;
  return { g, c, tex };
}
// son aramalar: en üstteki "Bizim Takımdaki Kaan" satırı sola kayar, kırmızı "Sil" görünür, satır silinir
function calls(c, sw, gone) {
  const g = c.getContext('2d'), w = c.width, h = c.height;
  g.fillStyle = D('#f6f4fb'); g.fillRect(0, 0, w, h);
  g.fillStyle = D('#1a1630'); g.textAlign = 'left'; g.font = `700 ${w * .085}px Poppins, sans-serif`; g.fillText('Son aramalar', w * .07, h * .1);
  const rows = [['Bizim Takımdaki Kaan', 'Cmt 21:12', true], ['Annem', 'Cmt 18:40'], ['Berber Hakan', 'Cum 11:05'], ['Ayça ❤', 'Cum 09:30'], ['Ofis', 'Per 17:55']];
  let y = h * .15; const rh = h * .1;
  rows.forEach((r, i) => {
    if (i === 0 && gone >= 1) return;
    const yy = i === 0 ? y : y - (gone > 0 ? rh * gone : 0) + (i > 0 && gone < 1 ? 0 : 0);
    const off = i === 0 ? -sw * w * .3 : 0, top = i === 0 ? y : yy - (gone >= 1 ? rh : 0) * 0;
    const Y = i === 0 ? y : y + (i - (gone >= 1 ? 1 : gone)) * rh;
    if (i === 0) { g.fillStyle = D('#e04a4a'); g.fillRect(w * .7, Y, w * .3, rh); g.fillStyle = D('#ffffff'); g.font = `700 ${w * .06}px Poppins, sans-serif`; g.textAlign = 'center'; g.fillText('Sil', w * .85, Y + rh * .6); g.textAlign = 'left'; }
    g.fillStyle = D(i === 0 ? '#fff6d6' : '#f6f4fb'); g.fillRect(off, Y, w, rh);
    g.fillStyle = D(r[2] ? '#d8343a' : '#1a1630'); g.font = `700 ${w * .056}px Poppins, sans-serif`; g.fillText(r[0], off + w * .07, Y + rh * .48);
    g.fillStyle = D('#6a6680'); g.font = `500 ${w * .042}px Poppins, sans-serif`; g.fillText(r[1], off + w * .07, Y + rh * .8);
    g.fillStyle = D('#c8c4d4'); g.fillRect(off + w * .07, Y + rh - 2, w * .86, 2);
  });
}

// ---------------------------------------------------------------- kurulum
export async function setup(ctx) {
  C = ctx; WORDS = ctx.words; LINES = ctx.lines;
  DUR = +(LINES[LINES.length - 1].end + 1.2 + END).toFixed(2);
  const scene = ctx.scene; scene.background = new THREE.Color('#1c1830');
  try { await document.fonts.load('600 40px Poppins'); await document.fonts.load('800 40px Poppins'); } catch (e) { /* yedek */ }
  sets.sp = salonPencere(scene); { const fl = new THREE.PointLight('#fff0dc', 1.6, 0, 1.4); fl.position.set(200.7, 1.7, .6); sets.sp.L.add(fl); } sets.an = antre(scene); sets.md = merdiven(scene);
  cast.ayca = new Toon({ ...LOOK.ayca, cloth: '#d6c2e6', clothDark: '#a28ab8', buttons: false }, scene);     // sabah: leylak sabahlık
  cast.aycaAksam = new Toon(LOOK.ayca, scene);                                                                // akşam: yeşil hırka
  cast.nihat = new Toon({ ...LOOK.nihat }, scene);
  dyn.armS = new Arm3D(scene, cast.ayca); dyn.armP = new Arm3D(scene, cast.ayca); dyn.armM = new Arm3D(scene, cast.aycaAksam);
  dyn.shirt = makeShirt(scene); dyn.basket = makeBasket(scene); dyn.bag = makeBag(scene); dyn.ph = makeHandPhone(scene);
  // vanilya: gömlekten ve alt kattan yükselen ince, sıcak kıvrımlar (koku)
  dyn.van = new Smoke(scene, { color: '#ffd98a', maxPoints: 900, additive: true });
  for (let i = 0; i < 5; i++) dyn.van.wisps.push({ n: 34, size: .014, alpha: .3, seed: i, speed: .12,
    on: t => t > Lb('L03') - .2 && t < Lb('L05') - .1,
    fade: t => ramp(t, Lb('L03') - .2, Lb('L03') + .5),
    path: (u, t) => { const s = dyn.shirt.g.position; return [s.x - .12 + i * .06 + Math.sin(u * 7 + i + t) * .05, s.y - .15 + u * .55, s.z + .06 + Math.cos(u * 5 + i) * .04]; } });
  for (let i = 0; i < 7; i++) dyn.van.wisps.push({ n: 40, size: .03, alpha: .35, seed: i, speed: .07,
    on: t => t > Lb('L14') - .4,
    fade: t => ramp(t, Lb('L14') - .4, Lb('L14') + .8),
    path: (u, t) => [lerp(MD.altKapi.x - .2 + i * .06, AY_MD.x + .3, u) + Math.sin(u * 6 + i + t * .7) * .12, lerp(MD.altY + .1, 1.2, u) + Math.sin(u * 4 + i) * .08, lerp(-2.1, -1.2 + i * .05, u) + Math.cos(u * 5 + i) * .1] });
  dyn.cam = cameraPath();
  const cue = (t, type, extra = {}) => CUES.push({ t: +t.toFixed(3), type, ...extra });
  cue(0, 'sabah', { dur: Lb('L13') - .1 });
  cue(.2, 'kumas'); cue(Lb('L03') - .1, 'kumas'); cue(Lb('L03') + .2, 'kalp', { dur: 2.2 });
  cue(Lb('L05') - .05, 'whoosh'); cue(Wd('L05', 2) - .1, 'kumas'); cue(Wd('L05', 2) + .25, 'klik');
  cue(Lb('L06') - .05, 'vurgu');
  cue(Lb('L08') - .1, 'whoosh'); cue(Lb('L09') - .1, 'whoosh'); cue(Lb('L10') - .1, 'whoosh'); cue(Lb('L11') - .1, 'whoosh');
  cue(Lb('L13') - .1, 'gece', { dur: DUR - END - Lb('L13') }); cue(Lb('L13') - .1, 'kapi_kapan');
  cue(Lb('L14') - .1, 'kalp', { dur: 3.4 }); cue(Le('L15') + .3, 'vurgu'); cue(DUR - END, 'son', { dur: END });
}

// ---------------------------------------------------------------- her kare
const DAY = '#ece8f6', EVE = '#d8d0ec', WARM = '#ffb870';
const GRADE = { sp: [1, 1, 1.02], an: [1.03, 1.0, .95], md: [1.02, .97, 1.0] };
export function frame(t, ctx) {
  const { cam, env } = ctx;
  const cp = dyn.cam.apply(cam, t);
  const x = cam.position.x, where = x < 150 ? 'an' : x < 250 ? 'sp' : 'md';
  for (const k of ['sp', 'an', 'md']) { sets[k].g.visible = k === where; sets[k].L.visible = k === where; }
  for (const c of Object.values(cast)) c.hide();
  dyn.armS.hide(); dyn.armP.hide(); dyn.armM.hide();
  dyn.shirt.g.visible = dyn.basket.g.visible = where === 'sp'; dyn.bag.g.visible = where === 'md'; dyn.ph.g.visible = false;
  const tint = [.98, .98, 1];
  const A = id => Lb(id) - 2 / FPS;
  const talking = id => t > Lb(id) - .02 && t < Le(id) + .05;
  const bl = (seed, ...sw) => blinkAt(t, seed, sw, FPS);
  const f = p => cam.position.distanceTo(p);
  let look;

  if (where === 'sp') {
    const Aa = cast.ayca;
    Aa.show(); Aa.place(AY.x, 0, AY.z, cam, tint); Aa.castFrom(V(203.6, 3.6, -6.5));
    // gömlek: sepetten kalkar (L01), elde durur, buruna gider (L03-L04), yaka için kaldırılır (L06)
    const lift = ramp(t, .25, Wd('L01', 2) + .2), sniff = ramp(t, Lb('L03') - .15, Lb('L03') + .35) * (1 - ramp(t, Le('L04') - .1, Le('L04') + .4));
    const inBasket = V(SEPET.x + .02, .62, SEPET.z + .05);
    const P = inBasket.clone().lerp(GOMLEK_EL, lift).lerp(GOMLEK_BURUN, sniff);
    dyn.shirt.g.position.copy(P);
    dyn.shirt.g.rotation.set(lerp(-1.1, -.05, lift), lerp(.5, -.15, lift), lerp(.3, .04, lift) + Math.sin(t * 1.7) * .02);
    const phoneClose = t > Lb('L05') - .1 && t < Lb('L06') - .05;
    // ifade
    let ex = 'focused', lk = .5, lid = .2, brow = 0;
    if (t < Lb('L02')) { ex = 'neutral'; lk = .6; }
    else if (t < Lb('L03')) { ex = 'focused'; lk = .55; lid = .35; }
    else if (t < Lb('L04')) { ex = 'focused'; lk = .7; lid = .6; }
    else if (t < Lb('L05')) { ex = t < A('L04') + .4 ? 'surprised' : 'worried'; lk = .3; lid = 0; brow = .3; }
    else if (t < Lb('L07')) { ex = 'focused'; lk = .5; }
    else { ex = 'angry'; lk = .2; lid = .3; }
    Aa.draw({ expr: ex, look: lk, lookY: t < Lb('L02') ? -.25 : -.05, lid, brow, gazeX: lk * 1.1, blink: bl(3, A('L03'), A('L04'), A('L07')),
      noArmR: true, noArmL: phoneClose, armL: [14, 10], lit: 1, shade: DAY, rim: { color: '#dfe8ff', a: .5 } });
    dyn.armS.set(1, dyn.shirt.g.localToWorld(V(.09, -.02, .01)), { sag: .05, tint });
    if (phoneClose) {
      dyn.ph.g.visible = true;
      const up = ramp(t, Lb('L05') - .1, Lb('L05') + .3);
      dyn.ph.g.position.set(PH.x, lerp(PH.y - .1, PH.y, up), PH.z); dyn.ph.g.rotation.set(lerp(-.5, -.1, up), .1, 0);
      const sw = ramp(t, Wd('L05', 1) - .1, Wd('L05', 2) - .1), gone = ramp(t, Wd('L05', 2) + .25, Wd('L05', 2) + .6);
      const key = `${sw.toFixed(2)}|${gone.toFixed(2)}`;
      if (dyn.scKey !== key) { dyn.scKey = key; calls(dyn.ph.c, sw, gone); dyn.ph.tex.needsUpdate = true; }
      dyn.armP.set(-1, dyn.ph.g.localToWorld(V(-.055, -.11, .01)), { sag: .04, tint: [.9, .9, 1] });
    }
    if (t < Wd('L01', 2) - .1) look = { focus: f(dyn.shirt.g.position), coc: 8, range: .35 };
    else if (phoneClose) look = { focus: f(dyn.ph.g.position), coc: 10, range: .12 };
    else if (t > Lb('L06') - .05 && t < Lb('L07') - .05) look = { focus: f(V(200.44, 1.14, -.7)), coc: 10, range: .12 };
    else look = { focus: f(V(AY.x, 1.4, AY.z)), coc: 6, range: .8 };
    Object.assign(look, { sat: 1.08, lift: [.085, .085, .13], bloom: .8, vignette: .28, contrast: 1.07 });
  } else if (where === 'an') {
    const Nn = cast.nihat, Aa = cast.ayca;
    Nn.show(); Nn.place(NIHAT.x, 0, NIHAT.z, cam, tint); Nn.castFrom(V(107, 3.2, .6));
    const fixing = t < A('L09') + .3;
    const nEx = t < A('L09') ? 'focused' : t < A('L11') ? 'smug' : t < A('L12') ? 'smile' : 'smug';
    Nn.draw({ expr: nEx, look: fixing ? -.55 : .65, lookY: fixing ? -.2 : 0, blink: bl(7, A('L09'), A('L11'), A('L12')),
      mouth: talking('L09') || talking('L11') ? flap(env, t) : 0,
      armL: fixing ? [150 + Math.sin(t * 9) * 8, 70] : t > A('L11') && t < Le('L11') ? [55, 30] : [16, 20],
      armR: fixing ? [140, 80] : t > A('L11') && t < Le('L11') ? [55, 30] : [14, 8], lean: t > A('L11') && t < Le('L11') ? -2 : 0,
      lit: 1, shade: DAY, rim: { color: '#ffd59a', a: .4 } });
    Aa.show(); Aa.place(AYCA_AN.x, 0, AYCA_AN.z, cam, tint); Aa.castFrom(V(107, 3.2, .6));
    const show = t > A('L08') && t < Le('L08') + .4;
    Aa.draw({ expr: t < A('L10') ? 'focused' : t < Le('L10') + .2 ? 'angry' : 'focused', look: -.8, lid: .2, brow: t > A('L10') && t < Le('L10') ? .2 : 0,
      blink: bl(8, A('L08'), A('L10')), mouth: talking('L08') || talking('L10') ? flap(env, t) : 0,
      armR: show ? [75, 40] : [40, 70], propR: 'shirt', shirtColor: '#8a2a3a', armL: [18, 20], lit: 1, shade: DAY, rim: { color: '#ffd59a', a: .5 } });
    const onN = (t > Lb('L09') - .1 && t < Lb('L10') - .1) || t > Lb('L11') - .1;
    look = { focus: f(onN ? V(NIHAT.x, 1.5, NIHAT.z) : V(AYCA_AN.x, 1.4, AYCA_AN.z)), coc: 6, range: .8, sat: 1.15, lift: [.09, .085, .12], bloom: .8, vignette: .24, contrast: 1.06 };
  } else {
    const Aa = cast.aycaAksam;
    const walk = ramp(t, Lb('L13') - .1, Wd('L13', 4));
    const ax = lerp(AY_MD0.x, AY_MD.x, walk), az = lerp(AY_MD0.z, AY_MD.z, walk);
    Aa.show(); Aa.place(ax, 0, az, cam, tint); Aa.castFrom(V(300.3, 2.0, -2.0));
    const down = t > Lb('L14') - .2;
    Aa.draw({ expr: t < A('L14') ? 'neutral' : t < A('L15') ? 'worried' : 'focused', look: down ? .75 : .5, lookY: down && t < A('L15') ? -.45 : -.05,
      lid: t > A('L15') ? .3 : 0, brow: down ? .25 : 0, gazeX: .8, blink: bl(9, A('L14'), A('L15')),
      bob: walk > 0 && walk < 1 ? Math.abs(Math.sin(t * 9)) * 7 : 0, noArmL: true, armR: [12, 8],
      lit: 1, shade: EVE, rim: { color: WARM, a: .45 } });
    const hand = Aa.toWorld(-(150), 600);
    dyn.bag.g.position.set(hand.x, hand.y, hand.z + .04); dyn.bag.g.rotation.y = Math.sin(t * 2) * .1;
    dyn.armM.set(-1, dyn.bag.g.localToWorld(V(0, .01, 0)), { sag: .03, tint });
    sets.md.leakL.intensity = 1.6 + Math.sin(t * 3) * .15;
    if (t < Lb('L14') - .1) look = { focus: f(V(ax, 1.3, az)), coc: 4, range: 1.6 };
    else look = { focus: f(V(ax, 1.4, az)), coc: 7, range: .7 };
    Object.assign(look, { sat: 1.1, lift: [.08, .07, .12], bloom: .95, vignette: .32, contrast: 1.07 });
  }
  dyn.van.update(t);
  look.tint = GRADE[where];
  look.blur = cp.moving > .15 ? 16 : 0;
  look.captions = t < DUR - END;
  return look;
}

// ---------------------------------------------------------------- yazı katmanı: dizi adı (açılış), son kart
export function overlay(g, t, ctx) {
  const W = ctx.W, H = ctx.H, k = W / 1080;
  const a = Math.min(1, t / .25) * (1 - ramp(t, 2.8, 3.3));
  if (a > 0) {
    g.save(); g.globalAlpha = a; g.textAlign = 'center';
    g.font = `800 ${46 * k}px Poppins, sans-serif`; g.fillStyle = '#ffd27a'; g.shadowColor = 'rgba(10,6,20,.7)'; g.shadowBlur = 18 * k;
    g.fillText('ÇAPKIN NİHAT', W / 2, H * .085);
    g.font = `600 ${28 * k}px Poppins, sans-serif`; g.fillStyle = '#ffffff'; g.fillText(`${BOLUM.no}. BÖLÜM · ${BOLUM.ad.toLocaleUpperCase('tr-TR')}`, W / 2, H * .085 + 44 * k);
    g.restore();
  }
  const e = ramp(t, DUR - END, DUR - END + .5);
  if (e > 0) {
    g.save();
    g.fillStyle = `rgba(16,12,30,${.82 * e})`; g.fillRect(0, 0, W, H);
    g.globalAlpha = e; g.textAlign = 'center'; g.shadowColor = 'rgba(0,0,0,.6)'; g.shadowBlur = 20 * k;
    g.font = `800 ${74 * k}px Poppins, sans-serif`; g.fillStyle = '#ffd27a'; g.fillText('ÇAPKIN NİHAT', W / 2, H * .36);
    g.font = `600 ${40 * k}px Poppins, sans-serif`; g.fillStyle = '#ffffff'; g.fillText(BOLUM.sonraki, W / 2, H * .36 + 70 * k);
    const q = ramp(t, DUR - END + .5, DUR - END + 1.0);
    g.globalAlpha = q; g.font = `800 ${54 * k}px Poppins, sans-serif`; g.fillStyle = '#ffffff';
    const words = BOLUM.soru.split(' '), mid = Math.ceil(words.length / 2);
    g.fillText(words.slice(0, mid).join(' '), W / 2, H * .58); g.fillText(words.slice(mid).join(' '), W / 2, H * .58 + 66 * k);
    g.font = `700 ${34 * k}px Poppins, sans-serif`; g.fillStyle = '#ffd27a'; g.fillText('YORUMLARA YAZ ↓', W / 2, H * .58 + 150 * k);
    g.restore();
  }
}
