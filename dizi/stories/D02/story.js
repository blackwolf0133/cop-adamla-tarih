// Çapkın Nihat · Bölüm 2 · "Halı Saha Çantası"
// Set: ANTRE (x≈100), AKŞAM. Banyo kapısı = sağ duvardaki boşluk (sıcak ışık oradan gelir, tek ana ışık).
// Her şey satır saatlerine bağlı: Lb('L06') = satırın başı, Wd('L06', 3) = o satırın 4. kelimesinin başı (voice/words.json).
// İç ses satırlarında ağız oynamaz; yalnızca yüksek sesle konuşanın ağzı oynar (Nihat L03). Kaan (L11) telefondan duyulur.
import * as THREE from 'three';
import { Toon, Arm3D, flap, blinkAt } from '/engine/src/toon.js';
import { CamPath, smoother } from '/engine/src/camera.js';
import { flat } from '/engine/src/paint.js';
import { LOOK as KADRO } from '/lib/kadro.js';
import { antre, AN, V, HDR, texOf, shadows } from '/lib/ev.js';
import { D } from '/engine/src/paint.js';

export const NAME = 'capkin-nihat-02';
export const FPS = 30;
export let DUR = 50;
export const CUES = [];
export const LOOK = KADRO;
export const BOLUM = { no: 2, ad: 'Halı Saha Çantası', soru: 'Sence telefonu açan kadın kim?', sonraki: '3. BÖLÜM YARIN 20.00' };

const S = smoother;
const ramp = (t, a, b) => S((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
let C, LINES, WORDS, cast = {}, sets = {}, dyn = {};
const Lb = id => LINES.find(l => l.id === id).start;
const Le = id => LINES.find(l => l.id === id).end;
const Wd = (id, n) => WORDS.filter(w => w.line === id)[n].start;
const END = 3.2;

// sahne yerleşimi
const BAG = V(98.95, .89, -2.12);                 // ayakkabılığın üstünde spor çanta
const NIHAT0 = V(99.82, 0, -1.78), BANYO = V(102.45, 0, -.25);
const AYCA_KAPI = V(101.25, 0, -.65), AYCA_CANTA = V(99.78, 0, -1.62), AYCA_ASKI = V(98.3, 0, -.45);
const CEKET = V(97.52, 1.22, -.85);
const POCKET = V(97.62, 1.08, -.78);              // telefonun cepten görünen ucu
const PH = V(98.62, 1.2, .05);                    // elde telefon (yakın plan)

// ---------------------------------------------------------------- kamera
function cameraPath() {
  const k = [];
  const key = (t, pos, look, fov, move = 'glide', dur = .6, extra = {}) => k.push({ t, pos, look, fov, move, dur, ...extra });
  // kanca: fermuar (yakın) -> Nihat çantayla -> kapıda Ayça
  key(0, [99.25, 1.42, -1.25], [98.98, 1.08, -2.1], 32, 'cut', 0, { creep: .3, drift: .03 });
  key(Wd('L01', 2) - .1, [99.9, 1.55, .8], [99.65, 1.32, -1.85], 40, 'glide', .7, { creep: .12, drift: .04 });
  key(Lb('L02') - .05, [100.95, 1.5, 1.55], [101.25, 1.32, -.65], 38, 'whip', .3, { creep: .12, drift: .04 });
  // Nihat konuşur
  key(Lb('L03') - .1, [99.95, 1.62, .7], [99.8, 1.45, -1.78], 38, 'whip', .3, { creep: .1, drift: .04 });
  // Nihat banyoya gider, Ayça çantaya
  key(Lb('L04') - .05, [100.2, 1.55, 1.9], [100.6, 1.15, -1.2], 50, 'glide', .7, { creep: .12, drift: .03 });
  key(Wd('L04', 4) - .1, [100.05, 1.5, .55], [99.4, 1.2, -1.85], 40, 'glide', .8, { creep: .12, drift: .03 });
  // krampon: yakın (sert kesme)
  key(Lb('L05') - .05, [100.1, 1.3, .05], [99.45, 1.1, -1.3], 34, 'cut', 0, { creep: .25, drift: .02 });
  // Ayça'nın yüzü, elinde krampon
  key(Lb('L06') - .05, [100.0, 1.52, .55], [99.72, 1.36, -1.62], 38, 'glide', .6, { creep: .1, drift: .03 });
  // askıdaki ceket, cepteki telefon
  key(Lb('L07') - .05, [99.15, 1.42, 1.25], [97.95, 1.2, -.7], 40, 'whip', .32, { creep: .12, drift: .03 });
  // elde telefon: şifre, rehber, arama
  key(Lb('L08') - .05, [PH.x + .1, PH.y + .1, PH.z + .62], [PH.x, PH.y, PH.z], 26, 'glide', .55, { creep: .12, drift: .01 });
  key(Lb('L09') - .05, [PH.x + .06, PH.y + .08, PH.z + .55], [PH.x, PH.y + .005, PH.z], 24, 'glide', .5, { creep: .15, drift: .01 });
  // Kaan açar: Ayça'nın yüzü
  key(Lb('L11') - .1, [98.6, 1.5, 1.75], [98.3, 1.36, -.45], 38, 'whip', .26, { creep: .12, drift: .03 });
  // su sesi kesilir: Ayça banyoya döner
  key(Lb('L13') - .05, [99.1, 1.5, 1.5], [98.4, 1.38, -.45], 40, 'glide', .7, { creep: .1, drift: .04 });
  // son: Ayça'ya yavaşça yaklaş
  key(Lb('L14') - .15, [98.75, 1.5, 1.95], [98.3, 1.38, -.45], 40, 'whip', .3, { creep: .1, drift: .03 });
  key(Le('L14') + .3, [98.55, 1.46, 1.45], [98.3, 1.4, -.45], 37, 'glide', 1.6, { creep: .08, drift: .02 });
  return new CamPath(k, { fps: FPS });
}

// ---------------------------------------------------------------- nesneler
function makeBag(scene) {
  const g = new THREE.Group(); g.position.copy(BAG); scene.add(g);
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(.13, .28, 8, 20), flat('#3d5cb0')); body.rotation.z = Math.PI / 2; body.scale.set(1, 1, .95); body.position.y = .13; g.add(body);
  for (const x of [-.12, .12]) { const r = new THREE.Mesh(new THREE.CylinderGeometry(.134, .134, .035, 24), flat('#f2c94a')); r.rotation.z = Math.PI / 2; r.position.set(x, .13, 0); g.add(r); }
  const hm = flat('#1f2a4a');
  for (const z of [-.06, .06]) { const h = new THREE.Mesh(new THREE.TorusGeometry(.08, .011, 8, 20, Math.PI), hm); h.position.set(0, .25, z); g.add(h); }
  const zip = new THREE.Mesh(new THREE.BoxGeometry(.5, .008, .012), flat('#c9c4d8')); zip.position.set(0, .262, 0); g.add(zip);
  const pull = new THREE.Mesh(new THREE.BoxGeometry(.018, .012, .04), flat('#e8c24a')); pull.position.set(0, .268, .02); g.add(pull);
  const mouth = new THREE.Mesh(new THREE.PlaneGeometry(.42, .1), new THREE.MeshLambertMaterial({ color: '#141022' })); mouth.rotation.x = -Math.PI / 2; mouth.position.set(0, .266, 0); mouth.visible = false; g.add(mouth);
  const flapM = new THREE.Group(); flapM.position.set(0, .262, -.05); g.add(flapM);
  const fl = new THREE.Mesh(new THREE.BoxGeometry(.42, .01, .1), flat('#3d5cb0')); fl.position.set(0, 0, .05); flapM.add(fl);
  shadows(g);
  return { g, pull, mouth, flapM };
}
// krampon: turuncu saya, koyu taban, çiviler, bağcıklar, siyah şerit + etiketi
function tagTex() {
  const c = document.createElement('canvas'); c.width = 200; c.height = 300; const g = c.getContext('2d');
  g.fillStyle = D('#fbf6ea'); g.beginPath(); g.roundRect(4, 4, 192, 292, 18); g.fill();
  g.strokeStyle = D('#2a1a2c'); g.lineWidth = 6; g.stroke();
  g.fillStyle = D('#2a1a2c'); g.beginPath(); g.arc(100, 36, 12, 0, 6.29); g.fill();
  g.fillStyle = D('#d8343a'); g.font = '800 54px Poppins, sans-serif'; g.textAlign = 'center'; g.fillText('YENİ', 100, 112);
  g.fillStyle = D('#2a1a2c'); g.font = '700 40px Poppins, sans-serif'; g.fillText('1.899 ₺', 100, 170);
  for (let i = 0; i < 22; i++) g.fillRect(36 + i * 6, 200, (i % 3 ? 3 : 5), 56);
  g.font = '600 18px Poppins, sans-serif'; g.fillText('NO 43', 100, 282);
  return texOf(c);
}
function makeBoot(scene) {
  const g = new THREE.Group(); scene.add(g);
  const up = new THREE.Mesh(new THREE.CapsuleGeometry(.05, .17, 8, 16), flat('#f0702e')); up.rotation.z = Math.PI / 2; up.scale.set(.85, 1, 1); up.position.y = .055; g.add(up);
  const heel = new THREE.Mesh(new THREE.BoxGeometry(.07, .07, .09), flat('#ff7a2a')); heel.position.set(-.1, .075, 0); g.add(heel);
  const sole = new THREE.Mesh(new THREE.BoxGeometry(.28, .016, .088), flat('#2a2632')); sole.position.y = .006; g.add(sole);
  for (const x of [-.11, -.06, .02, .07, .11]) for (const z of [-.025, .025]) { const s = new THREE.Mesh(new THREE.CylinderGeometry(.008, .006, .018, 8), flat('#e8e4ee')); s.position.set(x, -.01, z); g.add(s); }
  for (const z of [-.052, .052]) { const st = new THREE.Mesh(new THREE.BoxGeometry(.16, .022, .004), flat('#1a1626')); st.position.set(-.01, .06, z); st.rotation.z = .25; g.add(st); }
  for (const x of [-.02, .01, .04]) { const l = new THREE.Mesh(new THREE.BoxGeometry(.008, .006, .06), flat('#ffffff')); l.position.set(x, .105, 0); g.add(l); }
  const str = new THREE.Mesh(new THREE.CylinderGeometry(.0015, .0015, .07, 4), flat('#d8343a')); str.position.set(-.02, .13, .02); g.add(str);
  const tag = new THREE.Mesh(new THREE.PlaneGeometry(.06, .09), new THREE.MeshLambertMaterial({ map: tagTex(), side: THREE.DoubleSide })); tag.position.set(-.02, .12, .055); tag.rotation.set(0, 0, .15); g.add(tag);
  shadows(g); tag.castShadow = false;
  g.visible = false;
  return { g, tag };
}
function makeJacket(scene) {
  const g = new THREE.Group(); g.position.copy(CEKET); scene.add(g);
  const m = flat('#4a5274'), md = flat('#3a4060');
  const body = new THREE.Mesh(new THREE.CapsuleGeometry(.2, .45, 6, 14), m); body.scale.set(.32, 1, 1); g.add(body);
  for (const s of [-1, 1]) { const sl = new THREE.Mesh(new THREE.CapsuleGeometry(.05, .5, 6, 10), md); sl.position.set(.02, -.05, s * .2); sl.rotation.x = s * .08; g.add(sl); }
  const col = new THREE.Mesh(new THREE.TorusGeometry(.1, .025, 6, 14, Math.PI), flat('#41475f')); col.position.set(.02, .36, 0); col.rotation.y = Math.PI / 2; g.add(col);
  const hook = new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, .1, 8), flat('#c9a64a')); hook.rotation.z = Math.PI / 2; hook.position.set(-.04, .46, 0); g.add(hook);
  const pocket = new THREE.Mesh(new THREE.BoxGeometry(.012, .1, .16), md); pocket.position.set(.065, -.17, .07); g.add(pocket);
  // cepten görünen telefon: ekranı sızdırır
  const ph = new THREE.Group(); ph.position.copy(POCKET); scene.add(ph);
  const pb = new THREE.Mesh(new THREE.BoxGeometry(.012, .15, .075), flat('#2a2632')); ph.add(pb);
  const lit = new THREE.Mesh(new THREE.PlaneGeometry(.065, .06), new THREE.MeshBasicMaterial({ color: HDR(.6, .8, 1.3), transparent: true, opacity: 0 })); lit.rotation.y = Math.PI / 2; lit.position.set(.007, .04, 0); lit.layers.set(1); ph.add(lit);
  shadows(g);
  return { g, ph, lit };
}
// elde telefon (yakın plan): kilit/şifre -> rehber -> aranıyor -> görüşme
function makeHandPhone(scene) {
  const g = new THREE.Group(); scene.add(g);
  const b = new THREE.Mesh(new THREE.BoxGeometry(.08, .16, .009), flat('#2a2632')); b.position.z = -.006; g.add(b);
  const c = document.createElement('canvas'); c.width = 360; c.height = 720; const tex = texOf(c);
  const scr = new THREE.Mesh(new THREE.PlaneGeometry(.07, .14), new THREE.MeshBasicMaterial({ map: tex, color: HDR(1.1, 1.1, 1.1) })); scr.layers.set(1); g.add(scr);
  const light = new THREE.PointLight('#bcd6ff', 0, 0, 1.6); light.position.set(0, 0, .12); g.add(light);
  g.visible = false;
  return { g, c, tex, scr, light };
}
function screen(c, { mode = 'kilit', dots = 0, hl = 0, ring = 0, sure = '00:01' }) {
  const g = c.getContext('2d'), w = c.width, h = c.height;
  let gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, D('#2a3a8a')); gr.addColorStop(1, D('#6a3a8a')); g.fillStyle = gr; g.fillRect(0, 0, w, h);
  g.textAlign = 'center'; g.fillStyle = D('#ffffff');
  if (mode === 'kilit') {
    g.font = `600 ${w * .07}px Poppins, sans-serif`; g.fillText('Şifreyi girin', w / 2, h * .2);
    for (let i = 0; i < 6; i++) { g.beginPath(); g.arc(w * (.22 + i * .112), h * .28, w * .03, 0, 6.29); g.strokeStyle = D('#ffffff'); g.lineWidth = 4; g.stroke(); if (i < dots) g.fill(); }
    const keys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '', '0', ''];
    g.font = `500 ${w * .085}px Poppins, sans-serif`;
    keys.forEach((k, i) => { if (!k) return; const x = w * (.25 + (i % 3) * .25), y = h * (.42 + Math.floor(i / 3) * .13);
      g.fillStyle = D('#ffffff', .16); g.beginPath(); g.arc(x, y, w * .095, 0, 6.29); g.fill(); g.fillStyle = D('#ffffff'); g.fillText(k, x, y + w * .03); });
  } else if (mode === 'rehber') {
    g.fillStyle = D('#f6f4fb'); g.fillRect(0, 0, w, h);
    g.fillStyle = D('#1a1630'); g.textAlign = 'left'; g.font = `700 ${w * .09}px Poppins, sans-serif`; g.fillText('Kişiler', w * .07, h * .1);
    g.fillStyle = D('#e4e0ee'); g.beginPath(); g.roundRect(w * .06, h * .13, w * .88, h * .06, w * .04); g.fill();
    g.fillStyle = D('#1a1630'); g.font = `500 ${w * .06}px Poppins, sans-serif`; g.fillText('🔍 Kaan', w * .1, h * .172);
    g.fillStyle = D('#6a6680'); g.font = `600 ${w * .045}px Poppins, sans-serif`; g.fillText('1 SONUÇ', w * .07, h * .25);
    const y = h * .27;
    g.fillStyle = D('#ffe9a6', hl); g.fillRect(0, y, w, h * .1);
    g.fillStyle = D('#3fbf6a'); g.beginPath(); g.arc(w * .14, y + h * .05, w * .07, 0, 6.29); g.fill();
    g.fillStyle = D('#ffffff'); g.textAlign = 'center'; g.font = `700 ${w * .07}px Poppins, sans-serif`; g.fillText('K', w * .14, y + h * .065);
    g.textAlign = 'left'; g.fillStyle = D('#1a1630'); g.font = `700 ${w * .056}px Poppins, sans-serif`; g.fillText('Bizim Takımdaki Kaan', w * .25, y + h * .06);
    g.fillStyle = D('#c8c4d4'); g.fillRect(w * .07, y + h * .1, w * .86, 2);
  } else {
    // arama ekranı
    g.font = `500 ${w * .055}px Poppins, sans-serif`; g.fillStyle = D('#e8e8ff', .85); g.fillText(mode === 'arama' ? 'aranıyor…' : sure, w / 2, h * .17);
    g.fillStyle = D('#ffffff'); g.font = `700 ${w * .075}px Poppins, sans-serif`; g.fillText('Bizim Takımdaki', w / 2, h * .26); g.fillText('Kaan', w / 2, h * .32);
    for (let i = 0; i < 2; i++) { const r = (ring + i * .5) % 1; g.strokeStyle = D('#ffffff', (1 - r) * .5); g.lineWidth = 5; g.beginPath(); g.arc(w / 2, h * .48, w * (.16 + r * .2), 0, 6.29); g.stroke(); }
    g.fillStyle = D('#3fbf6a'); g.beginPath(); g.arc(w / 2, h * .48, w * .16, 0, 6.29); g.fill();
    g.fillStyle = D('#ffffff'); g.font = `800 ${w * .14}px Poppins, sans-serif`; g.fillText('K', w / 2, h * .505);
    g.fillStyle = D('#e04a4a'); g.beginPath(); g.arc(w / 2, h * .84, w * .1, 0, 6.29); g.fill();
    g.strokeStyle = D('#ffffff'); g.lineWidth = 9; g.lineCap = 'round'; g.beginPath(); g.arc(w / 2, h * .86, w * .05, Math.PI * 1.15, Math.PI * 1.85); g.stroke();
  }
}

// ---------------------------------------------------------------- kurulum
export async function setup(ctx) {
  C = ctx; WORDS = ctx.words; LINES = ctx.lines;
  DUR = +(LINES[LINES.length - 1].end + 1.2 + END).toFixed(2);
  const scene = ctx.scene; scene.background = new THREE.Color('#1c1830');
  try { await document.fonts.load('600 40px Poppins'); await document.fonts.load('800 40px Poppins'); } catch (e) { /* yedek */ }
  sets.an = antre(scene);
  // AKŞAM: güneş yerine banyonun sıcak ışığı (aynı boşluktan), soğuk ve kısık dolgu
  sets.an.sun.color.set('#ffb070'); sets.an.sun.intensity = 3.4; sets.an.sun.target.position.set(100.2, .2, -1.3);
  sets.an.L.traverse(o => { if (o.isHemisphereLight) { o.color.set('#6c78c0'); o.groundColor.set('#4a3a4a'); o.intensity = .95; } });
  const lamp = new THREE.PointLight('#ffc78a', 1.1, 0, 1.4); lamp.position.set(99.2, 2.3, -.8); sets.an.L.add(lamp);   // tavan apliği (zayıf sıcak dolgu)
  cast.ayca = new Toon(LOOK.ayca, scene); cast.nihat = new Toon({ ...LOOK.nihat }, scene);
  dyn.armA = new Arm3D(scene, cast.ayca); dyn.armN = new Arm3D(scene, cast.nihat);
  dyn.bag = makeBag(scene); dyn.boot = makeBoot(scene); dyn.jk = makeJacket(scene); dyn.ph = makeHandPhone(scene);
  dyn.cam = cameraPath();
  const cue = (t, type, extra = {}) => CUES.push({ t: +t.toFixed(3), type, ...extra });
  cue(0, 'gece', { dur: DUR - END });
  cue(.15, 'kumas'); cue(Lb('L02') - .05, 'whoosh'); cue(Lb('L03') - .1, 'whoosh');
  cue(Wd('L04', 4) - .1, 'kumas'); cue(Lb('L05') - .05, 'klik'); cue(Lb('L07') - .05, 'whoosh'); cue(Lb('L07') + .5, 'titresim', { dur: .7 });
  cue(Wd('L08', 0) - .3, 'klik'); cue(Wd('L08', 1) - .2, 'klik'); cue(Wd('L08', 2) - .1, 'klik'); cue(Lb('L09') - .1, 'bildirim');
  cue(Wd('L10', 3), 'titresim', { dur: .9 }); cue(Wd('L10', 6), 'titresim', { dur: .9 });
  cue(Lb('L11') - .15, 'klik'); cue(Lb('L11') - .1, 'kalp', { dur: Lb('L13') - Lb('L11') + .6 });
  cue(Lb('L13') - .05, 'kapi_kapan'); cue(Wd('L13', 4), 'klik'); cue(Lb('L14') - .15, 'whoosh'); cue(Le('L14') + .3, 'vurgu'); cue(DUR - END, 'son', { dur: END });
}

// ---------------------------------------------------------------- her kare
const EVE = '#d8d0ec', WARM = '#ffb870', COOL = '#a9c4ff';
const GRADE = [1.02, .97, 1.02];
export function frame(t, ctx) {
  const { cam, env } = ctx;
  const cp = dyn.cam.apply(cam, t);
  const tint = [.98, .98, 1];
  const A = id => Lb(id) - 2 / FPS;
  const talking = id => t > Lb(id) - .02 && t < Le(id) + .05;
  const bl = (seed, ...sw) => blinkAt(t, seed, sw, FPS);
  const f = p => cam.position.distanceTo(p);
  dyn.armA.hide(); dyn.armN.hide();
  const N = cast.nihat, Aa = cast.ayca;
  const LIGHT = V(107, 3.2, .6);

  // ---------------- çanta: Nihat kapatır (L01), Ayça açar (L04 sonu)
  const zipClose = ramp(t, .2, Wd('L01', 2)), zipOpen = ramp(t, Wd('L04', 4) + .2, Le('L04') + .1);
  const pullX = lerp(lerp(.2, -.2, zipClose), .2, zipOpen);
  dyn.bag.pull.position.x = pullX;
  const open = ramp(t, Le('L04') - .1, Le('L04') + .35);
  dyn.bag.mouth.visible = open > .01; dyn.bag.flapM.rotation.x = -open * 1.9;
  const pullW = dyn.bag.g.localToWorld(V(pullX, .272, .04));

  // ---------------- Nihat: çantanın başında -> konuşur -> banyoya yürür
  const walkN = ramp(t, Le('L03') + .1, Lb('L04') + 1.3);
  const nx = lerp(NIHAT0.x, BANYO.x, walkN), nz = lerp(NIHAT0.z, BANYO.z, walkN);
  if (walkN < .98) {
    N.show(); N.place(nx, 0, nz, cam, tint);
    const zipping = t < Wd('L01', 2) + .3;
    const bob = walkN > 0 && walkN < 1 ? Math.abs(Math.sin(t * 9)) * 8 : 0;
    N.draw({ expr: t < Lb('L02') ? 'focused' : t < A('L03') ? 'smug' : 'smile', look: zipping ? -.7 : t < Le('L03') ? .7 : .9, lookY: zipping ? -.3 : 0,
      blink: bl(5, A('L03')), mouth: talking('L03') ? flap(env, t) : 0, noArmL: zipping, armL: [16, 20], armR: t > A('L03') && t < Le('L03') ? [60, 50] : [12, 10],
      bob, lean: walkN > 0 ? 3 : 0, lit: 1, shade: EVE, rim: { color: WARM, a: .45 } });
    N.castFrom(LIGHT);
    if (zipping) dyn.armN.set(-1, pullW, { sag: .05, tint });
  } else N.hide();

  // ---------------- Ayça: kapıda -> çantaya -> askıya
  const walkA = ramp(t, Lb('L04') + .1, Wd('L04', 4) + .05);
  let ax, az;
  if (t < Lb('L07') - .2) { ax = lerp(AYCA_KAPI.x, AYCA_CANTA.x, walkA); az = lerp(AYCA_KAPI.z, AYCA_CANTA.z, walkA); }
  else { ax = AYCA_ASKI.x; az = AYCA_ASKI.z; }
  Aa.show(); Aa.place(ax, 0, az, cam, tint); Aa.castFrom(LIGHT);
  const atBag = t > Wd('L04', 4) - .1 && t < Lb('L07') - .2;
  const holdBoot = t > Lb('L05') - .1 && t < Lb('L07') - .2;
  const atJacket = t > Lb('L07') + .3 && t < Lb('L08') - .1;
  const phoneClose = t > Lb('L08') - .1 && t < Lb('L11') - .1;
  const phoneHeld = t > Lb('L11') - .1;
  // krampon yolu: çantadan yukarı, Ayça'nın önüne
  const liftK = ramp(t, Lb('L05') - .1, Lb('L05') + .5);
  const bootP = V(lerp(98.98, 99.42, liftK), lerp(1.02, 1.16, liftK), lerp(-2.1, -1.32, liftK));
  dyn.boot.g.visible = holdBoot || (open > .5 && t < Lb('L07') - .2);
  if (!holdBoot) { dyn.boot.g.position.set(98.98, 1.04, -2.1); dyn.boot.g.rotation.set(0, .3, -.15); }
  else { dyn.boot.g.position.copy(bootP); dyn.boot.g.rotation.set(lerp(0, .15, liftK), lerp(.3, .65, liftK), lerp(-.15, .12, liftK) + Math.sin(t * 2) * .03); }
  dyn.boot.tag.rotation.z = .15 + Math.sin(t * 3.1) * .12;
  // ifade
  let ex = 'neutral', lk = -.6, lid = .2, brow = 0;
  if (t < Lb('L04')) { ex = t < A('L03') ? 'focused' : 'neutral'; lk = -.8; lid = .25; }
  else if (t < Lb('L05')) { ex = 'focused'; lk = -.6; lid = .3; }
  else if (t < Lb('L07')) { ex = t < A('L06') ? 'worried' : 'focused'; lk = -.5; lid = t < A('L06') ? 0 : .3; brow = .2; }
  else if (t < Lb('L11')) { ex = 'focused'; lk = -.6; }
  else if (t < Lb('L13')) { ex = t < A('L12') + .5 ? 'surprised' : 'worried'; lk = .1; lid = 0; brow = .4; }
  else { ex = t < A('L14') ? 'worried' : 'focused'; lk = t < A('L14') ? .95 : .5; lid = t < A('L14') ? 0 : .25; brow = .2; }
  const armR = phoneHeld ? [38, 100] : atBag && !holdBoot ? [20, 30] : [12, 8];
  Aa.draw({ expr: ex, look: lk, lookY: t > Lb('L05') && t < Lb('L07') ? -.15 : -.05, lid, brow, gazeX: lk * 1.1,
    blink: bl(3, A('L05'), A('L06'), A('L11'), A('L12'), A('L14')), mouth: 0,
    noArmL: (atBag && t > Wd('L04', 4) + .2) || holdBoot, noArmR: atJacket || phoneClose,
    armL: [14, 10], armR, propR: phoneHeld ? 'phone' : undefined, screen: phoneHeld,
    sweat: t > A('L12') && t < Lb('L14') ? 1 : 0, lit: 1, shade: EVE, rim: { color: phoneHeld && t < Lb('L13') ? COOL : WARM, a: .45 } });
  if (holdBoot) dyn.armA.set(-1, dyn.boot.g.localToWorld(V(-.1, .06, 0)), { sag: .05, tint });
  else if (atBag && t > Wd('L04', 4) + .2) dyn.armA.set(-1, pullW, { sag: .05, tint });

  // ---------------- ceketteki telefon: titrer, Ayça alır
  const buzz = t > Lb('L07') + .5 && t < Lb('L07') + 1.2;
  const take = ramp(t, Lb('L07') + 1.0, Lb('L08') - .1);
  dyn.jk.lit.material.opacity = buzz ? .9 : .25;
  dyn.jk.ph.position.set(POCKET.x + (buzz ? Math.sin(t * 150) * .003 : 0) + take * .1, POCKET.y + take * .12, POCKET.z + take * .12);
  dyn.jk.ph.visible = !phoneClose && !phoneHeld;
  if (atJacket) dyn.armA.set(1, dyn.jk.ph.localToWorld(V(.01, -.03, .02)), { sag: .08, tint });

  // ---------------- elde telefon (yakın): şifre -> rehber -> aranıyor
  dyn.ph.g.visible = phoneClose;
  if (phoneClose) {
    const up = ramp(t, Lb('L08') - .1, Lb('L08') + .3);
    dyn.ph.g.position.set(PH.x, lerp(PH.y - .12, PH.y, up), PH.z); dyn.ph.g.rotation.set(lerp(-.6, -.12, up), .12, 0);
    const dots = t < Wd('L08', 3) ? Math.min(6, Math.floor((t - (Lb('L08') - .3)) / ((Wd('L08', 3) - Lb('L08') + .3) / 6))) : 6;
    let st;
    if (t < Lb('L09') - .1) st = { mode: 'kilit', dots: Math.max(0, dots) };
    else if (t < Lb('L10')) st = { mode: 'rehber', hl: ramp(t, Wd('L09', 5) - .2, Wd('L09', 5) + .2) };
    else st = { mode: 'arama', ring: ((t - Lb('L10')) * 1.2) % 1 };
    const key = JSON.stringify(st, (k, v) => typeof v === 'number' ? Math.round(v * 12) / 12 : v);
    if (dyn.scKey !== key) { dyn.scKey = key; screen(dyn.ph.c, st); dyn.ph.tex.needsUpdate = true; }
    dyn.ph.light.intensity = .6;
    dyn.armA.set(1, dyn.ph.g.localToWorld(V(.055, -.115, .01)), { sag: .04, tint: [.9, .9, 1] });
  }

  // banyo ışığı: su kesilince biraz söner
  const off = ramp(t, Wd('L13', 4), Wd('L13', 4) + .6);
  sets.an.sun.intensity = 3.4 - off * 1.1;

  // ---------------- lens
  let look;
  if (t < Wd('L01', 2) - .1) look = { focus: f(BAG), coc: 9, range: .3 };
  else if (t < Lb('L02') - .05) look = { focus: f(V(nx, 1.5, nz)), coc: 6, range: .8 };
  else if (t < Lb('L03') - .1) look = { focus: f(V(ax, 1.4, az)), coc: 6, range: .8 };
  else if (t < Lb('L04') - .05) look = { focus: f(V(nx, 1.5, nz)), coc: 6, range: .8 };
  else if (t < Lb('L05') - .05) look = { focus: f(V(ax, 1.3, az)), coc: 4, range: 1.4 };
  else if (t < Lb('L06') - .05) look = { focus: f(dyn.boot.g.position), coc: 10, range: .2 };
  else if (t < Lb('L07') - .05) look = { focus: f(V(ax, 1.4, az)), coc: 6, range: .7 };
  else if (t < Lb('L08') - .05) look = { focus: f(CEKET), coc: 6, range: .8 };
  else if (phoneClose) look = { focus: f(dyn.ph.g.position), coc: 10, range: .12 };
  else if (t < Lb('L13') - .05) look = { focus: f(V(ax, 1.4, az)), coc: 7, range: .6 };
  else look = { focus: f(V(ax, 1.4, az)), coc: 8, range: .5 };
  Object.assign(look, { sat: 1.12, lift: [.08, .07, .12], bloom: .9, vignette: .3, contrast: 1.07 });
  look.tint = GRADE;
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
