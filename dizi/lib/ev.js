// ev.js — Ayça ile Nihat'ın evi: bölümlerin ortak setleri (yatak odası, antre, salon penceresi).
// Kurallar (yumurta-stili): her sette görünen BİR ana ışık, sıcak-soğuk karşıtlığı, gerçek gölgeler, büyük duvarlarda desen,
// hiçbir yüzey başka bir yüzeyle aynı düzlemde değil (titreme), saf siyah yok.
import * as THREE from 'three';
import { woodTex, carpetTex, painted, flat, rng, shade, D } from '/engine/src/paint.js';
import { PLUM } from '/engine/src/toon.js';
import { holedWall, vistaMat, nightCityTex, dayGardenTex } from '/engine/src/vista.js';
import { glow } from '/engine/src/fx.js';

export const V = (...a) => new THREE.Vector3(...a);
export const HDR = (r, g, b) => new THREE.Color().setRGB(r, g, b);
const DEG = Math.PI / 180;

function cv(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return [c, c.getContext('2d')]; }
export function texOf(c, rep = [1, 1]) { const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = 8; t.wrapS = t.wrapT = THREE.RepeatWrapping; t.repeat.set(...rep); return t; }

// ---------------------------------------------------------------- dokular
// duvar kâğıdı: açık zemin üstünde ince çizgili damask motifleri (açık dolgu + ince koyu çizgi)
export function wallpaperTex({ base = '#8d9cc8', motif = '#a9b6dc', line, w = 512, h = 512, rep = [1, 1], seed = 5 } = {}) {
  const [c, g] = cv(w, h); g.fillStyle = base; g.fillRect(0, 0, w, h);
  const R = rng(seed), ln = line || shade(base, .62);
  for (let i = 0; i < 260; i++) { g.fillStyle = shade(base, .95 + R() * .1); g.globalAlpha = .3; g.beginPath(); g.ellipse(R() * w, R() * h, 30 * R() + 10, 12 * R() + 6, R() * 3, 0, 6.29); g.fill(); }
  g.globalAlpha = 1;
  for (const [x, y] of [[w * .25, h * .25], [w * .75, h * .75], [w * .75, -h * .25], [w * .25, h * 1.25], [-w * .25, h * .75], [w * 1.25, h * .75]]) {
    g.save(); g.translate(x, y); g.fillStyle = motif; g.strokeStyle = ln; g.lineWidth = 3;
    g.beginPath(); g.moveTo(0, -70); g.bezierCurveTo(38, -40, 30, 10, 0, 44); g.bezierCurveTo(-30, 10, -38, -40, 0, -70); g.fill(); g.stroke();   // yaprak
    for (const s of [-1, 1]) { g.beginPath(); g.moveTo(0, 30); g.bezierCurveTo(s * 50, 20, s * 64, -20, s * 40, -40); g.stroke();
      g.beginPath(); g.arc(s * 40, -46, 7, 0, 6.29); g.fill(); g.stroke(); }
    g.beginPath(); g.moveTo(0, 44); g.lineTo(0, 74); g.stroke(); g.restore();
  }
  g.strokeStyle = shade(base, .85); g.lineWidth = 2; g.globalAlpha = .6;
  for (const x of [0, w / 2]) { g.beginPath(); g.moveTo(x + 2, 0); g.lineTo(x + 2, h); g.stroke(); }
  g.globalAlpha = 1;
  return texOf(c, rep);
}
// yatak örtüsü: geniş kareli, kenarı şeritli pike
export function quiltTex({ base = '#d08a3e', alt = '#e3a95c', line = '#8a5220', w = 512, h = 512, rep = [1, 1] } = {}) {
  const [c, g] = cv(w, h); g.fillStyle = base; g.fillRect(0, 0, w, h);
  const n = 4, s = w / n;
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) if ((i + j) % 2) { g.fillStyle = alt; g.fillRect(i * s, j * s, s, s); }
  g.strokeStyle = line; g.lineWidth = 3; g.setLineDash([10, 8]);
  for (let k = 0; k <= n; k++) { g.beginPath(); g.moveTo(k * s, 0); g.lineTo(k * s, h); g.stroke(); g.beginPath(); g.moveTo(0, k * s); g.lineTo(w, k * s); g.stroke(); }
  g.setLineDash([]); g.fillStyle = shade(base, 1.25);
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { g.beginPath(); g.arc(i * s + s / 2, j * s + s / 2, 10, 0, 6.29); g.fill(); }
  return texOf(c, rep);
}
// zemin karosu / parke
export function tileFloorTex({ a = '#c9b89a', b = '#b9a684', line = '#7a6a50', w = 512, h = 512, rep = [1, 1] } = {}) {
  const [c, g] = cv(w, h), n = 4, s = w / n;
  for (let i = 0; i < n; i++) for (let j = 0; j < n; j++) { g.fillStyle = (i + j) % 2 ? a : b; g.fillRect(i * s, j * s, s, s); }
  g.strokeStyle = line; g.lineWidth = 2;
  for (let k = 0; k <= n; k++) { g.beginPath(); g.moveTo(k * s, 0); g.lineTo(k * s, h); g.stroke(); g.beginPath(); g.moveTo(0, k * s); g.lineTo(w, k * s); g.stroke(); }
  return texOf(c, rep);
}
// düğün fotoğrafı: iki yumurta kafa, gelinlik ve damatlık (Ayça + Nihat, 12 yıl önce)
export function weddingPhotoTex() {
  const [c, g] = cv(512, 640);
  let gr = g.createLinearGradient(0, 0, 0, 640); gr.addColorStop(0, D('#f3d9c4')); gr.addColorStop(1, D('#d9a7a0')); g.fillStyle = gr; g.fillRect(0, 0, 512, 640);
  g.fillStyle = D('#ffffff', .35); for (let i = 0; i < 18; i++) { g.beginPath(); g.arc(40 + (i * 97) % 440, 40 + (i * 53) % 260, 6 + (i % 3) * 4, 0, 6.29); g.fill(); }
  const ink = D('#2a1a2c');
  const head = (x, y, r) => { g.fillStyle = '#ffffff'; g.strokeStyle = ink; g.lineWidth = 7; g.beginPath(); g.ellipse(x, y, r, r * .93, 0, 0, 6.29); g.fill(); g.stroke();
    g.fillStyle = ink; for (const s of [-1, 1]) { g.beginPath(); g.arc(x + s * r * .3, y - r * .05, r * .12, 0, Math.PI); g.fill(); g.fillRect(x + s * r * .3 - r * .16, y - r * .07, r * .32, 5); }
    g.lineWidth = 5; g.beginPath(); g.arc(x, y + r * .28, r * .22, .3, Math.PI - .3); g.stroke(); };
  // damat (sol): siyah takım, papyon; gelin (sağ): duvak, gelinlik
  g.fillStyle = D('#2c2a3a'); g.strokeStyle = ink; g.lineWidth = 7; g.beginPath(); g.roundRect(80, 330, 170, 330, 60); g.fill(); g.stroke();
  g.fillStyle = '#ffffff'; g.beginPath(); g.moveTo(140, 336); g.lineTo(165, 420); g.lineTo(190, 336); g.closePath(); g.fill();
  g.fillStyle = D('#b8323a'); g.beginPath(); g.moveTo(150, 346); g.lineTo(180, 360); g.lineTo(150, 372); g.closePath(); g.fill(); g.beginPath(); g.moveTo(180, 346); g.lineTo(150, 360); g.lineTo(180, 372); g.closePath(); g.fill();
  g.fillStyle = D('#1f1a22'); g.beginPath(); g.ellipse(165, 200, 98, 70, 0, Math.PI, 0); g.fill();
  head(165, 250, 92);
  g.fillStyle = D('#f8f4ee'); g.beginPath(); g.moveTo(300, 340); g.bezierCurveTo(260, 500, 250, 600, 240, 660); g.lineTo(480, 660); g.bezierCurveTo(470, 600, 460, 500, 420, 340); g.closePath(); g.fill(); g.stroke();
  g.fillStyle = D('#ffffff', .7); g.beginPath(); g.moveTo(300, 150); g.bezierCurveTo(230, 260, 240, 420, 250, 520); g.lineTo(470, 520); g.bezierCurveTo(480, 420, 490, 260, 420, 150); g.closePath(); g.fill();
  g.fillStyle = D('#4a2a1e'); g.beginPath(); g.ellipse(360, 230, 100, 110, 0, Math.PI * .95, Math.PI * 2.05); g.fill();
  head(360, 260, 88);
  g.fillStyle = D('#f4a6b0', .5); for (const x of [335, 385]) { g.beginPath(); g.ellipse(x, 280, 16, 8, 0, 0, 6.29); g.fill(); }
  g.fillStyle = D('#f8f4ee'); for (let k = 0; k < 7; k++) { g.beginPath(); g.arc(300 + k * 20, 150 - Math.sin(k / 6 * Math.PI) * 26, 12, 0, 6.29); g.fill(); g.stroke(); }   // taç
  for (const [x, y, col] of [[262, 420, '#f2a7b8'], [282, 438, '#ffffff'], [250, 446, '#f6d06a']]) { g.fillStyle = D(col); g.beginPath(); g.arc(x, y, 16, 0, 6.29); g.fill(); g.stroke(); }  // buket
  return texOf(c);
}
// telefon ekranı (kilit ekranı + bildirim)
export function phoneScreen(c, { saat = '02:14', gonderen = 'Bizim Takımdaki Kaan', mesaj = 'Yarın aynı yerde mi?', bildirim = 1, vurgu = 0 } = {}) {
  const g = c.getContext('2d'), w = c.width, h = c.height;
  let gr = g.createLinearGradient(0, 0, w, h); gr.addColorStop(0, D('#2a3a8a')); gr.addColorStop(1, D('#6a3a8a')); g.fillStyle = gr; g.fillRect(0, 0, w, h);
  g.fillStyle = D('#ffffff', .1); for (let i = 0; i < 6; i++) { g.beginPath(); g.arc(w * (.2 + i * .15), h * (.7 - (i % 2) * .1), w * .25, 0, 6.29); g.fill(); }
  g.fillStyle = D('#ffffff'); g.textAlign = 'center'; g.font = `600 ${w * .26}px Poppins, sans-serif`; g.fillText(saat, w / 2, h * .22);
  g.font = `500 ${w * .055}px Poppins, sans-serif`; g.fillStyle = D('#e8e8ff', .85); g.fillText('Cuma, 27 Kasım', w / 2, h * .28);
  if (bildirim <= 0) return;
  g.globalAlpha = Math.min(1, bildirim);
  const bx = w * .06, by = h * .38 - (1 - Math.min(1, bildirim)) * h * .04, bw = w * .88, bh = h * .2;
  g.fillStyle = D('#f6f4fb', .94); g.beginPath(); g.roundRect(bx, by, bw, bh, w * .06); g.fill();
  if (vurgu > 0) { g.strokeStyle = D('#ffcf5a', vurgu); g.lineWidth = w * .015; g.stroke(); }
  // uygulama simgesi (yeşil konuşma balonu) + gönderen + futbol topu
  g.fillStyle = D('#3fbf6a'); g.beginPath(); g.roundRect(bx + w * .04, by + h * .025, w * .11, w * .11, w * .03); g.fill();
  g.fillStyle = '#fff'; g.beginPath(); g.ellipse(bx + w * .095, by + h * .025 + w * .05, w * .035, w * .028, 0, 0, 6.29); g.fill();
  g.textAlign = 'left'; g.fillStyle = D('#1a1630'); g.font = `700 ${w * .062}px Poppins, sans-serif`;
  g.fillText(gonderen, bx + w * .19, by + h * .055);
  const ballX = bx + w * .19 + g.measureText(gonderen).width + w * .05, ballY = by + h * .045;
  g.fillStyle = '#fff'; g.strokeStyle = D('#1a1630'); g.lineWidth = w * .008; g.beginPath(); g.arc(ballX, ballY, w * .028, 0, 6.29); g.fill(); g.stroke();
  g.fillStyle = D('#1a1630'); g.beginPath(); for (let k = 0; k < 5; k++) { const a = -Math.PI / 2 + k * 2 * Math.PI / 5; g.lineTo(ballX + Math.cos(a) * w * .011, ballY + Math.sin(a) * w * .011); } g.fill();
  g.font = `500 ${w * .045}px Poppins, sans-serif`; g.fillStyle = D('#6a6680'); g.fillText('şimdi', bx + w * .19, by + h * .09);
  g.font = `600 ${w * .072}px Poppins, sans-serif`; g.fillStyle = D('#1a1630'); g.fillText(mesaj, bx + w * .06, by + h * .155);
  g.globalAlpha = 1;
}
// dijital saat ekranı
export function clockFace(c, text = '02:14', on = 1) {
  const g = c.getContext('2d'); g.fillStyle = '#100808'; g.fillRect(0, 0, c.width, c.height);
  g.fillStyle = `rgba(255,${120 + 40 * on},${60},${.25 + .75 * on})`; g.font = `700 ${c.height * .72}px Poppins, monospace`; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillText(text, c.width / 2, c.height * .54);
}

// ---------------------------------------------------------------- yardımcılar
export function shadows(g) {
  g.traverse(o => {
    if (!o.isMesh || o.isInstancedMesh) return;
    if (o.material.isMeshLambertMaterial) o.receiveShadow = true;
    if (/Box|Cylinder|Extrude|Lathe|Torus|Capsule|Sphere/.test(o.geometry.type) && !o.userData.noShadow) o.castShadow = true;
  });
}
export function keySpot(color, intensity, pos, target, angle, { map, size = 2048, near = .5, far = 40, penumbra = .4, decay = 0 } = {}) {
  const l = new THREE.SpotLight(color, intensity, 0, angle, penumbra, decay);
  l.position.set(...pos); l.target.position.set(...target); l.castShadow = true;
  l.shadow.mapSize.set(size, size); l.shadow.camera.near = near; l.shadow.camera.far = far; l.shadow.bias = -.0006; l.shadow.normalBias = .03; l.shadow.radius = 3;
  if (map) l.map = map;
  return l;
}
export function gobo(draw, s = 512) {
  const [c, g] = cv(s, s); g.fillStyle = '#000'; g.fillRect(0, 0, s, s); draw(g, s);
  const t = new THREE.CanvasTexture(c); t.colorSpace = THREE.SRGBColorSpace; return t;
}
const box = (w, h, d, mat, x, y, z, parent) => { const m = new THREE.Mesh(new THREE.BoxGeometry(w, h, d), mat); m.position.set(x, y, z); parent.add(m); return m; };
const plane = (w, h, mat, x, y, z, ry, parent) => { const m = new THREE.Mesh(new THREE.PlaneGeometry(w, h), mat); m.position.set(x, y, z); m.rotation.y = ry || 0; parent.add(m); return m; };
// yumuşak kenarlı kutu (yastık, yorgan): yuvarlatılmış köşeler
function soft(w, h, d, r, mat) {
  const s = new THREE.Shape(), x = w / 2 - r, y = h / 2 - r;
  s.moveTo(-x, -h / 2); s.lineTo(x, -h / 2); s.quadraticCurveTo(w / 2, -h / 2, w / 2, -y); s.lineTo(w / 2, y); s.quadraticCurveTo(w / 2, h / 2, x, h / 2);
  s.lineTo(-x, h / 2); s.quadraticCurveTo(-w / 2, h / 2, -w / 2, y); s.lineTo(-w / 2, -y); s.quadraticCurveTo(-w / 2, -h / 2, -x, -h / 2);
  const geo = new THREE.ExtrudeGeometry(s, { depth: d - 2 * r * .6, bevelEnabled: true, bevelSize: r * .6, bevelThickness: r * .6, bevelSegments: 4, curveSegments: 8 });
  geo.translate(0, 0, -(d - 2 * r * .6) / 2); return new THREE.Mesh(geo, mat);
}
// bir lamba: abajur (ışık yanınca içi parlar), gövde, ampul ışığı
function lamp(parent, x, y, z, { shade: shadeCol = '#e8d8b8', base = '#5a6a8a' } = {}) {
  const g = new THREE.Group(); g.position.set(x, y, z); parent.add(g);
  const b = new THREE.Mesh(new THREE.CylinderGeometry(.06, .08, .22, 18), flat(base)); b.position.y = .11; g.add(b);
  const st = new THREE.Mesh(new THREE.CylinderGeometry(.012, .012, .14, 8), flat('#c9a64a')); st.position.y = .29; g.add(st);
  const shM = new THREE.MeshLambertMaterial({ color: shadeCol, side: THREE.DoubleSide, emissive: new THREE.Color('#000') });
  const sh = new THREE.Mesh(new THREE.CylinderGeometry(.1, .16, .2, 24, 1, true), shM); sh.position.y = .44; sh.userData.noShadow = true; g.add(sh);
  const bulb = new THREE.Mesh(new THREE.SphereGeometry(.035, 12, 8), new THREE.MeshBasicMaterial({ color: '#3a3020' })); bulb.position.y = .4; g.add(bulb);
  const light = new THREE.PointLight('#ffc78a', 0, 0, 1.4); light.position.y = .42; light.castShadow = true; light.shadow.mapSize.set(1024, 1024); light.shadow.bias = -.002; light.shadow.radius = 4; g.add(light);
  const halo = glow(parent, [x, y + .44, z], '#ffb870', .9, 0);
  return { g, set(on) { light.intensity = 3.2 * on; shM.emissive.setRGB(1.2 * on, .8 * on, .38 * on); bulb.material.color.setRGB(.25 + 3 * on, .2 + 2.2 * on, .12 + 1 * on); halo.material.opacity = .55 * on; halo.visible = on > .01; } };
}

// ---------------------------------------------------------------- YATAK ODASI (x ≈ 0), gece
// Yatak arka duvara dayalı; kamera ayak ucundan bakar. Uzanan kişiler: yastıktaki kafa kartı (gövdeyi yorgan saklar).
export const YO = { x: 0, pillowZ: -2.02, headY: .98, nihatX: -.5, aycaX: .5, phone: V(-1.3, .556, -2.02), clock: V(1.38, .556, -2.06) };
export function yatakOdasi(scene) {
  const g = new THREE.Group(); scene.add(g); const L = new THREE.Group(); scene.add(L);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(8, 7), painted(woodTex({ base: '#8a6a52', plank: 48, rep: [3, 3] }))); floor.rotation.x = -Math.PI / 2; floor.position.z = -.5; g.add(floor);
  const wp = wallpaperTex({ base: '#7d8cc0', motif: '#99a8d6', rep: [1 / .9, 1 / .9] });
  // arka duvar pencereli (sağda), sol ve sağ duvar
  const back = holedWall(8, 2.8, [1.75, .95, 2.75, 2.25], painted(wp)); back.position.set(0, 0, -2.4); g.add(back);
  const left = plane(7, 2.8, painted(wallpaperTex({ base: '#7d8cc0', motif: '#99a8d6', rep: [1 / .9, 1 / .9], seed: 8 })), -3.2, 1.4, -.5, Math.PI / 2, g);
  plane(7, 2.8, painted(wp), 3.2, 1.4, -.5, -Math.PI / 2, g);
  // duvar altı lambri (duvardan 4 cm önde) + pervaz
  const pan = flat('#e8e2f0');
  box(8, .9, .03, flat('#c9c4dc'), 0, .45, -2.37, g); box(8, .06, .06, pan, 0, .92, -2.35, g); box(8, .1, .04, flat('#6a5a7a'), 0, .05, -2.36, g);
  box(.03, .9, 7, flat('#c9c4dc'), -3.17, .45, -.5, g); box(.06, .06, 7, pan, -3.15, .92, -.5, g);
  // yatak: baza, başlık (kapitone), şilte, yorgan, yastıklar
  const fabric = flat('#6a4a7a'), wood = painted(woodTex({ base: '#6a4632', rep: [1, 1] }));
  box(2.2, .32, 2.25, wood, 0, .16, -1.25, g);
  const head = box(2.3, 1.2, .14, fabric, 0, .74, -2.31, g);
  for (let i = -3; i <= 3; i++) for (const y of [.55, .85, 1.12]) { const b = new THREE.Mesh(new THREE.SphereGeometry(.025, 8, 6), flat('#4a3058')); b.position.set(i * .3, y, -2.235); g.add(b); }
  box(2.1, .22, 2.12, flat('#eae6f2'), 0, .43, -1.22, g);
  const pillowM = flat('#f4f1fa');
  for (const x of [-.5, .5]) { const p = soft(.78, .2, .42, .08, pillowM); p.position.set(x, .66, -2.0); p.rotation.x = -.35; g.add(p); }
  const quilt = soft(2.16, .16, 1.75, .06, painted(quiltTex({ rep: [1.5, 1.5] }))); quilt.position.set(0, .62, -.98); g.add(quilt);
  const fold = soft(2.18, .07, .26, .03, flat('#f4f1fa')); fold.position.set(0, .71, -1.83); g.add(fold);           // çarşaf kıvrımı (kafaların önü)
  for (const x of [-.5, .5]) { const b = soft(.6, .14, 1.4, .07, painted(quiltTex({ rep: [.6, 1.2] }))); b.position.set(x, .7, -1.05); g.add(b); }   // yorganın altındaki bedenler
  // komodinler, telefon (Nihat), saat ve lamba (Ayça), Nihat'ın lambası
  const nsM = painted(woodTex({ base: '#a07850', rep: [1, 1], vertical: true }));
  for (const s of [-1, 1]) { box(.5, .55, .42, nsM, s * 1.38, .275, -2.12, g); box(.42, .16, .02, flat('#8a6440'), s * 1.38, .38, -1.9, g); const k = new THREE.Mesh(new THREE.SphereGeometry(.02, 8, 6), flat('#d8b44a')); k.position.set(s * 1.38, .38, -1.885); g.add(k); }
  const phone = new THREE.Group(); phone.position.copy(YO.phone); g.add(phone);
  const pb = box(.078, .009, .158, flat('#2a2632'), 0, 0, 0, phone);
  const leak = new THREE.Mesh(new THREE.PlaneGeometry(.1, .19), new THREE.MeshBasicMaterial({ color: HDR(.45, .62, 1.15), transparent: true, opacity: 0, depthWrite: false }));
  leak.rotation.x = -Math.PI / 2; leak.position.y = -.004; leak.layers.set(1); phone.add(leak);
  const phoneLight = new THREE.PointLight('#bcd6ff', 0, 0, 1.5); phoneLight.position.set(0, .08, .05); phone.add(phoneLight);
  const [sc] = cv(360, 720), scTex = texOf(sc); scTex.repeat.set(1, 1);
  const screen = new THREE.Mesh(new THREE.PlaneGeometry(.07, .14), new THREE.MeshBasicMaterial({ map: scTex, color: HDR(1.15, 1.15, 1.15) })); screen.layers.set(1);
  const handPhone = new THREE.Group(); scene.add(handPhone);                                  // elde kaldırılan telefon (yakın plan)
  box(.08, .16, .009, flat('#2a2632'), 0, 0, -.006, handPhone); screen.position.z = .0; handPhone.add(screen); handPhone.visible = false;
  const clock = new THREE.Group(); clock.position.copy(YO.clock); g.add(clock);
  box(.18, .08, .07, flat('#3a3448'), 0, .04, 0, clock);
  const [cc] = cv(256, 96), ccTex = texOf(cc); clockFace(cc);
  const cface = new THREE.Mesh(new THREE.PlaneGeometry(.15, .055), new THREE.MeshBasicMaterial({ map: ccTex, color: HDR(1.05, .95, .9) })); cface.position.set(0, .042, .036); cface.layers.set(1); clock.add(cface);
  const clockLight = new THREE.PointLight('#ff9a60', .12, 0, 2); clockLight.position.set(0, .1, .12); clock.add(clockLight);
  const lampN = lamp(g, -1.42, .55, -2.2, { base: '#5a6a8a' }), lampA = lamp(g, 1.5, .55, -2.22, { base: '#8a5a6a' });
  // duvarda düğün fotoğrafı (çerçeve duvardan önde)
  box(.86, 1.04, .04, flat('#c9a24a'), 0, 1.9, -2.36, g); plane(.72, .9, new THREE.MeshBasicMaterial({ map: weddingPhotoTex(), color: HDR(.9, .88, .9) }), 0, 1.9, -2.335, 0, g);
  // pencere: kasa, pervaz, cam arkası gece şehri, perdeler
  const winM = flat('#e6e2f2');
  box(1.12, .08, .1, winM, 2.25, .93, -2.36, g); box(1.12, .08, .08, winM, 2.25, 2.27, -2.37, g);
  for (const x of [1.71, 2.79]) box(.08, 1.38, .08, winM, x, 1.6, -2.37, g);
  box(.04, 1.3, .04, winM, 2.25, 1.6, -2.4, g); box(1.0, .04, .04, winM, 2.25, 1.6, -2.4, g);
  const camHold = [0, 1.5, 1.8];
  const vis = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 1.4), vistaMat(nightCityTex(), { yaw: Math.atan2(2.25 - camHold[0], -2.7 - camHold[2]) + Math.PI, az: 70 * DEG, el: [-12 * DEG, 30 * DEG], gain: 1.25 }));
  vis.position.set(2.25, 1.6, -2.6); g.add(vis);
  const curtainM = painted(curtainTex('#4a3a7a')), curtains = [];
  for (const s of [-1, 1]) { const c = new THREE.Mesh(new THREE.PlaneGeometry(.55, 2.3, 8, 1), curtainM); c.position.set(2.25 + s * .72, 1.3, -2.28); g.add(c); curtains.push(c);
    const pos = c.geometry.attributes.position; for (let i = 0; i < pos.count; i++) pos.setZ(i, Math.sin(pos.getX(i) * 40) * .025); c.geometry.computeVertexNormals(); }
  box(1.9, .04, .04, flat('#c9a64a'), 2.25, 2.46, -2.25, g);
  // dolap (sol duvar), halı, saksı
  const wd = painted(woodTex({ base: '#b89a74', rep: [1, 1], vertical: true }));
  box(.6, 2.1, 1.5, wd, -2.88, 1.05, -.2, g); box(.02, 1.9, .01, flat('#6a5040'), -2.575, 1.05, -.2, g);
  for (const z of [-.3, -.1]) { const k = box(.03, .14, .03, flat('#d8b44a'), -2.56, 1.1, z, g); }
  const rug = new THREE.Mesh(new THREE.PlaneGeometry(2.8, 1.4), painted(carpetTex({ base: '#5a6aa8', band: '#e6b45a', rep: [1, 1] }))); rug.rotation.x = -Math.PI / 2; rug.position.set(0, .006, .55); g.add(rug);
  // ışık: ay ışığı penceresinden (soğuk anahtar, pencere kafesli), şehrin sıcak sokak ışığı, zayıf mavi dolgu
  const moonMap = gobo((q, s) => { q.fillStyle = '#fff'; q.fillRect(s * .2, s * .2, s * .6, s * .6); q.fillStyle = '#000'; q.fillRect(s * .49, s * .2, s * .02, s * .6); q.fillRect(s * .2, s * .49, s * .6, s * .02); });
  const moon = keySpot('#9fb4ff', 3.6, [4.2, 4.4, -5.5], [.1, .6, -1.3], 22 * DEG, { map: moonMap }); L.add(moon); L.add(moon.target);
  const street = new THREE.PointLight('#ff9a50', 1.8, 0, 1.1); street.position.set(2.3, 1.2, -2.8); L.add(street);
  const hemi = new THREE.HemisphereLight('#5a6ac0', '#3a2a50', 1.05); L.add(hemi);
  shadows(g);
  [phone, clock].forEach(o => o.traverse(m => { if (m.isMesh) m.castShadow = false; }));
  return { g, L, phone, leak, phoneLight, sc, scTex, screen, handPhone, cc, ccTex, lampN, lampA, moon, hemi, curtains };
}
function curtainTex(base) {
  const [c, g] = cv(256, 512); g.fillStyle = base; g.fillRect(0, 0, 256, 512);
  for (let x = 0; x < 256; x += 32) { const gr = g.createLinearGradient(x, 0, x + 32, 0); gr.addColorStop(0, shade(base, .7)); gr.addColorStop(.5, shade(base, 1.2)); gr.addColorStop(1, shade(base, .7)); g.fillStyle = gr; g.fillRect(x, 0, 32, 512); }
  g.strokeStyle = shade(base, 1.5); g.lineWidth = 3; for (let y = 40; y < 512; y += 90) { g.beginPath(); for (let x = 0; x <= 256; x += 16) g.lineTo(x, y + Math.sin(x / 20) * 6); g.stroke(); }
  return texOf(c);
}

// ---------------------------------------------------------------- ANTRE (x ≈ 100), sabah
export const AN = { x: 100, door: V(100.6, 0, -2.3), mirror: V(98.9, 1.45, -2.33) };
export function antre(scene) {
  const g = new THREE.Group(); scene.add(g); const L = new THREE.Group(); scene.add(L);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(8, 6), painted(tileFloorTex({ rep: [6, 4.5] }))); floor.rotation.x = -Math.PI / 2; floor.position.set(100, 0, -.5); g.add(floor);
  const wp = wallpaperTex({ base: '#e8c9a0', motif: '#f2dcb8', line: '#a8825a', rep: [1 / .8, 1 / .8], seed: 11 });
  // arka duvar: kapı boşluğu (sağda) ; sağ duvar: mutfak kapısı boşluğu (güneş oradan girer)
  const back = holedWall(8, 2.8, [.1, 0, 1.1, 2.1], painted(wp)); back.position.set(100, 0, -2.4); g.add(back);
  const right = holedWall(6, 2.8, [-.2, 0, .8, 2.1], painted(wp)); right.position.set(102.6, 0, -.5); right.rotation.y = -Math.PI / 2; g.add(right);
  plane(6, 2.8, painted(wallpaperTex({ base: '#e8c9a0', motif: '#f2dcb8', line: '#a8825a', rep: [1 / .8, 1 / .8], seed: 12 })), 97.4, 1.4, -.5, Math.PI / 2, g);
  box(8, .9, .03, flat('#7a9a8a'), 100, .45, -2.37, g); box(8, .06, .06, flat('#f2ece0'), 100, .92, -2.35, g);   // yeşil lambri
  // dış kapı (menteşe solda, açılır), kasa, dürbün, kol, buzlu cam şerit
  const kasa = flat('#f2ece0');
  box(.1, 2.18, .14, kasa, 100.05, 1.09, -2.38, g); box(.1, 2.18, .14, kasa, 101.15, 1.09, -2.38, g); box(1.2, .1, .14, kasa, 100.6, 2.15, -2.38, g);
  const pivot = new THREE.Group(); pivot.position.set(100.12, 0, -2.42); g.add(pivot);
  const doorM = painted(woodTex({ base: '#7a4a32', rep: [1, 2], vertical: true }));
  const leaf = box(.96, 2.08, .06, doorM, .48, 1.04, 0, pivot);
  for (const y of [.55, 1.5]) box(.7, .7, .02, flat('#6a3e28'), .48, y, .04, pivot);
  box(.04, .14, .04, flat('#d8b44a'), .86, 1.02, .06, pivot); const eye = new THREE.Mesh(new THREE.CylinderGeometry(.015, .015, .02, 10), flat('#d8b44a')); eye.rotation.x = Math.PI / 2; eye.position.set(.48, 1.55, .05); pivot.add(eye);
  const outside = plane(1.0, 2.1, new THREE.MeshBasicMaterial({ color: HDR(1.05, 1.1, 1.3) }), 100.6, 1.05, -2.6, 0, g);   // merdiven boşluğu ışığı
  // ayna (çerçeveli, duvardan önde) + altında ayakkabılık + anahtar kâsesi, askılık
  box(.72, 1.02, .05, flat('#c9a24a'), AN.mirror.x, AN.mirror.y, -2.36, g);
  const [mc, mg] = cv(256, 384); let gr = mg.createLinearGradient(0, 0, 256, 384); gr.addColorStop(0, D('#dfe9f4')); gr.addColorStop(.5, D('#a9bcd8')); gr.addColorStop(1, D('#e7eef6')); mg.fillStyle = gr; mg.fillRect(0, 0, 256, 384);
  mg.strokeStyle = D('#ffffff', .7); mg.lineWidth = 10; for (const o of [60, 110]) { mg.beginPath(); mg.moveTo(o, 0); mg.lineTo(o + 120, 384); mg.stroke(); }
  plane(.6, .9, new THREE.MeshBasicMaterial({ map: texOf(mc) }), AN.mirror.x, AN.mirror.y, -2.33, 0, g);
  const sk = painted(woodTex({ base: '#f0e6d4', rep: [1, 1] }));
  box(1.1, .85, .38, sk, AN.mirror.x, .425, -2.18, g); box(1.14, .04, .42, flat('#c9b090'), AN.mirror.x, .87, -2.18, g);
  const bowl = new THREE.Mesh(new THREE.CylinderGeometry(.1, .06, .05, 20), flat('#3a7ab8')); bowl.position.set(AN.mirror.x + .32, .915, -2.15); g.add(bowl);
  box(.6, .05, .05, flat('#6a4632'), 97.75, 1.7, -1.4, g).rotation.y = Math.PI / 2;
  for (const [z, col] of [[-1.6, '#3a5a8a'], [-1.25, '#a85a3a']]) { const c = soft(.07, .75, .32, .03, flat(col)); c.position.set(97.5, 1.3, z); g.add(c); }
  const plant = new THREE.Mesh(new THREE.CylinderGeometry(.16, .12, .34, 16), flat('#c86a3a')); plant.position.set(101.9, .17, -2.05); g.add(plant);
  for (let i = 0; i < 7; i++) { const l = new THREE.Mesh(new THREE.SphereGeometry(.14, 10, 8), flat(i % 2 ? '#3f8a5a' : '#2f7a4a')); l.scale.set(.6, 1.5, .6); l.position.set(101.9 + Math.cos(i) * .12, .55 + (i % 3) * .1, -2.05 + Math.sin(i) * .1); l.rotation.z = Math.cos(i) * .4; g.add(l); }
  // mutfak tarafı: kapının ardında sıcak güneşli duvar
  plane(2, 2.6, flat('#f6d6a0'), 104.0, 1.3, -.2, -Math.PI / 2, g);
  // ışık: mutfak penceresinden gelen sabah güneşi (sıcak anahtar, pencere deseni yere ve duvara), soğuk dolgu
  const sunMap = gobo((q, s) => { q.fillStyle = '#fff'; for (const [x, y] of [[.15, .15], [.52, .15], [.15, .52], [.52, .52]]) q.fillRect(s * x, s * y, s * .33, s * .33); });
  const sun = keySpot('#ffd08a', 4.2, [107, 3.2, .6], [100, .2, -1.6], 16 * DEG, { map: sunMap }); L.add(sun); L.add(sun.target);
  const fill = new THREE.HemisphereLight('#b8c8ee', '#7a6a5a', 1.35); L.add(fill);
  const doorLight = new THREE.PointLight('#cfe0ff', 0, 0, 1.4); doorLight.position.set(100.6, 1.4, -2.9); L.add(doorLight);
  shadows(g);
  return { g, L, pivot, doorLight, outside, sun };
}

// ---------------------------------------------------------------- SALON PENCERESİ (x ≈ 200), sabah
export const SP = { x: 200, aycaPos: V(200.05, 0, -1.0) };
export function salonPencere(scene) {
  const g = new THREE.Group(); scene.add(g); const L = new THREE.Group(); scene.add(L);
  const floor = new THREE.Mesh(new THREE.PlaneGeometry(8, 6), painted(woodTex({ base: '#9a7454', plank: 48, rep: [3, 3] }))); floor.rotation.x = -Math.PI / 2; floor.position.set(200, 0, -.5); g.add(floor);
  const wp = wallpaperTex({ base: '#c7a6b4', motif: '#dcc0cc', line: '#8a6a7a', rep: [1 / .85, 1 / .85], seed: 21 });
  const back = holedWall(8, 2.8, [.4, .7, 2.0, 2.4], painted(wp)); back.position.set(200, 0, -2.4); g.add(back);
  plane(6, 2.8, painted(wp), 197, 1.4, -.5, Math.PI / 2, g);
  box(8, .7, .03, flat('#8a7a9a'), 200, .35, -2.37, g); box(8, .06, .06, flat('#f2ece0'), 200, .72, -2.35, g);
  const winM = flat('#f2eef6');
  box(1.7, .08, .2, winM, 201.2, .66, -2.32, g); box(1.7, .08, .1, winM, 201.2, 2.44, -2.36, g);
  for (const x of [200.4, 202.0]) box(.08, 1.78, .1, winM, x, 1.55, -2.36, g);
  box(.05, 1.7, .05, winM, 201.2, 1.55, -2.4, g);
  const camHold = [199.6, 1.45, 1.2];
  const vis = new THREE.Mesh(new THREE.PlaneGeometry(1.8, 1.9), vistaMat(dayGardenTex(), { yaw: Math.atan2(201.2 - camHold[0], -2.7 - camHold[2]) + Math.PI, az: 80 * DEG, el: [-14 * DEG, 30 * DEG], gain: 1.15 }));
  vis.position.set(201.2, 1.55, -2.6); g.add(vis);
  // tül perde (yarı saydam), koltuk köşesi, sehpa, saksı
  const tul = new THREE.Mesh(new THREE.PlaneGeometry(.7, 2.2, 10, 1), new THREE.MeshLambertMaterial({ color: '#f4f0fa', transparent: true, opacity: .55, side: THREE.DoubleSide }));
  tul.position.set(200.2, 1.35, -2.25); { const p = tul.geometry.attributes.position; for (let i = 0; i < p.count; i++) p.setZ(i, Math.sin(p.getX(i) * 30) * .03); tul.geometry.computeVertexNormals(); } tul.userData.noShadow = true; g.add(tul);
  const sofa = soft(1.6, .5, .8, .12, flat('#3a6a8a')); sofa.position.set(198.0, .35, -1.6); g.add(sofa);
  const back2 = soft(1.6, .5, .25, .1, flat('#2f5a78')); back2.position.set(198.0, .75, -1.95); g.add(back2);
  const pot = new THREE.Mesh(new THREE.CylinderGeometry(.18, .14, .4, 16), flat('#e8e2d6')); pot.position.set(202.4, .2, -2.0); g.add(pot);
  for (let i = 0; i < 9; i++) { const l = new THREE.Mesh(new THREE.SphereGeometry(.18, 10, 8), flat(i % 2 ? '#4f9a5a' : '#3a7a4a')); l.scale.set(.5, 1.6, .5); l.position.set(202.4 + Math.cos(i * 1.3) * .16, .7 + (i % 3) * .14, -2.0 + Math.sin(i * 1.3) * .12); l.rotation.z = Math.cos(i * 1.3) * .5; g.add(l); }
  // ışık: pencereden serin sabah ışığı (anahtar, kafes deseni), içeride sıcak bir abajur (dolgu)
  const winMap = gobo((q, s) => { q.fillStyle = '#fff'; q.fillRect(s * .18, s * .12, s * .3, s * .76); q.fillRect(s * .52, s * .12, s * .3, s * .76); });
  const day = keySpot('#dfe8ff', 2.6, [203.6, 3.6, -6.5], [199.6, .9, -.4], 20 * DEG, { map: winMap }); L.add(day); L.add(day.target);
  box(.5, .55, .45, painted(woodTex({ base: '#a07850', rep: [1, 1] })), 197.4, .275, -1.9, g); const lampL = lamp(g, 197.4, .55, -1.95, { shade: '#f2dcb0', base: '#c9a64a' }); lampL.set(.7);
  const hemi = new THREE.HemisphereLight('#9fb0e0', '#5a4a5a', .7); L.add(hemi);
  shadows(g);
  return { g, L };
}
