# Çizgiden Dizi · Çapkın Nihat — dizi kitabı ve üretim kuralları

Kanal: @cizgidendizi.tr (Instagram, eski @copadamlatarih). Her akşam **20.00**'de bir bölüm (kanal/slotlar.txt).
İlham: sabit karakterli, duygusal, bölüm bölüm ilerleyen dikey çizgi diziler (örnek hesaplar @cizgihayat.tr, @ciraktanpatrona —
yalnızca yapı dersi; hikâye, karakter, metin ASLA kopyalanmaz). Görsel motor: yumurta-stili (MIT, dizi/engine).

## Hikâye
Ayça (34) ile Nihat (38) on iki yıllık evli. Ayça kocasının onu aldattığından şüpheleniyor; her bölüm bir ipucu bulur.
Nihat gerçekten çapkın ama ustaca yalan söyler. Her bölüm "acaba mı?" duygusuyla, bir sonrakini bekletecek bir merakla biter.
Anlatım: **Ayça'nın iç sesi** (sakin, alçak, düşünür gibi). Yüksek sesle söylenen satırlar ayrı (karakterin ağzı oynar).
Ton: gerilim + hüzün + ara ara ince ironi. Müstehcenlik, şiddet, küfür YOK; aldatma ima edilir, gösterilmez.

### Kadro (dizi/lib/kadro.js — görünüşler sabit, id'ler değişmez)
- **ayca**: uzun kestane saç, yeşil hırka (evde) / leylak sabahlık (sabah); dikkatli, sessiz, zeki.
- **nihat**: jöleli geriye taranmış siyah saç, bordo gömlek, altın zincir; kendinden emin, "smug".
- Yeni karakter gerekirse kadro.js'e ekle (id ver, saç stili: long | bob | slick | short). Öneriler:
  **selin** (alt kat komşusu, kısa sarı bob saç, kırmızı elbise, kokusu vanilya), **derya** (Ayça'nın en yakın arkadaşı, kıvırcık
  koyu saç → 'bob' + koyu renk, sarı kazak), **kaan** (gerçekten var mı? hiç yüzü gösterilmez).

### 1. sezon iskeleti (yazarken buna sadık kal, ayrıntıyı sen kur)
| Bölüm | Ad | İpucu / olay | Son merak |
|---|---|---|---|
| D01 | Gece 02.14 | "Bizim Takımdaki Kaan": "Yarın aynı yerde mi?" Nihat futbol oynamaz. | "Aynı yer neresiydi, Nihat?" |
| D02 | Halı Saha Çantası | Nihat akşam "maça" gider; çantadaki kramponların etiketi hâlâ üstünde, hiç giyilmemiş. Ayça "Kaan"ı arar. | Telefonu bir KADIN açar: "Alo?" |
| D03 | Vanilya | Gömlekte vanilya kokusu, yakada uzun SARI saç teli. Nihat: "Asansörde biri sürtündü." | Aynı koku apartman merdiveninde… |
| D04 | Konum | Ayça konum paylaşımını açar; Nihat'ın noktası ofiste değil, sahilde bir kafede. | Ayça kafeye varır: Nihat'ın arabası orada, yanında kırmızı bir palto… |
| D05 | İki Tiramisu | Ceketten iki kişilik restoran fişi (Salı 21.40). Nihat tatlı sevmez. | Fişin arkasında bir telefon numarası. |
| D06 | Mesai | Ayça ofisi arar: "Nihat Bey bugün izinli." | Akşam Nihat "çok yoruldum" diye eve gelir. |
| D07 | Altın Bilezik | Nihat'ın cebinde kuyumcu kutusu; Ayça yıldönümü sanır. Yıldönümünde Nihat ona bir eşarp verir. | Bilezik kimin? |
| D08 | Asansör | Komşu Selin asansörde; bileğinde O bilezik. | Selin gülümser: "Nihat Bey çok kibar biri." |
| D09 | Stepne | Arabanın stepne yuvasında ikinci telefon. | Ekranda: "Kaan ❤️ – 3 cevapsız arama" |
| D10 | Ayça Cevap Verir | İkinci telefon çalar, Ayça açar, susar. | Karşıdaki ses: "Nihat? Karın biliyor mu?" |
| D11 | Derya | Ayça her şeyi Derya'ya anlatır; Derya'nın tepkisi tuhaf. | Derya'nın telefonunda da "Kaan" diye bir kayıt… |
| D12 | Sezon finali: Aynı Yer | Ayça "aynı yere" gider. | Kapıyı açan kişi… (2. sezon) |

## Bölüm üretim kuralları
Klasör: `dizi/stories/Dxx/` (D01 örnek: story.js, voice/satirlar.json, bolum.json, SCRIPT.md).
- **Süre** 40-55 sn, **12-16 satır**, Türkçe ~1.8-2.2 kelime/sn (sakin anlatım). `ara` değerleri 0.3-0.8 sn.
- **Kanca**: ilk 5 sn'de üç-dört görüntü, ilk cümlenin her parçasına bir resim; ilk karede karakter hikâyenin nesnesiyle bir şey yapıyor.
- **Son satır** her zaman cevapsız bir soru/merak (Ayça'nın iç sesi). Son kart: `BOLUM.soru` (izleyiciye soru) + "N. BÖLÜM YARIN 20.00".
- Satırlar `voice/satirlar.json`: `kim` = `ic` (iç ses) | `ayca` | `nihat` | (yeni karakter için `sesler`'e ekle: kadın sesleri Kore/Leda/Aoede/
  Despina, erkek Charon/Orus/Puck; Ayça HEP Vindemiatrix, Nihat HEP Algenib). Sayıları yazıyla yaz ("iki on dört").
- `bolum.json`: id, title ("Çapkın Nihat · N. Bölüm · Ad"), caption (2-3 kısa satır merak + "Sence …? Yorumlara yaz 👇" +
  "Çapkın Nihat · Her akşam 20.00'de yeni bölüm, tüm bölümler profilde."), hashtags TAM 5: #çapkınnihat #dizi #animasyon + 1 konuya
  uygun + #keşfet. Müzik kredisini YAZMA (paylaşımda otomatik eklenir).
- `story.js`: D01'i kopyala, `BOLUM` (no, ad, soru, sonraki) ve kamera/oyunculuğu yeniden yaz. Zamanlar SADECE satır saatlerinden:
  `Lb('L05')`, `Le('L05')`, `Wd('L05', n)`. İç ses satırlarında ağız OYNAMAZ; konuşanın ağzı `flap(env, t)` ile ve yalnız kendi satırında.
- Setler `dizi/lib/ev.js`: yatakOdasi (x≈0, gece), antre (x≈100, sabah), salonPencere (x≈200, sabah). Yeni set gerekirse (mutfak, araba
  içi, apartman merdiveni/asansör, kafe, sahil) ev.js'e x≈300, 400… ekle. Kurallar: görünen BİR ana ışık, sıcak-soğuk karşıtlığı,
  gerçek gölgeler (`shadows(g)`), büyük duvarda desen, hiçbir yüzey başka yüzeyle aynı düzlemde değil, saf siyah yok.
- **Kadraj**: yüzler kadrajın %35-60 yüksekliğinde; yumurta kafalar büyük (~0.5 m) — yakın plan için kamera kafadan ≥2 m uzakta, fov 34-40.
  Uzun tutuşlarda `creep` ≤ .12 (yoksa yüz kadrajı doldurur). Kamera hiç durmaz; bölümde en fazla 2 sert kesme.
- Karakterleri ve yeni setleri kontrol et: `cd dizi/engine && npm ci --silent` (ilk sefer), yerel deneme sesi
  `TTS_ENGINE=sessiz python3 dizi/tools/ses_uret.py dizi/stories/Dxx` (bu dosyaları COMMIT ETME), sonra
  `node render.mjs Dxx --stills=<her satırdan bir saniye> --scale=0.5 --cols=5` ve `stories/Dxx/out/stills.jpg`'ye BAK:
  kesilen yüz, kadraj dışı karakter, karanlık/boş kare, yazının yüzü örtmesi, elinde olmayan nesne. Düzelt, tekrar bak.
- Bitince: deneme ses dosyalarını sil (`voice/voice.wav`, `words.json`, `env.json`, `satir/`), yalnız satirlar.json, story.js,
  bolum.json, SCRIPT.md (+ ev.js/kadro.js değiştiyse) commit + push. Sonra **Dizi sesi** iş akışını başlat:
  `gh api -X POST repos/blackwolf0133/cop-adamla-tarih/actions/workflows/dizi-ses.yml/dispatches -f ref=main -f 'inputs[bolum]=Dxx'`
  (ses bitince render kendiliğinden başlar, ~40 dk; sonuç `dizi-Dxx` sürümünde). Paylaşım 20.00'de otomatik.
