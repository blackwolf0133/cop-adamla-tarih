# YouTube otomasyonu — repo araştırması (10 Kasım 2026)

> Kullanıcı "YouTube repo araştırması" dediğinde bu dosya okunur ve buradan devam edilir.

## İstek
Instagram robotu gibi, 7 kanalın videolarını YouTube'a da otomatik (GitHub Actions ile) yüklemek.

## API durumu (doğrulandı)
- YouTube Data API revizyonu, 2 Kasım 2026: doğrulanmamış projelerden yüklenen videolar artık zorla "gizli" kalmıyor.
- `videos.insert` kendi kotasında: proje başına günde 100 yükleme (çağrı başına 1 birim). 7 kanal × 1 video rahat sığar.
- Shorts için özel uç nokta yok: dikey ve 60 sn altı videoyu YouTube otomatik Shorts sayar.
- OAuth kapsamı: `https://www.googleapis.com/auth/youtube.upload`. Refresh token gerekir.
- İzin ekranı "Testing" modunda kalırsa refresh token 7 günde düşer → **Production**'a alınmalı.

## Bulunan repolar
| Repo | Dil | Not |
|---|---|---|
| porjo/youtubeuploader | Go | En iyi hazır seçenek. Apache-2.0, hazır Linux binary, client_id.json + token JSON ile başsız çalışır. README'deki "private" ve "~6 video/gün" uyarıları eski. |
| BotolMehedi/automatic-youtube-shorts-uploader | PHP | Çok kanallı, panel + cron; kendi sunucusu gerekir, Actions düzenimize uymaz. |
| redianmarku/youtube-video-uploader | Python | Basit; ilk girişi tarayıcıdan bekliyor, uyarlama gerekir. |
| tokland/youtube-upload | Python | Eski. |
| SH20RAJ/youtube-remote-uploader | Python + Actions | Actions örneği. |
| anwerj/youtube-uploader-mcp | Go | Çok kanallı, MCP odaklı. |
| Selenium/Playwright yükleyicileri (ör. wanghaisheng/youtube-automation-toolkit) | — | Önerilmez: kırılgan; "Workspace gerekir" iddiası eski. |

## Karar önerisi
Kendi küçük `youtube_yukle.py` betiğimiz (google-api-python-client, refresh token secret'tan):
- Her repoda `gunluk-paylasim` içinde Instagram paylaşımından **sonra**, hata verse de IG'yi bozmayan adım.
- Yüklenen bölümü state'e yazar (aynı video iki kez gitmez).
- Önce tek kanalda dene, sonra 7 kanala yay.

## Kullanıcının bir kez yapacağı kurulum
1. Her IG kanalı için YouTube kanalı (tek Google hesabı altında marka kanalı olabilir).
2. Google Cloud projesi + YouTube Data API v3 etkin.
3. OAuth consent screen → Production.
4. OAuth istemcisi; OAuth Playground ile kanal başına refresh token.
5. GitHub secret'ları kullanıcı kendisi ekler (sohbete yapıştırmadan): `YT_CLIENT_ID`, `YT_CLIENT_SECRET`, `YT_REFRESH_TOKEN`.

## Durum
- Araştırma bitti, yaklaşım kullanıcıya sunuldu.
- Bekleyen: hangi kanalla başlanacağı / YouTube kanallarının açılması. Kullanıcı onaylamadan repo değişikliği yapılmaz.
