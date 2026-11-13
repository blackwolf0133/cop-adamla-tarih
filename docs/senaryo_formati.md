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

## Anlatım tonu: "karışık" (Kasım 2026'dan itibaren)
Örnek alınan tarz: merak uyandıran, akıcı belgesel anlatımı + yer yer hafif espri.
- **Kanca (ilk cümle):** Şaşırtıcı, neredeyse inanılmaz bir iddia. "Dur!" yerine doğrudan iddiayla da açılabilir: "100 koyunu ölüme götürmek için bir kurda değil, bir keçiye ihtiyacın var."
- **Akış:** Kısa, net cümleler; sahneler arası duraksama az. Hedef ~170-180 kelime/dk, toplam 45-60 sn.
- **Dönüm noktası:** Ortada merakı tazeleyen bir soru: "İşin en ilginç kısmı ne biliyor musun?"
- **Espri:** Her bölümde 1-2 hafif espri yeter (abartı yok); görsel şakalar (pop yazıları) devam.
- **Kapanış dersi:** Düşündüren, akılda kalan tek cümle ("Günün dersi: ..."). Ardından kısa takip çağrısı.
- **Duygu (isteğe bağlı):** Sahneye `"emotion"` eklenebilir: `mutlu` `şaşkın` `sakin` `üzgün` `kızgın` (kendi sesinle okurken tonlamayı etkiler). Çoğu sahnede boş bırak; kanca ve dönüm noktasında `şaşkın`, dersde `sakin` iyi gider.

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

## Haftalık trend raporu (last30days)
Her pazartesi blackwolf0133/cop-adamla-tarih deposundaki "Trend araştırma" iş akışı son 30 günün trendlerini 6 kanal için tarar
(YouTube, Reddit vb.; SCRAPECREATORS anahtarı varsa Instagram ve TikTok da). Yeni bölüm yazmadan önce en yeni raporu oku:

```bash
TAG=$(gh api "repos/blackwolf0133/cop-adamla-tarih/releases?per_page=20" --jq '[.[]|select(.tag_name|startswith("trend-"))][0].tag_name')
ID=$(gh api "repos/blackwolf0133/cop-adamla-tarih/releases/tags/$TAG" --jq '.assets[]|select(.name=="cop.md").id')
gh api -H "Accept: application/octet-stream" "repos/blackwolf0133/cop-adamla-tarih/releases/assets/$ID" > /tmp/trend.md
```
Bu kanalın dosyası: **cop.md**. Rapordaki tutan kanca kalıplarını, konu açılarını ve formatları kendi kurallarımıza uyarlayarak kullan;
başka içerik üreticilerinin metnini, videosunu ya da hikâyesini kopyalama. Rapor yoksa ya da eskiyse (14 günden eski) bu adımı atla.

---

## 13 Kasım: İLK 3 SANİYE kuralları (ZORUNLU, diğer kurallarla çelişirse bu geçerli)

Veri: 8 kanalda izleyici ortalama 5-13 sn'de kaydırıyor. Instagram videoyu önce küçük bir test grubuna gösteriyor; izlenme süresi, sona kadar izlenme ve DM ile gönderilme iyi değilse yaymıyor. Reels izleyicisi ~1,4 sn'de karar veriyor ve izlemelerin yarısından fazlası ses kapalı başlıyor.

**Motor ne yapıyor (otomatik):** 0. saniyede ekranda büyük kanca yazısı (~3 sn) + ilk 0,8 sn hızlı zoom. Yazı bölümdeki `"kanca_yazi"` alanından gelir; yoksa açıklamanın (caption / instagram_caption) ilk satırından, o da uzunsa ilk cümlesinden. Bu yüzden:
- Her bölüme `"kanca_yazi"` ekle: en fazla 8 kelime, sessizken tek başına merak uyandıran cümle (cevabı vermeden). Seslendirilen ilk cümleyle aynı olmak zorunda değil ama aynı merakı açsın. (Son Mola'da bu alan sahne içindedir ve 2-3 kelimedir; orada mevcut kural geçerli.)
- Açıklamanın ilk satırı da kısa ve merak uyandıran olsun (yedek kanca yazısı olarak kullanılıyor).

**Kanca puanlama (yazdıktan sonra her bölüm için):** İlk seslendirilen cümleyi ve kanca_yazi'yi şu 5 türe göre 1-5 puanla, kendine sor: "Akışta kaydırırken 1,5 sn'de durur muydum?"
1. Ortak dert: izleyicinin yaşadığı ama dile getirmediği bir sıkıntı (Reels'te en güçlüsü)
2. Merak boşluğu: kapanması için izlemek gereken bir soru/boşluk
3. İddialı/ters köşe cümle: doğru ama şaşırtıcı, karşı çıkılası bir iddia
4. Kalıp kırma: beklenmedik bir giriş
5. Görsel şok: ilk karede açıklama isteyen bir görüntü
En yüksek puan 4'ün altındaysa ilk cümleyi yeniden yaz. Selamlama, giriş, "bugün size … anlatacağım", tarih/yer ile başlamak YASAK; en çarpıcı an ilk cümlede. Doğruluk kuralları aynen geçerli (abartı/uydurma yok).

**Gönderilme (DM) sebebi:** Instagram'da yeni kişilere ulaştıran en güçlü sinyal videonun DM ile birine gönderilmesi. Her bölümün SON seslendirilen cümlesi (ya da kapanış kartı alt yazısı), izleyicinin videoyu belirli birine göndermesi için doğal bir sebep versin; TEK cümle, dilenmeden: "Bunu her ay sonu batan arkadaşına gönder.", "Bunu gece yolculuğu seven birine gönder." Açıklamadaki tek çağrı kuralı aynen kalır (bu cümle videonun içinde).
