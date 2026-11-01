# Bölüm Senaryo Formatı

Her bölüm `episodes/NNN_kisa_ad.json` dosyasıdır. Program sıradaki (paylaşılmamış, en küçük numaralı) bölümü alır.

## Üst alanlar
| Alan | Açıklama |
|---|---|
| `id` | "009" gibi 3 haneli numara (dosya adıyla aynı) |
| `series` | "ÇÖP ADAMLA TARİH" |
| `title` | Dikkat çekici başlık (video üstünde yazar) |
| `year` | Panelin köşesindeki etiket: "1453", "MÖ 2560", "1630'LAR" |
| `voice_fx` | `{"pitch": 1.15, "noise": 0.2, "noise_w": 0.3}` (sabit tonlu karikatür ses) |
| `instagram_caption` | Paylaşım yazısı. **En fazla 5 etiket** (Instagram sınırı), sonuncusu `#çöpadamlatarih` |
| `skip` | `true` ise bölüm atlanır |

## Sahne yapısı (8-10 sahne, toplam 45-60 sn)
1. **Giriş**: Tarih Hoca (`narrator`) – "Dur!" kancası + şaşırtıcı soru
2. **Hikâye**: 5-7 sahne, her biri 1-2 cümle
3. **Ders**: "Günün dersi: ..." espri ile (`{"type":"sfx","name":"rimshot","f":0.75}`)
4. **Kapanış**: Tarih Hoca – takip et çağrısı

### Sahne alanları
- `say`: Seslendirilecek metin. Sayılar rakamla yazılabilir; yıllar ("1453", "1071'de") otomatik "bin dört yüz elli üç" diye net okunur.
- `text`: Altyazı (rakamlı hali). Boşsa `say` kullanılır.
- `bg`: `plain` `sea` `hill` `desert` `farm` `city` (İstanbul) `battlefield` `palace` · `night: true` gece
- `voice_delay`: konuşma başlamadan önce bekleme (giriş sahnesi 1.0)

### Karakter (`actors`)
`{"id","x","y","scale","hat","pose","face","anim","flip","talk","holds","wings","enter","pose2","face2","switch","to_x","to_y","arc","move_dur","stand_on"}`
- **hat**: `sarik` (Osmanlı) `kavuk` (padişah) `bork` (yeniçeri) `selcuk` `crown` (Bizans/kral) `helmet` (Bizans askeri) `greek` (antik Yunan) `nemes` (firavun) `bicorne` (Napolyon) `tophat` `slouch` (Avustralya/kaşif) `fez` (yalnızca 1829 sonrası!)
- **pose**: `stand` `point` `hips` `relax` `shock` `think` `push` `cheer` `sad` `stretch` `shrug` `open` `open_arms`
- **face**: `neutral` `happy` `confident` `shock` `smug` `think` `sad` `effort` `sleepy` `surprised`
- **anim**: `idle` `bounce` `shake` `walk`
- **holds**: `sword` `mug` `cup` `scroll` `torch`
- Hareket: `to_x` / `to_y` (+ `arc` yükseklik) sahne boyunca kayar; `stand_on: "wall"` surun üstüne koyar
- Zemin y: plain/city/palace 0.93 · desert/farm/battlefield 0.90 · hill otomatik

### Nesneler (`props`)
`ship` `chain` `wall` `pyramid`(progress/build) `block` `palm` `horse`(anim gallop) `trojan`(open) `tower`(Galata) `emu`(anim run) `tent` `cezve` `ban`(yasak işareti) `ruler`(labels) `fence` `sign`(text) `coins` `sun`
Efekt/yazı: `pop` (çizgi roman yazısı) `bubble` (konuşma balonu) `bulb` (fikir ampulü, `actor`) `flag` (`actor`, `emblem`) `label` `sfx` (assets/audio/<name>.mp3)
Zamanlama: `delay` (sn) ya da `f` (konuşmanın oranı 0-1); `until`/`until_f` ile kaybolur.

## Doğruluk kuralları
- Efsane/tek kaynaklı hikâyelerde bunu söyle ("Efsaneye göre", "Evliya Çelebi'ye göre").
- Kıyafet/eşya döneme uygun olsun (fes 1829 öncesi yok, ay-yıldızlı bayrak Selçuklu'da yok).
- Şiddet sahnesi çizme; savaşlar şaka, şaşkınlık ve kaçışla anlatılır.
