# Çöp Adamla Tarih 🎬

Her gün saat **19:00**'da (Türkiye) yeni bir tarih bölümünü çöp adam çizimli, esprili bir Reels videosu olarak üretip Instagram'a **otomatik** paylaşan sistem. Tamamen ücretsiz araçlarla çalışır.

```
episodes/*.json  ──►  GitHub Actions (her gün 18:47)  ──►  video üret  ──►  GitHub Pages  ──►  Instagram Reels
 (senaryolar)          ücretsiz sunucu                     çizim+ses+altyazı   (geçici adres)      (resmi Meta API)
```

## Klasörler
| Yol | Ne işe yarar |
|---|---|
| `episodes/` | Bölüm senaryoları. Sıradaki (paylaşılmamış, en küçük numara) her gün paylaşılır |
| `engine/` | Çizim ve video motoru (çöp adamlar, aksesuarlar, ses, altyazı) |
| `daily.py` | Günlük akış: `status`, `render`, `publish`, `check`, `refresh-token` |
| `publisher.py` | Instagram paylaşım modülü |
| `state/posted.json` | Paylaşılan bölümlerin kaydı (otomatik güncellenir) |
| `assets/audio/` | (İsteğe bağlı) telifsiz müzik ve efektler: `music.mp3`, `boing.mp3`, `rimshot.mp3`, `pop.mp3`, `ding.mp3`, `whoosh.mp3` |
| `docs/` | Konu takvimi ve senaryo format rehberi |
| `.github/workflows/` | Günlük paylaşım + haftalık token yenileme |

---

## Kurulum (bir kerelik, ~20 dakika)

### 1) Instagram hesabını profesyonele çevir
Instagram → Ayarlar → **Hesap türü ve araçlar** → **Profesyonel hesaba geç** → *İçerik Üreticisi* veya *İşletme*.
> Yayın reddedilirse hesabı *İşletme* türüne çevirmek çözüm olabilir.

### 2) Meta geliştirici uygulaması aç (ücretsiz)
1. https://developers.facebook.com → **Uygulamalarım → Uygulama oluştur**
2. Kullanım durumu: **"Instagram'da mesajlaşmayı ve içeriği yönet"** (Manage messaging & content on Instagram)
3. Sol menü → **Instagram → API setup with Instagram login**
4. **İzinler:** `instagram_business_basic` ve `instagram_business_content_publish` ekli olsun
5. **Hesabı uygulamaya tanıt:** Uygulama rolleri → Roller → *Instagram testers* → kullanıcı adını davet et → Instagram'da *Ayarlar → Uygulamalar ve web siteleri → Test davetleri*'nden kabul et
6. **Generate access tokens** → *Add account* → hesabınla giriş yap → **Generate token** → tokenı hemen kopyala (bir kez gösterilir, 60 gün geçerli)

> Kendi hesabına paylaşım için **uygulama incelemesi (App Review) gerekmez** (Standard Access).

### 3) GitHub deposu
1. https://github.com → yeni depo: `cop-adamla-tarih`, **Public** (ücretsiz sınırsız çalışma süresi ve GitHub Pages için)
2. Bu klasördeki tüm dosyaları yükle (`.github` klasörü dahil!)
3. **Settings → Pages → Source: GitHub Actions**
4. **Settings → Secrets and variables → Actions → New repository secret**:
   - `IG_ACCESS_TOKEN` = 2. adımdaki token
   - `IG_USER_ID` = (isteğe bağlı) boş bırakırsan tokendan otomatik bulunur
   - `GH_PAT` = (isteğe bağlı) tokenın her hafta otomatik yenilenip kaydedilmesi için; *Settings → Developer settings → Fine-grained tokens* → bu depo için **Secrets: Read and write** izni

### 4) Dene
1. **Actions → Günlük paylaşım → Run workflow** → ✅ *Sadece videoyu üret* → çalıştır
2. Bitince sayfanın altındaki **Artifacts**'tan videoyu indirip izle
3. Her şey yolundaysa aynı işi kutuyu işaretlemeden çalıştır → ilk Reel paylaşılır 🎉

Bundan sonra her gün 19:00 civarında kendiliğinden paylaşır. (GitHub zamanlanmış işleri bazen 5-15 dk geciktirebilir.)

---

## Günlük kullanım
- **Sırada ne var?** Actions çıktısındaki "Sıra durumu" adımına bak. Sırada 4'ten az bölüm kalınca uyarı verir.
- **Yeni bölüm eklemek:** `episodes/` klasörüne `009_...json` gibi yeni dosya ekle (format: `docs/senaryo_formati.md`). Yeni senaryoları Claude yazar.
- **Bir bölümü atlamak:** dosyada `"skip": true`
- **Saati değiştirmek:** `.github/workflows/gunluk-paylasim.yml` içindeki `cron: "47 15 * * *"` (UTC; Türkiye = UTC+3)
- **Müzik/efekt eklemek:** Pixabay'den indirdiğin dosyaları `assets/audio/` içine yukarıdaki adlarla koy. Müzik konuşma sırasında otomatik kısılır.
- **Token:** 60 günde biter. `GH_PAT` tanımlıysa her pazartesi otomatik yenilenir; değilse ~50 günde bir 2. adımdan yeni token alıp secret'ı güncelle.

## Yerelde çalıştırma (isteğe bağlı)
```bash
pip install -r requirements.txt     # + ffmpeg, yazı tipleri: fonts/*.ttf
python daily.py status
python daily.py render              # output/<id>.mp4
python make_video.py episodes/001_istanbul_fethi.json --preview
python tests/test_publisher.py      # paylaşım modülü testi (internete çıkmaz)
```

## Lisanslar
Tüm çizimler kodla üretilir. Ses: Piper TTS (MIT) Türkçe "fahrettin" modeli. Yazı tipleri: SIL OFL (`fonts/LISANS.md`).
