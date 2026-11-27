// Çapkın Nihat · Bölüm 1 · "Gece 02.14"
// Setler: YATAK ODASI (x≈0, gece), ANTRE (x≈100, sabah), SALON PENCERESİ (x≈200, sabah).
// Her şey satır saatlerine bağlı: Lb('L06') = satırın başı, Wd('L06', 6) = o satırın 7. kelimesinin başı (voice/words.json).
// İç ses satırlarında ağız oynamaz (düşünce); yalnızca yüksek sesle konuşan karakterin ağzı oynar.
import * as THREE from 'three';
import { Toon, Arm3D, PLUM, flap, blinkAt } from '/engine/src/toon.js';
import { CamPath, smoother } from '/engine/src/camera.js';
import { Smoke } from '/engine/src/fx.js';
import { LOOK as KADRO } from '/lib/kadro.js';
import { yatakOdasi, antre, salonPencere, YO, AN, SP, V, HDR, phoneScreen, clockFace } from '/lib/ev.js';

export const NAME = 'capkin-nihat-01';
export const FPS = 30;
export let DUR = 50;
export const CUES = [];
export const LOOK = KADRO;
export const BOLUM = { no: 1, ad: 'Gece 02.14', soru: 'Sence Nihat nereye gidiyor?', sonraki: '2. BÖLÜM YARIN 20.00' };

const S = smoother;
const ramp = (t, a, b) => S((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
let C, LINES, WORDS, cast = {}, sets = {}, dyn = {};
const Lb = id => LINES.find(l => l.id === id).start;
const Le = id => LINES.find(l => l.id === id).end;
const Wd = (id, n) => WORDS.filter(w => w.line === id)[n].start;
const END = 3.2;                       // son kart süresi

// ---------------------------------------------------------------- kamera
function cameraPath() {
  const k = [];
  const key = (t, pos, look, fov, move = 'glide', dur = .6, extra = {}) => k.push({ t, pos, look, fov, move, dur, ...extra });
  const ph = YO.phone, ck = YO.clock;
  // kanca: üç resim, her biri cümlenin bir parçası
  key(0, [ck.x + .2, .74, ck.z + .55], [ck.x - .02, .6, ck.z], 30, 'cut', 0, { creep: .35, drift: .03 });         // saat 02:14
  key(Lb('L02') - .05, [ph.x + .18, .78, ph.z + .5], [ph.x, .57, ph.z], 30, 'whip', .28, { creep: .4, drift: .03 }); // titreyen telefon
  key(Lb('L03') - .05, [YO.aycaX + .75, 1.25, .3], [YO.aycaX - .05, 1.0, YO.pillowZ], 38, 'whip', .28, { creep: .3, drift: .04 }); // Ayça yastıkta
  // geniş: oda, ikisi yatakta, düğün fotoğrafı
  key(Lb('L04') - .1, [0, 1.62, 1.75], [0, 1.05, -1.9], 46, 'glide', .9, { creep: .1 });
  key(Lb('L05') - .1, [-1.62, .84, -1.45], [ph.x + .03, .6, ph.z], 36, 'glide', .9, { creep: .2, drift: .04 });
  // ekran: elde kaldırılan telefon (yakın)
  key(Lb('L06') - .05, [ph.x + .66, .99, ph.z + .72], [ph.x + .48, .865, ph.z + .38], 28, 'cut', 0, { creep: .12, drift: .02 });
  key(Lb('L07') - .05, [ph.x + .62, .955, ph.z + .64], [ph.x + .478, .868, ph.z + .38], 21, 'glide', .5, { creep: .35, drift: .01 });
  // şok: Ayça'nın yüzü
  key(Lb('L08') - .08, [YO.aycaX + .45, 1.2, .15], [YO.aycaX, 1.02, YO.pillowZ], 36, 'whip', .26, { creep: .45, drift: .03 });
  // Nihat uyanır: iki kişilik orta plan
  key(Lb('L09') - .25, [0, 1.42, 1.05], [0, 1.0, -2.0], 50, 'cut', 0, { creep: .2 });
  key(Lb('L10') - .05, [.25, 1.3, .55], [.25, 1.08, -2.0], 44, 'glide', .5, { creep: .25 });
  // yalnız ve karanlık: Ayça'ya yavaşça yaklaş
  key(Lb('L11') - .1, [YO.aycaX + .25, 1.25, .6], [YO.aycaX, 1.04, YO.pillowZ], 38, 'glide', .9, { creep: .1, drift: .03 });
  // sabah, antre: Nihat aynada; Ayça mutfak kapısında
  key(Lb('L12') - .1, [99.9, 1.5, 1.9], [99.7, 1.15, -1.6], 56, 'whip', .32, { creep: .22 });
  key(Lb('L13') - .1, [100.4, 1.45, 1.7], [100.35, 1.15, -1.6], 52, 'glide', .7, { creep: .25 });
  // son: salon penceresi, Ayça'ya yaklaş
  key(Lb('L14') - .2, [200.5, 1.45, 2.0], [200.55, 1.3, -1.2], 46, 'whip', .32, { creep: .3, drift: .04 });
  key(Le('L14') + .2, [200.3, 1.42, 1.0], [200.25, 1.36, -1.0], 38, 'glide', 1.8, { creep: .2, drift: .02 });
  return new CamPath(k, { fps: FPS });
}

// ---------------------------------------------------------------- kurulum
export async function setup(ctx) {
  C = ctx; WORDS = ctx.words; LINES = ctx.lines;
  DUR = +(LINES[LINES.length - 1].end + 1.2 + END).toFixed(2);
  const scene = ctx.scene; scene.background = new THREE.Color('#15142a');
  try { await document.fonts.load('600 40px Poppins'); await document.fonts.load('800 40px Poppins'); } catch (e) { /* yedek yazı tipi */ }
  sets.yo = yatakOdasi(scene); sets.an = antre(scene); sets.sp = salonPencere(scene);
  cast.ayca = new Toon(LOOK.ayca, scene); cast.nihat = new Toon(LOOK.nihat, scene);
  cast.aycaAyakta = new Toon({ ...LOOK.ayca, cloth: '#d6c2e6', clothDark: '#a28ab8', buttons: false }, scene);    // sabah: sabahlık
  cast.nihatAyakta = new Toon({ ...LOOK.nihat }, scene);
  dyn.cam = cameraPath();
  dyn.hand = new Arm3D(scene, cast.ayca);
  // telefon ekranı canvas'ını ilk hâliyle çiz
  phoneScreen(sets.yo.sc, { bildirim: 0 }); sets.yo.scTex.needsUpdate = true;
  // ses ipuçları (dizi/tools/dizi_mix.py okur)
  const cue = (t, type, extra = {}) => CUES.push({ t: +t.toFixed(3), type, ...extra });
  cue(0, 'gece', { dur: Lb('L12') - .2 });
  cue(Lb('L02') - .05, 'titresim', { dur: 1.1 }); cue(Lb('L05') + .6, 'titresim', { dur: .7 });
  cue(Lb('L03') - .07, 'whoosh'); cue(Lb('L06') - .05, 'bildirim'); cue(Lb('L08') - .08, 'kalp', { dur: 2.2 });
  cue(Lb('L09') - .22, 'klik'); cue(Lb('L11') + .3, 'klik');
  cue(Lb('L12') - .3, 'whoosh'); cue(Lb('L12') - .1, 'sabah', { dur: Lb('L14') - Lb('L12') });
  cue(Wd('L12', 6) - .1, 'kumas'); cue(Lb('L13') + .9, 'kapi'); cue(Le('L13') + .25, 'kapi_kapan');
  cue(Lb('L14') - .2, 'whoosh'); cue(Le('L14') + .3, 'vurgu'); cue(DUR - END, 'son', { dur: END });
}

// ---------------------------------------------------------------- her kare
const NIGHT = '#cdd2f4', DAY = '#ece8f6', WARM = '#ffb86a', COOL = '#a9c4ff';
const GRADE = { yo: [.96, .97, 1.06], an: [1.03, 1.0, .95], sp: [1, 1, 1.02] };
const FACE = { yo: [.95, .96, 1], an: [1, .99, .97], sp: [.99, 1, 1] };
export function frame(t, ctx) {
  const { cam, env } = ctx;
  const cp = dyn.cam.apply(cam, t);
  const x = cam.position.x, where = x < 50 ? 'yo' : x < 150 ? 'an' : 'sp';
  for (const k of ['yo', 'an', 'sp']) { sets[k].g.visible = k === where; sets[k].L.visible = k === where; }
  for (const c of Object.values(cast)) c.hide();
  dyn.hand.hide(); sets.yo.handPhone.visible = false;
  const tint = FACE[where].map((v, i) => v / GRADE[where][i]);
  const A = id => Lb(id) - 2 / FPS;                                            // oyunculuk sözcükten iki kare önce
  const talking = id => t > Lb(id) - .02 && t < Le(id) + .05;
  const bl = (seed, ...sw) => blinkAt(t, seed, sw, FPS);
  let look;

  if (where === 'yo') {
    const Y = sets.yo;
    // ---- telefon: titreşim (L02 ve L05 sonu), kenarlardan sızan ışık, ekran ışığı
    const buzz = (t > Lb('L02') && t < Lb('L02') + 1.1) || (t > Lb('L05') + .6 && t < Lb('L05') + 1.3);
    Y.phone.position.set(YO.phone.x + (buzz ? Math.sin(t * 160) * .004 : 0), YO.phone.y, YO.phone.z + (buzz ? Math.cos(t * 130) * .003 : 0));
    Y.phone.rotation.y = buzz ? Math.sin(t * 90) * .05 : 0;
    const lit = buzz ? 1 : 0;
    Y.leak.material.opacity = .6 * lit; Y.phoneLight.intensity = .7 * lit;
    // ---- saat
    const ck = t < Lb('L11') ? '02:14' : '02:16';
    if (dyn.ck !== ck) { dyn.ck = ck; clockFace(Y.cc, ck); Y.ccTex.needsUpdate = true; }
    // ---- Nihat'ın lambası: uyanınca yanar, Ayça "yalan söyledim" derken söner
    const lampOn = ramp(t, A('L09') - .2, A('L09') - .12) * (1 - ramp(t, Lb('L11') + .3, Lb('L11') + .38));
    Y.lampN.set(lampOn); Y.lampA.set(0);
    // ---- elde telefon (L06-L07): Ayça'nın eli telefonu kaldırır, ekran yanar, bildirim düşer
    const inHand = t > Lb('L06') - .1 && t < Lb('L08') - .1;
    if (inHand) {
      Y.handPhone.visible = true; Y.phone.visible = false;
      const up = ramp(t, Lb('L06') - .1, Lb('L06') + .5);
      const P = V(YO.phone.x + .48, lerp(.6, .86, up), YO.phone.z + .38);
      Y.handPhone.position.copy(P); Y.handPhone.rotation.set(lerp(-1.4, -.18, up), .55, 0);
      const bil = ramp(t, Wd('L06', 6) - .15, Wd('L06', 6) + .2), vurgu = ramp(t, Lb('L07'), Lb('L07') + .4);
      const key = `${bil.toFixed(2)}|${vurgu.toFixed(2)}`;
      if (dyn.scKey !== key) { dyn.scKey = key; phoneScreen(Y.sc, { bildirim: bil, vurgu }); Y.scTex.needsUpdate = true; }
      Y.screen.material.color.setScalar(lerp(.2, .98, ramp(t, Lb('L06') + .2, Lb('L06') + .6)));
      Y.phoneLight.intensity = 0;
      // el: kadrajın sağ altından gelen mor kol (Ayça'nın)
      const hand = Y.handPhone.localToWorld(V(.03, -.07, .012));
      dyn.hand.toon = { shoulder: () => V(P.x + .5, P.y - .45, P.z + .35), mesh: { rotation: { y: 0 } } };
      dyn.hand.set(1, hand, { sag: .03, tint: [.9, .9, 1] });
    } else Y.phone.visible = true;
    // ---- kişiler
    const nihatUp = ramp(t, A('L09') - .25, A('L09') + .1) * (1 - ramp(t, Lb('L11') + .2, Lb('L11') + .7));
    const aycaUp = ramp(t, A('L10') - .2, A('L10') + .25) * (1 - ramp(t, Lb('L11') + .5, Lb('L11') + 1.1));
    // yastıktaki kafa: kart gövdesi yorganın arkasında kalacak kadar aşağıda
    const headDrop = (L) => YO.headY - (L.height || 1.72) * (800 / 916);
    cast.nihat.show(); cast.nihat.place(YO.nihatX + nihatUp * .04, headDrop(LOOK.nihat) + nihatUp * .2, YO.pillowZ + .06, cam, tint);
    cast.ayca.show(); cast.ayca.place(YO.aycaX, headDrop(LOOK.ayca) + aycaUp * .26, YO.pillowZ + .08, cam, tint);
    const phoneOnFace = inHand || (t > Lb('L08') - .1 && t < Lb('L09') - .3);
    const rimA = lampOn > .5 ? { color: WARM, a: .4 * lampOn } : phoneOnFace ? { color: COOL, a: .55 } : { color: '#8fa4ff', a: .25 };
    const shock = t > A('L08') && t < A('L09');
    const lie = t > A('L11') + .5;
    let aExpr = 'neutral', aLid = .35, aLook = -.35, aBrow = 0;
    if (t < Lb('L04')) { aExpr = 'neutral'; aLid = .45; aLook = -.6; }                               // uyuyor numarası: göz aralık
    else if (t < A('L08')) { aExpr = 'focused'; aLid = .1; aLook = -.7; }
    else if (shock) { aExpr = t < A('L08') + .45 ? 'surprised' : 'worried'; aLook = -.2; }
    else if (t < A('L11')) { aExpr = t < A('L10') ? 'worried' : 'smile'; aLook = -.75; aBrow = .4; }
    else { aExpr = t < Wd('L11', 2) ? 'worried' : 'focused'; aLook = .15; aLid = .1; }
    cast.ayca.draw({ expr: aExpr, lid: aLid, look: aLook, lookY: -.1, brow: aBrow, gazeX: aLook * 1.2,
      blink: t < Lb('L04') ? 0 : bl(3, A('L08'), A('L10'), A('L11')), mouth: talking('L10') ? flap(env, t) : 0,
      tilt: lerp(-10, -2, aycaUp), armL: [10, 4], armR: [10, 4], lit: lampOn > .5 ? -1 : 1, shade: NIGHT, rim: rimA, sweat: shock && t > A('L08') + .5 ? 1 : 0 });
    const nAwake = t > A('L09') - .2 && t < Lb('L11') + .3;
    cast.nihat.draw({ expr: nAwake ? 'neutral' : 'neutral', lid: nAwake ? .5 : 0, blink: nAwake ? bl(5) : 1, look: nAwake ? .55 : .2, lookY: -.05,
      mouth: talking('L09') ? flap(env, t) : 0, tilt: lerp(12, 4, nihatUp), lit: -1, shade: NIGHT, rim: lampOn > .5 ? { color: WARM, a: .45 * lampOn } : { color: '#8fa4ff', a: .2 } });
    cast.nihat.castFrom(lampOn > .5 ? V(-1.42, 1.0, -2.2) : V(4.2, 4.4, -5.5)); cast.ayca.castFrom(lampOn > .5 ? V(-1.42, 1.0, -2.2) : V(4.2, 4.4, -5.5));
    // ---- lens
    const f = p => cam.position.distanceTo(p);
    if (t < Lb('L02')) look = { focus: f(YO.clock), coc: 9, range: .25 };
    else if (t < Lb('L03')) look = { focus: f(YO.phone), coc: 9, range: .3 };
    else if (t < Lb('L04') - .1) look = { focus: f(V(YO.aycaX, .9, YO.pillowZ)), coc: 8, range: .35 };
    else if (t < Lb('L05')) look = { focus: f(V(0, .9, -2.0)), coc: 3, range: 2.5 };
    else if (t < Lb('L06')) look = { focus: f(YO.phone), coc: 6, range: .6 };
    else if (inHand) look = { focus: f(sets.yo.handPhone.position), coc: 10, range: .15 };
    else if (t < Lb('L09') - .25) look = { focus: f(V(YO.aycaX, .9, YO.pillowZ)), coc: 9, range: .3 };
    else if (t < Lb('L11') - .1) look = { focus: f(V(0, .95, -2.0)), coc: 5, range: 1.0 };
    else look = { focus: f(V(YO.aycaX, .95, YO.pillowZ)), coc: 8, range: .35 };
    Object.assign(look, { sat: 1.12, lift: [.075, .07, .15], bloom: .95, vignette: .34, contrast: 1.08 });
  } else if (where === 'an') {
    const Nn = cast.nihatAyakta, Aa = cast.aycaAyakta;
    // gömlek iki kez değişir: beyaz -> açık mavi -> bordo (her değişimde hızlı bir sıçrama)
    const c1 = Wd('L12', 6) - .15, c2 = Wd('L12', 8);
    const shirt = t < c1 ? ['#e8eef6', '#b8c2d8'] : t < c2 ? ['#8fb6e0', '#5a82b0'] : [LOOK.nihat.cloth, LOOK.nihat.clothDark];
    Nn.look.cloth = shirt[0]; Nn.look.clothDark = shirt[1]; Nn.key = '';
    const atDoor = t > A('L13') - .2;
    const walk = ramp(t, A('L13') - .5, A('L13') + .3);
    const nx = lerp(AN.mirror.x + .05, 100.45, walk), nz = lerp(-1.75, -1.85, walk);
    const pop = (tc) => t > tc && t < tc + .18 ? Math.sin((t - tc) / .18 * Math.PI) * 6 : 0;
    Nn.show(); Nn.place(nx, 0, nz, cam, tint);
    const fixing = !atDoor && t > Lb('L12');
    Nn.draw({ expr: atDoor ? 'smug' : (t < c2 ? 'focused' : 'proud'), look: atDoor ? .6 : -.55, lookY: atDoor ? 0 : -.2, blink: bl(7, c1, c2, A('L13')),
      mouth: talking('L13') ? flap(env, t) : 0, armL: fixing ? [150 + Math.sin(t * 9) * 8, 70] : [18, 30], armR: atDoor ? [55, 40] : fixing ? [140, 80] : [14, 8],
      propR: atDoor ? 'keys' : undefined, bob: pop(c1) + pop(c2), lean: atDoor ? -2 : 0, lit: 1, shade: DAY, rim: { color: '#ffd59a', a: .4 } });
    Nn.castFrom(V(107, 3.2, .6));
    Aa.show(); Aa.place(100.38, 0, -.25, cam, tint);
    Aa.draw({ expr: atDoor ? 'neutral' : 'focused', look: -.85, lid: .15, blink: bl(8, A('L13')), armR: [40, 95], propR: 'tea', armL: [20, 30], lit: 1, shade: DAY, rim: { color: '#ffd59a', a: .5 } });
    Aa.castFrom(V(107, 3.2, .6));
    // kapı açılır, merdiven ışığı girer; söz bitince kapanır
    const open = ramp(t, Lb('L13') + .8, Lb('L13') + 1.4) * (1 - ramp(t, Le('L13') + .15, Le('L13') + .45));
    sets.an.pivot.rotation.y = open * 1.4; sets.an.doorLight.intensity = 2.2 * open;
    const f = p => cam.position.distanceTo(p);
    look = { focus: f(V(nx, 1.3, nz)), coc: 5, range: 1.2, sat: 1.18, lift: [.09, .085, .12], bloom: .8, vignette: .22, contrast: 1.06 };
  } else {
    const Aa = cast.aycaAyakta;
    Aa.show(); Aa.place(SP.aycaPos.x, 0, SP.aycaPos.z, cam, tint);
    const last = t > Le('L14') - .1;
    Aa.draw({ expr: last ? 'focused' : 'worried', look: .75, lookY: -.05, lid: last ? .2 : 0, brow: last ? -.2 : .3, gazeX: 1.2, blink: bl(9, Le('L14') - .1),
      armR: [40, 95], propR: 'tea', armL: [18, 20], lit: 1, shade: DAY, rim: { color: '#dfe8ff', a: .5 } });
    Aa.castFrom(V(203.6, 3.6, -6.5));
    const f = p => cam.position.distanceTo(p);
    look = { focus: f(V(SP.aycaPos.x, 1.35, SP.aycaPos.z)), coc: 6, range: .8, sat: 1.05, lift: [.085, .085, .13], bloom: .8, vignette: .3, contrast: 1.07 };
  }
  look.tint = GRADE[where];
  look.blur = cp.moving > .15 ? 16 : 0;
  look.flash = (where === 'an' && [Wd('L12', 6) - .15, Wd('L12', 8)].some(tc => t >= tc && t < tc + 2 / FPS)) ? .25 : 0;
  look.captions = t < DUR - END;
  return look;
}

// ---------------------------------------------------------------- yazı katmanı: dizi adı (açılış), son kart
export function overlay(g, t, ctx) {
  const W = ctx.W, H = ctx.H, k = W / 1080;
  // açılış: üstte küçük dizi künyesi (ilk 3.2 sn)
  const a = Math.min(1, t / .25) * (1 - ramp(t, 2.8, 3.3));
  if (a > 0) {
    g.save(); g.globalAlpha = a; g.textAlign = 'center';
    g.font = `800 ${46 * k}px Poppins, sans-serif`; g.fillStyle = '#ffd27a'; g.shadowColor = 'rgba(10,6,20,.7)'; g.shadowBlur = 18 * k;
    g.fillText('ÇAPKIN NİHAT', W / 2, H * .085);
    g.font = `600 ${28 * k}px Poppins, sans-serif`; g.fillStyle = '#ffffff'; g.fillText(`${BOLUM.no}. BÖLÜM · ${BOLUM.ad.toLocaleUpperCase('tr-TR')}`, W / 2, H * .085 + 44 * k);
    g.restore();
  }
  // son kart
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
