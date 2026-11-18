"""Dördüncü bölüm paketini üretir (episodes/023..029). Ton: "karışık" + 13 Kasım ilk 3 saniye kuralları (kanca_yazi, gönderme cümlesi)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = "#çöpadamlatarih"
FOLLOW = "Her gün yeni bir tarih hikâyesi için takip et 📚"
TURN = "İşin en ilginç kısmı ne biliyor musun? "


def intro(say, pop1, pop2, text=None):
    return {"say": say, "text": text or say, "voice_delay": 1.0, "emotion": "şaşkın",
            "narrator": {"x": 0.5, "y": 0.97, "scale": 1.6, "pose": "wave", "face": "happy",
                         "beats": [{"t": 0.45, "pose": "point", "face": "wink"}, {"f": 0.0, "pose": "hips", "face": "happy"},
                                   {"f": 0.3, "pose": "think", "face": "think"}, {"f": 0.6, "pose": "open", "face": "surprised"},
                                   {"f": 0.85, "pose": "shrug", "face": "happy"}]},
            "props": [{"type": "pop", "text": pop1, "x": 0.27, "y": 0.15, "size": 120, "f": 0.0, "rot": -10, "until_f": 0.55},
                      {"type": "pop", "text": pop2, "x": 0.5, "y": 0.13, "size": 88, "f": 0.6, "rot": 5}]}


def outro(say="İşte böyle! Yarın yepyeni bir hikâye var. Takip et, kaçırma!"):
    return {"say": say, "text": say, "voice_delay": 0.5,
            "narrator": {"x": 0.5, "y": 0.97, "scale": 1.6, "pose": "open", "face": "happy",
                         "beats": [{"f": 0.35, "pose": "point", "face": "happy"}, {"f": 0.72, "pose": "wave", "face": "wink"}]},
            "props": [{"type": "pop", "text": "TAKİP ET!", "x": 0.5, "y": 0.13, "size": 120, "f": 0.72, "rot": -5}]}


def S(say, bg="plain", actors=(), props=(), text=None, **kw):
    d = {"say": say, "text": text or say, "bg": bg, "actors": list(actors), "props": list(props)}
    d.update(kw); return d


def A(id, x, hat=None, pose="stand", face="neutral", **kw):
    d = {"id": id, "x": x, "hat": hat, "pose": pose, "face": face}; d.update(kw); return d


def pop(text, x, y, delay, size=100, rot=0):
    return {"type": "pop", "text": text, "x": x, "y": y, "size": size, "delay": delay, "rot": rot}


def popf(text, x, y, f, size=100, rot=0):
    return {"type": "pop", "text": text, "x": x, "y": y, "size": size, "f": f, "rot": rot}


RIM = {"type": "sfx", "name": "rimshot", "f": 0.75}


def cap(hook, info, tags):
    """Kanca + bilgi + TEK çağrı + tam 5 etiket (sonuncusu #çöpadamlatarih)."""
    assert len(tags) == 4
    return f"{hook}\n\n{info}\n\n{FOLLOW}\n\n" + " ".join(tags + [TAG])




def outro_dm(send):
    """Kapanış: takip çağrısı + DM ile gönderme sebebi (son cümle, 13 Kasım kuralı)."""
    say = "İşte böyle! Yarın yeni hikâye var, takip et. " + send
    return {"say": say, "text": say, "voice_delay": 0.5,
            "narrator": {"x": 0.5, "y": 0.97, "scale": 1.6, "pose": "open", "face": "happy",
                         "beats": [{"f": 0.3, "pose": "point", "face": "happy"}, {"f": 0.72, "pose": "wave", "face": "wink"}]},
            "props": [{"type": "pop", "text": "TAKİP ET!", "x": 0.5, "y": 0.13, "size": 120, "f": 0.25, "rot": -5, "until_f": 0.6},
                      {"type": "pop", "text": "GÖNDER!", "x": 0.5, "y": 0.13, "size": 120, "f": 0.65, "rot": 5}]}


EP = []
# ---------------------------------------------------------------- 023 Sabiha Gökçen
EP.append({"id": "023", "file": "023_sabiha_gokcen", "title": "Soyadı Bile Göklerden Geliyordu!", "year": "1936",
 "kanca_yazi": "Dünyanın ilk kadın savaş pilotu kimdi?",
 "caption": cap("Guinness'e göre dünyanın ilk kadın savaş pilotu bir Türk'tü ✈️",
  "Sabiha Gökçen 1913'te Bursa'da doğdu, Atatürk tarafından evlat edinildi. 1934'te Soyadı Kanunu'yla \"göğe ait\" anlamındaki Gökçen soyadını aldı. "
  "1935'te Türkkuşu'nda uçmayı öğrendi, 1936'da Eskişehir'de askeri pilot eğitimine başladı ve 1938'de Balkan ülkelerini dolaşan bir uçuş yaptı. "
  "İstanbul'daki Sabiha Gökçen Havalimanı onun adını taşıyor.",
  ["#tarih", "#sabihagökçen", "#havacılık", "#atatürk"]),
 "scenes": [
  intro("Guinness'e göre dünyanın ilk kadın savaş pilotu bir Türk'tü. Üstelik soyadı bile göklerden geliyordu!", "İLK KADIN?", "SAVAŞ PİLOTU!"),
  S("1913, Bursa. Küçük Sabiha erken yaşta yetim kalır. 1925'te Bursa'ya gelen Atatürk'e cesurca okumak istediğini söyler.", "plain",
    [A("ataturk", 0.3, None, "stand", "happy", scale=1.3), A("sabiha", 0.68, None, "point", "confident", flip=True, scale=0.9, talk=True)],
    [{"type": "bubble", "text": "Okumak istiyorum!", "x": 0.62, "y": 0.13, "tx": 0.66, "ty": 0.42, "f": 0.6}]),
  S("Atatürk onu evlat edinir. 1934'te Soyadı Kanunu çıkınca soyadını da o verir: Gökçen. Yani göğe ait!", "plain",
    [A("ataturk", 0.3, None, "open", "happy", scale=1.3), A("sabiha", 0.68, None, "cheer", "happy", flip=True, scale=1.1, anim="bounce")],
    [{"type": "sun", "x": 0.85, "y": 0.15}, popf("GÖKÇEN!", 0.5, 0.22, 0.6, 120, -6)]),
  S(TURN + "O yıllarda daha uçağa hiç binmemiştir! 1935'te bir paraşüt gösterisi izler ve karar verir: Ben de uçacağım!", "hill",
    [A("sabiha", 0.4, None, "think", "think", scale=1.3, pose2="cheer", face2="confident", switch=0.65)],
    [{"type": "bulb", "actor": "sabiha", "f": 0.62}, popf("UÇACAĞIM!", 0.6, 0.2, 0.75, 110, 6)], emotion="şaşkın"),
  S("Türkkuşu'nda uçmayı öğrenir, 1936'da Eskişehir'de askeri pilot eğitimi alır. Erkek kursiyerlerin yüzü görülmeye değerdir.", "hill",
    [A("sabiha", 0.1, None, "open_arms", "happy", scale=0.8, wings=True, y=0.4, to_x=0.85, to_y=0.3, arc=0.1)],
    [popf("VIIIN!", 0.5, 0.18, 0.2, 110, -8)]),
  S("1938'de tek başına Balkan ülkelerini dolaşan bir uçuş yapar. Bugün İstanbul'da bir havalimanı onun adını taşır.", "city",
    [A("sabiha", 0.4, None, "hips", "confident", scale=1.35)],
    [{"type": "sign", "x": 0.75, "y": 0.6, "text": "SABİHA GÖKÇEN"}, popf("BALKAN TURU!", 0.45, 0.2, 0.15, 95, -6)]),
  S("Günün dersi: Senden önce kimse yapmadıysa, ilk olan sen olabilirsin.", "plain",
    [A("sabiha", 0.45, None, "cheer", "happy", scale=1.35)], [{"type": "flag", "actor": "sabiha", "emblem": True}, RIM], emotion="sakin"),
  outro_dm("Bunu hayallerinden vazgeçmeyen bir arkadaşına gönder.")]})

# ---------------------------------------------------------------- 024 Pompeii
EP.append({"id": "024", "file": "024_pompeii", "title": "Pompeii'yi Lav Yok Etmedi!", "year": "MS 79",
 "kanca_yazi": "Pompeii'yi lav yok etmedi!",
 "caption": cap("Pompeii'yi lav yok etti sanıyorsan yanılıyorsun 🌋",
  "MS 79'da Vezüv patladığında Pompeii'ye lav ulaşmadı; şehir önce süngertaşı ve kül yağmuruna, sonra kızgın gaz ve kül bulutlarına gömüldü. "
  "Felaketin tarihi uzun süre 24 Ağustos sanıldı, ancak 2018'de bulunan bir kömür yazısı patlamanın Ekim'de olmuş olabileceğini gösterdi. "
  "Şehirde kazılar 1748'de başladı.",
  ["#tarih", "#pompeii", "#vezüv", "#antikroma"]),
 "scenes": [
  intro("Pompeii'yi lav yok etti, değil mi? Hayır! Lav şehre hiç ulaşmadı.", "LAV?", "HİÇ ULAŞMADI!"),
  S("MS 79, İtalya. Pompeii, Vezüv Dağı'nın eteğinde hareketli bir Roma şehridir. Fırınlar, hamamlar, duvar yazıları...", "hill",
    [A("romali", 0.35, None, "relax", "happy", holds="cup", scale=1.25), A("firinci", 0.7, None, "point", "happy", flip=True, scale=1.15, talk=True)],
    [{"type": "sun", "x": 0.85, "y": 0.15}]),
  S("Çoğu Romalı, Vezüv'ün bir yanardağ olduğunun farkında bile değildir. Yamaçlarında üzüm yetiştirirler!", "farm",
    [A("romali", 0.4, None, "hips", "smug", holds="mug", scale=1.3)],
    [popf("ŞARAP VAKTİ!", 0.62, 0.22, 0.6, 100, 6)]),
  S("Sonra dağ uyanır. Gökten lav değil, kül ve süngertaşı yağar. Ardından kızgın bir gaz ve kül bulutu iner.", "hill", night=True,
    actors=[A("romali", 0.25, None, "shock", "shock", anim="walk", scale=1.15, to_x=0.85, move_dur=4)],
    props=[popf("KÜL!", 0.3, 0.2, 0.25, 110, -8), popf("KAÇ!", 0.7, 0.24, 0.65, 110, 6)]),
  S(TURN + "Tarihi bile tartışmalı! Okullarda 24 Ağustos denir. Ama 2018'de bulunan kömürle yazılmış bir not, felaketin Ekim'de olabileceğini gösterir.", "plain",
    [A("arkeolog", 0.35, "slouch", "think", "think", holds="scroll", scale=1.3, pose2="shock", face2="surprised", switch=0.7)],
    [{"type": "sign", "x": 0.75, "y": 0.6, "text": "AĞUSTOS? EKİM?"}], emotion="şaşkın"),
  S("Şehir yaklaşık 1700 yıl külün altında unutulur. Kazılar 1748'de başlar. Bugün Pompeii dev bir açık hava müzesidir.", "hill",
    [A("arkeolog", 0.4, "slouch", "cheer", "happy", scale=1.3, anim="bounce")],
    [popf("1748!", 0.65, 0.22, 0.45, 120, -6)]),
  S("Günün dersi: Sakin görünen her dağ, aslında uyuyan bir dev olabilir.", "hill",
    [A("romali", 0.45, None, "shrug", "sleepy", scale=1.35)], [RIM], emotion="sakin"),
  outro_dm("Bunu Pompeii'yi hâlâ lav yuttu sanan arkadaşına gönder.")]})

# ---------------------------------------------------------------- 025 Matbaa / Müteferrika
EP.append({"id": "025", "file": "025_muteferrika", "title": "Matbaa İstanbul'a Sandığından Önce Geldi!", "year": "1727",
 "kanca_yazi": "İstanbul'un ilk matbaası 1727'de değildi!",
 "caption": cap("İstanbul'daki ilk matbaa 1727'de kurulmadı; 230 yılı aşkın süre önce zaten vardı 📜",
  "1492'de İspanya'dan sürülen Yahudiler İstanbul'a sığındı ve 1490'larda İbranice kitap basan bir matbaa kurdu. Ardından Ermeni ve Rum matbaaları geldi. "
  "Arap harfli ilk Türkçe kitap ise İbrahim Müteferrika'nın 1727'de izin alıp kurduğu matbaada 1729'da basılan Vankulu Lügatı oldu. Müteferrika hayatı boyunca 17 eser bastı.",
  ["#tarih", "#matbaa", "#ibrahimmüteferrika", "#osmanlı"]),
 "scenes": [
  intro("İstanbul'un ilk matbaası 1727'de kurulmadı. 230 yılı aşkın süre önce şehirde zaten matbaa vardı!", "1727?", "230 YIL ÖNCE!"),
  S("1492. İspanya'dan sürülen Yahudiler Osmanlı'ya sığınır. Yanlarında yeni bir icat getirirler: matbaa!", "sea",
    [A("muhacir", 0.3, None, "point", "happy", holds="scroll", scale=1.2)],
    [{"type": "ship", "x": 0.72, "y": 0.75, "scale": 0.8}, popf("MATBAA!", 0.6, 0.22, 0.7, 110, 6)]),
  S("Kısa sürede İstanbul'da İbranice kitaplar basılır. Sonra Ermeniler ve Rumlar da kendi matbaalarını kurar.", "city",
    [A("muhacir", 0.3, None, "open", "happy", holds="scroll", scale=1.15), A("komsu", 0.7, None, "cheer", "happy", flip=True, holds="scroll", scale=1.15)]),
  S(TURN + "Arap harfli ilk Türkçe kitap için 1729'u beklemek gerekir. Bu işi yapan da Macaristan doğumlu bir Osmanlı: İbrahim Müteferrika!", "palace",
    [A("ibrahim", 0.4, "sarik", "hips", "confident", scale=1.35)],
    [popf("MÜTEFERRİKA!", 0.5, 0.2, 0.75, 95, -6)], emotion="şaşkın"),
  S("1727'de padişahtan izin alır. Ama bir şart vardır: Dini kitap basmak yasak! Hattatlar da işsiz kalırız diye huzursuzdur.", "palace",
    [A("padisah", 0.28, "kavuk", "point", "neutral", scale=1.2, talk=True), A("ibrahim", 0.72, "sarik", "shrug", "think", flip=True, scale=1.2)],
    [{"type": "ban", "x": 0.5, "y": 0.3, "f": 0.45}]),
  S("İlk kitabı koca bir sözlüktür: Vankulu Lügatı. Müteferrika hayatı boyunca 17 eser basar, haritalar bile!", "palace",
    [A("ibrahim", 0.4, "sarik", "cheer", "happy", holds="scroll", scale=1.35, anim="bounce")],
    [popf("17 ESER!", 0.65, 0.22, 0.6, 120, 6)]),
  S("Günün dersi: Yeni bir fikre geç kapı açan, yarışa geriden başlar.", "plain",
    [A("ibrahim", 0.45, "sarik", "think", "think", scale=1.35)], [{"type": "bulb", "actor": "ibrahim", "delay": 1.0}, RIM], emotion="sakin"),
  outro_dm("Bunu kitap kurdu arkadaşına gönder.")]})

# ---------------------------------------------------------------- 026 Tutankamon laneti
EP.append({"id": "026", "file": "026_tutankamon_laneti", "title": "Firavunun Laneti Neden Tutmadı?", "year": "1922",
 "kanca_yazi": "Firavunun laneti neden tutmadı?",
 "caption": cap("Lanetli mezarı açan adam, 16 yıl daha yaşadı 🏺",
  "Howard Carter Tutankamon'un mezarını Kasım 1922'de buldu. Kazının destekçisi Lord Carnarvon 1923'te enfekte olmuş bir sivrisinek ısırığı yüzünden ölünce gazeteler \"firavunun laneti\" hikâyesini yaydı. "
  "Carter ise 1939'a kadar yaşadı. 2002'de yayımlanan bir araştırma, mezara girenlerin ortalama 70 yaşına kadar yaşadığını buldu.",
  ["#tarih", "#tutankamon", "#antikmısır", "#firavun"]),
 "scenes": [
  intro("Firavunun laneti mi? Mezarı açan adam, tam 16 yıl daha yaşadı!", "LANET?", "16 YIL DAHA!"),
  S("Kasım 1922, Mısır. Howard Carter, Kral Tutankamon'un neredeyse el değmemiş mezarını bulur. İçerisi altın dolu!", "desert",
    [A("carter", 0.35, "slouch", "shock", "surprised", holds="torch", scale=1.3, y=0.9)],
    [{"type": "coins", "x": 0.7, "y": 0.9, "delay": 2.5}, popf("ALTIN!", 0.65, 0.22, 0.75, 120, 6)]),
  S("Kazıyı parayla destekleyen Lord Carnarvon birkaç ay sonra ölür. Gazeteler hemen yazar: Firavunun laneti!", "city",
    [A("muhabir", 0.4, "tophat", "point", "shock", holds="scroll", scale=1.3, talk=True)],
    [popf("LANET!", 0.65, 0.22, 0.6, 130, -8)]),
  S(TURN + "Ölüm sebebi lanet değil, bir sivrisinek ısırığıydı. Carnarvon tıraş olurken ısırığı kesmiş, yara mikrop kapmıştı.", "plain",
    [A("doktor", 0.4, None, "shrug", "smug", scale=1.3)],
    [popf("SİVRİSİNEK!", 0.6, 0.22, 0.4, 100, 6)], emotion="şaşkın"),
  S("Mezarda korkunç bir lanet yazısı da bulunmadı. O kısmı gazeteler süsledi.", "desert",
    [A("carter", 0.4, "slouch", "hips", "smug", scale=1.3, y=0.9)],
    [{"type": "pyramid", "x": 0.78, "y": 0.88, "scale": 0.7, "progress": 1.0}, {"type": "ban", "x": 0.7, "y": 0.3, "f": 0.3}]),
  S("2002'de bir araştırmacı mezara giren 25 kişiyi inceledi. Ortalama 70 yaşına kadar yaşamışlar. Carter da 1939'a kadar!", "plain",
    [A("carter", 0.4, "slouch", "cheer", "happy", scale=1.3, anim="bounce")],
    [{"type": "sign", "x": 0.75, "y": 0.6, "text": "ORT. 70 YAŞ"}]),
  S("Günün dersi: Korkutucu bir hikâye, sıkıcı bir gerçekten hep daha hızlı yayılır.", "plain",
    [A("carter", 0.45, "slouch", "think", "think", scale=1.35)], [{"type": "bulb", "actor": "carter", "delay": 1.0}, RIM], emotion="sakin"),
  outro_dm("Bunu her şeyi lanete bağlayan arkadaşına gönder.")]})

# ---------------------------------------------------------------- 027 Cezeri
EP.append({"id": "027", "file": "027_cezeri_robotlar", "title": "800 Yıl Önceki Robotlar", "year": "1206",
 "kanca_yazi": "800 yıl önce Diyarbakır'da robotlar vardı",
 "caption": cap("Robotlar modern çağın icadı değil; 800 yıl önce Diyarbakır'da mekanik hizmetçiler vardı 🤖",
  "El Cezeri, Artuklu hükümdarlarının hizmetinde 25 yılı aşkın süre çalıştı. 1206'da tamamladığı kitapta yaklaşık 50 düzeneği çizimleriyle anlattı: "
  "el yıkayanlara su döküp havlu uzatan mekanik hizmetçi, su üstünde çalan mekanik müzisyenler ve ünlü fil saati bunlardan bazıları.",
  ["#tarih", "#cezeri", "#robot", "#bilimtarihi"]),
 "scenes": [
  intro("Robotlar modern çağın icadı mı? 800 yıl önce Diyarbakır'da zaten vardı!", "ROBOT?", "800 YIL ÖNCE!"),
  S("1200'ler, Artuklu sarayı. Mühendis El Cezeri, 25 yılı aşkın süre saray için makineler yapar.", "palace",
    [A("cezeri", 0.38, "sarik", "point", "confident", holds="scroll", scale=1.3)],
    [popf("MÜHENDİS!", 0.65, 0.22, 0.55, 100, 6)]),
  S("Biri elini yıkamak ister. Mekanik bir hizmetçi çıkar, su döker, sonra havlu uzatır. Bahşiş de istemez!", "palace",
    [A("misafir", 0.3, "sarik", "shock", "surprised", scale=1.2), A("robot", 0.7, None, "push", "neutral", holds="cup", flip=True, scale=1.15)],
    [popf("HAVLU?", 0.5, 0.2, 0.55, 110, -6)]),
  S(TURN + "Bir de su üstünde çalan mekanik müzisyenler yapar. Davulcu, flütçü, hepsi otomatik. Eğlencenin yıldızı Cezeri!", "sea",
    [A("cezeri", 0.25, "sarik", "cheer", "happy", scale=1.1, anim="bounce")],
    [{"type": "ship", "x": 0.65, "y": 0.75, "scale": 0.8}, popf("DUM TEK!", 0.65, 0.22, 0.5, 110, 6)], emotion="şaşkın"),
  S("En ünlüsü ise fil saati. Filin sırtındaki kule, her yarım saatte bir ses çıkarıp vakti haber verir.", "palace",
    [A("cezeri", 0.35, "sarik", "hips", "smug", scale=1.3)],
    [{"type": "tower", "x": 0.75, "y": 0.93, "scale": 0.6}, popf("DING!", 0.75, 0.22, 0.7, 120, -6)]),
  S("1206'da yaklaşık 50 düzeneği çizimleriyle bir kitapta toplar. Bugün robotiğin öncülerinden sayılır.", "plain",
    [A("cezeri", 0.4, "sarik", "open", "happy", holds="scroll", scale=1.35)],
    [popf("50 MAKİNE!", 0.65, 0.22, 0.4, 100, 6)]),
  S("Günün dersi: Bugünün teknolojisi, dünün hayalperestlerinin omuzlarında yükselir.", "plain",
    [A("cezeri", 0.45, "sarik", "think", "think", scale=1.35)], [{"type": "bulb", "actor": "cezeri", "delay": 1.0}, RIM], emotion="sakin"),
  outro_dm("Bunu robot meraklısı bir arkadaşına gönder.")]})

# ---------------------------------------------------------------- 028 Layka
EP.append({"id": "028", "file": "028_layka_uzay", "title": "Uzaya İlk Çıkan Canlı Kimdi?", "year": "1957",
 "kanca_yazi": "Uzaya ilk çıkan canlı köpek değildi!",
 "caption": cap("Uzaya ilk çıkan canlı Layka değildi; meyve sinekleriydi 🚀",
  "1947'de ABD, bir V-2 roketiyle meyve sineklerini uzaya gönderdi ve sinekler canlı geri döndü. "
  "Moskova sokaklarından bulunan köpek Layka ise 3 Kasım 1957'de Sputnik 2 ile Dünya yörüngesine çıkan ilk hayvan oldu. "
  "2002'de açıklanan bilgilere göre Layka, uçuştan birkaç saat sonra aşırı sıcaktan öldü.",
  ["#tarih", "#layka", "#uzay", "#uzayyarışı"]),
 "scenes": [
  intro("Uzaya çıkan ilk canlı Layka mıydı? Hayır! Meyve sinekleriydi.", "LAYKA?", "SİNEKLER!"),
  S("1947. Amerikalılar bir rokete meyve sinekleri koyar. Sinekler uzaya çıkar ve sağ salim geri döner.", "desert",
    [A("bilimci", 0.35, None, "point", "happy", scale=1.3, y=0.9)],
    [popf("VIIIN!", 0.6, 0.2, 0.2, 110, -8), popf("BIZZ!", 0.7, 0.3, 0.7, 90, 6)]),
  S("10 yıl sonra uzay yarışı kızışır. Sovyetler, Moskova sokaklarında bulunan küçük bir köpeği seçer: Layka.", "city",
    [A("sovyet", 0.35, None, "open", "happy", scale=1.3)],
    [{"type": "sign", "x": 0.75, "y": 0.6, "text": "LAYKA"}, popf("HAV!", 0.7, 0.22, 0.75, 120, 6)]),
  S("3 Kasım 1957. Layka, Sputnik 2 ile Dünya yörüngesine çıkan ilk hayvan olur. Bütün dünya onu konuşur.", "plain", night=True,
    actors=[A("sovyet", 0.4, None, "cheer", "happy", scale=1.3, anim="bounce")],
    props=[popf("YÖRÜNGE!", 0.6, 0.22, 0.4, 110, -6)]),
  S(TURN + "Bu yolculuğun dönüşü hiç planlanmamıştı. Gerçek 2002'de açıklandı: Layka birkaç saat içinde aşırı sıcaktan ölmüştü.", "plain", night=True,
    actors=[A("sovyet", 0.4, None, "sad", "sad", scale=1.3)], emotion="üzgün"),
  S("Onun yolculuğu insanlı uçuşlara yol açtı. Bugün Moskova'da Layka için bir anıt var.", "city",
    [A("sovyet", 0.4, None, "stand", "neutral", scale=1.3)],
    [{"type": "sign", "x": 0.72, "y": 0.6, "text": "LAYKA ANITI"}]),
  S("Günün dersi: Büyük adımların arkasında, bedelini sessizce ödeyenler vardır.", "plain", night=True,
    actors=[A("sovyet", 0.45, None, "think", "sad", scale=1.35)], props=[RIM], emotion="sakin"),
  outro_dm("Bunu köpek seven bir arkadaşına gönder.")]})

# ---------------------------------------------------------------- 029 Sakarya
EP.append({"id": "029", "file": "029_sakarya", "title": "22 Gün 22 Gece Süren Savaş", "year": "1921",
 "kanca_yazi": "Kaburgası kırık, 22 gün savaşı yönetti",
 "caption": cap("Kaburgası kırık bir başkomutan, 22 gün 22 gece süren savaşı yönetti 🇹🇷",
  "Sakarya Meydan Muharebesi 23 Ağustos - 13 Eylül 1921 arasında sürdü. Mustafa Kemal savaştan kısa süre önce attan düşüp kaburgası kırılmasına rağmen orduyu cepheden yönetti. "
  "\"Hattı müdafaa yoktur, sathı müdafaa vardır\" emri bu savaşta verildi. Zaferin ardından TBMM ona Gazi unvanını ve mareşal rütbesini verdi.",
  ["#tarih", "#sakarya", "#kurtuluşsavaşı", "#atatürk"]),
 "scenes": [
  intro("Kaburgası kırık bir başkomutan, 22 gün 22 gece süren bir savaşı yönetti.", "KABURGA?", "22 GÜN!"),
  S("1921 yazı. Yunan ordusu Ankara'ya doğru ilerler. Meclis'te herkes aynı şeyi sorar: Ankara düşer mi?", "plain",
    [A("vekil", 0.3, "fez", "shock", "shock", scale=1.15, anim="shake"), A("vekil2", 0.7, "fez", "think", "think", flip=True, scale=1.15)],
    [{"type": "bubble", "text": "Ankara düşer mi?", "x": 0.4, "y": 0.13, "tx": 0.32, "ty": 0.32, "f": 0.6}]),
  S("Başkomutan Mustafa Kemal'dir. Ama savaştan hemen önce attan düşer ve kaburgası kırılır.", "hill",
    [A("mk", 0.35, None, "sad", "effort", scale=1.3)],
    [{"type": "horse", "x": 0.72, "y": 0.92, "scale": 0.8, "flip": True}, popf("AH!", 0.4, 0.22, 0.75, 120, -8)]),
  S("Doktorlar dinlen der. O ise cepheye gider ve ağrıya rağmen orduyu bizzat yönetir.", "battlefield",
    [A("mk", 0.4, None, "point", "confident", scale=1.3)],
    [{"type": "tent", "x": 0.8, "y": 0.9, "scale": 0.7}, popf("CEPHEYE!", 0.6, 0.22, 0.5, 110, 6)]),
  S(TURN + "Ünlü emri şudur: Hattı müdafaa yoktur, sathı müdafaa vardır. Yani savunulacak tek bir çizgi yok, bütün vatan var!", "battlefield",
    [A("mk", 0.4, None, "open", "confident", scale=1.35, talk=True)],
    [popf("BÜTÜN VATAN!", 0.5, 0.2, 0.8, 100, -6)], emotion="şaşkın"),
  S("23 Ağustos'ta başlayan savaş 13 Eylül'de zaferle biter. Meclis ona Gazi unvanını ve mareşal rütbesini verir.", "plain",
    [A("mk", 0.4, None, "cheer", "happy", scale=1.35)],
    [{"type": "flag", "actor": "mk", "emblem": True}, popf("GAZİ!", 0.65, 0.22, 0.7, 120, 6)]),
  S("Günün dersi: Canın yandığında bile pes etmezsen, zafer seni bulur.", "plain",
    [A("mk", 0.45, None, "hips", "confident", scale=1.35)], [RIM], emotion="sakin"),
  outro_dm("Bunu hiç pes etmeyen bir arkadaşına gönder.")]})

for ep in EP:
    out = {"id": ep["id"], "series": "ÇÖP ADAMLA TARİH", "title": ep["title"], "year": ep["year"],
           "kanca_yazi": ep["kanca_yazi"],
           "voice_fx": {"pitch": 1.15, "noise": 0.2, "noise_w": 0.3},
           "instagram_caption": ep["caption"], "scenes": ep["scenes"]}
    assert len(ep["kanca_yazi"].split()) <= 8, ep["id"]
    json.dump(out, open(os.path.join(ROOT, "episodes", ep["file"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    words = sum(len(s["say"].split()) for s in ep["scenes"])
    print("yazıldı:", ep["file"], len(ep["scenes"]), "sahne", words, "kelime")
