"""Beşinci bölüm paketini üretir (episodes/030..036). Ton: "karışık" + ilk 3 saniye kuralları; 25 Kasım istatistiğine göre somut insan hikâyesi + efsane yıkma ağırlıklı, ~45-50 sn."""
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
# ---------------------------------------------------------------- 030 Soyadı Kanunu
EP.append({"id": "030", "file": "030_soyadi_kanunu", "title": "1934'e Kadar Soyadın Yoktu!", "year": "1934",
 "kanca_yazi": "1934'e kadar kimsenin soyadı yoktu?",
 "caption": cap("1934'e kadar Türkiye'de çoğu insanın soyadı yoktu 🪪😳",
  "İnsanlar \"Bakkalın oğlu\", \"Uzun Ahmet\" gibi lakaplarla ayırt ediliyordu. 21 Haziran 1934'te kabul edilen Soyadı Kanunu ile herkese soyadı alma zorunluluğu geldi ve iki yıl süre tanındı. "
  "Kasım 1934'te Meclis, Mustafa Kemal'e \"Atatürk\" soyadını verdi ve bu soyadını başka kimsenin almasını yasakladı.",
  ["#tarih", "#soyadıkanunu", "#atatürk", "#cumhuriyet"]),
 "scenes": [
  intro("1934'e kadar Türkiye'de çoğu insanın soyadı yoktu. Peki herkes birbirini nasıl ayırıyordu?", "SOYADI?", "YOK!"),
  S("Cevap: lakaplarla! Uzun Ahmet, Bakkalın oğlu Mehmet, Kör Ali. Mahallede işe yarar, ama resmi işlerde tam bir karmaşa.", "city",
    [A("ahmet", 0.28, None, "point", "smug", scale=1.15, talk=True), A("mehmet", 0.72, None, "shrug", "happy", flip=True, scale=1.0)],
    [popf("UZUN AHMET!", 0.5, 0.2, 0.35, 96, -6)]),
  S("Düşünsene: Sınıfta beş Mehmet var ve beşi de babasının adıyla çağrılıyor. Askerlikte, mahkemede kim kimdir, kimse bilemiyor.", "plain",
    [A("m1", 0.2, None, "shock", "surprised", scale=0.95), A("m2", 0.5, None, "shrug", "think", scale=0.95), A("m3", 0.8, None, "point", "happy", flip=True, scale=0.95)],
    [popf("5 MEHMET!", 0.5, 0.18, 0.4, 110, 5)]),
  S("21 Haziran 1934'te Soyadı Kanunu çıkar. Herkes kendine bir soyadı seçecek, bunun için iki yıl süre var.", "plain",
    [A("memur", 0.35, None, "open", "confident", scale=1.25, holds="scroll")],
    [{"type": "sign", "x": 0.75, "y": 0.6, "text": "SOYADI KANUNU"}, popf("2 YIL SÜRE!", 0.5, 0.2, 0.7, 100, -5)]),
  S("Kimi mesleğini seçer, kimi memleketini, kimi de güçlü bir kelime. Demirci, Karadeniz, Yılmaz derken, ülke soyadına kavuşur.", "city",
    [A("demirci", 0.3, None, "cheer", "happy", scale=1.15, anim="bounce"), A("yolcu", 0.7, None, "think", "think", flip=True, scale=1.1)],
    [{"type": "bulb", "actor": "yolcu", "f": 0.5}, popf("YILMAZ!", 0.5, 0.2, 0.75, 110, 6)]),
  S(TURN + "Mustafa Kemal'in soyadını Meclis verdi: Atatürk. Ve bu soyadını başka hiç kimse alamaz.", "palace",
    [A("mk", 0.4, None, "hips", "confident", scale=1.35)],
    [popf("ATATÜRK", 0.5, 0.2, 0.55, 110, -5), {"type": "ban", "x": 0.78, "y": 0.4, "scale": 0.6, "f": 0.8}], emotion="şaşkın"),
  S("Günün dersi: İsmin seni tanıtır, ama ona anlam katan sensin.", "plain",
    [A("ahmet", 0.45, None, "hips", "confident", scale=1.35)], [RIM], emotion="sakin"),
  outro_dm("Bunu soyadının hikâyesini merak eden birine gönder.")]})

# ---------------------------------------------------------------- 031 Çin Seddi
EP.append({"id": "031", "file": "031_cin_seddi_uzay", "title": "Çin Seddi Uzaydan Görünmez!", "year": "2003",
 "kanca_yazi": "Çin Seddi uzaydan görünür mü?",
 "caption": cap("Çin Seddi uzaydan çıplak gözle görünür, değil mi? Değil! 🧱🚀",
  "Sur binlerce kilometre uzun ama genişliği çoğu yerde birkaç metre ve rengi toprağa çok benziyor. 2003'te uzaya çıkan ilk Çinli astronot Yang Liwei dönüşte \"Seddi görmedim\" dedi. "
  "Efsane ise insanlar uzaya çıkmadan çok önce yayılmıştı.",
  ["#tarih", "#çinseddi", "#uzay", "#efsane"]),
 "scenes": [
  intro("Çin Seddi uzaydan çıplak gözle görünür, değil mi? Değil! Bunu söyleyen de bir Çinli astronottu.", "UZAYDAN?", "GÖRÜNMEZ!"),
  S("Çin Seddi gerçekten dev. Bütün kollarıyla binlerce kilometre uzanıyor. Ama genişliği çoğu yerde sadece birkaç metre.", "hill",
    [A("isci", 0.25, None, "point", "confident", scale=1.1)],
    [{"type": "wall", "x": 0.7, "w": 0.55, "h": 0.3}, popf("UZUN AMA İNCE!", 0.5, 0.18, 0.7, 96, -5)]),
  S("Uzay istasyonu yaklaşık 400 kilometre yukarıda. Oradan seddi aramak, kilometrelerce uzaktan bir saç teli aramaya benziyor. Üstelik rengi toprakla aynı!", "plain",
    [A("astronot", 0.35, None, "think", "think", scale=1.25, y=0.6, anim="bounce")],
    [popf("400 KM!", 0.7, 0.2, 0.25, 110, 6), popf("SAÇ TELİ?", 0.62, 0.42, 0.65, 90, -5)]),
  S("2003'te Çin'in ilk astronotu Yang Liwei uzaya çıkar. Dönüşte herkes aynı soruyu sorar. Cevabı: Seddi görmedim!", "plain",
    [A("yang", 0.38, None, "shrug", "happy", scale=1.3, talk=True)],
    [{"type": "bubble", "text": "Görmedim!", "x": 0.42, "y": 0.13, "tx": 0.38, "ty": 0.32, "f": 0.75}], emotion="şaşkın"),
  S(TURN + "Efsane, astronotlardan önce uzaya çıkmıştı! İnsanlar daha roket bile yokken, 1930'larda Ay'dan bile görünür diye yazıyordu.", "plain",
    [A("gazeteci", 0.35, "tophat", "point", "smug", scale=1.25, holds="scroll")],
    [{"type": "sign", "x": 0.75, "y": 0.6, "text": "AY'DAN BİLE!"}, popf("ROKET YOK!", 0.5, 0.2, 0.6, 100, 5)], emotion="şaşkın"),
  S("Yani sed gerçekten muhteşem. Sadece uzaydan değil, yakından bakınca muhteşem.", "hill",
    [A("isci", 0.3, None, "cheer", "happy", scale=1.15, anim="bounce")],
    [{"type": "wall", "x": 0.72, "w": 0.5, "h": 0.32}, {"type": "sun", "x": 0.85, "y": 0.15}]),
  S("Günün dersi: Herkesin tekrarladığı her şey doğru değildir.", "plain",
    [A("yang", 0.45, None, "think", "think", scale=1.35)], [{"type": "bulb", "actor": "yang", "delay": 0.8}, RIM], emotion="sakin"),
  outro_dm("Bunu Çin Seddi uzaydan görünür diyen arkadaşına gönder.")]})

# ---------------------------------------------------------------- 032 Mona Lisa
EP.append({"id": "032", "file": "032_mona_lisa_hirsizlik", "title": "Mona Lisa'yı Ünlü Yapan Hırsız", "year": "1911",
 "kanca_yazi": "Mona Lisa'yı bir hırsız ünlü yaptı",
 "caption": cap("Mona Lisa'yı dünyanın en ünlü tablosu yapan şey bir hırsızlıktı 🖼️🕵️",
  "21 Ağustos 1911'de Louvre'da çalışmış bir işçi olan Vincenzo Peruggia tabloyu müzeden kaçırdı. Gazeteler aylarca bunu yazdı, polis Picasso'yu bile sorguladı. "
  "Tablo iki yılı aşkın süre bir sandıkta saklandı ve Aralık 1913'te Floransa'da bulundu.",
  ["#tarih", "#monalisa", "#louvre", "#sanattarihi"]),
 "scenes": [
  intro("Mona Lisa'yı dünyanın en ünlü tablosu yapan şey bir hırsızlıktı.", "HIRSIZLIK?", "ÜNLÜ OLDU!"),
  S("1911, Paris. Mona Lisa, Louvre'da sessiz sedasız asılı. Sanatçılar bilir, ama halk pek tanımaz.", "palace",
    [A("ziyaretci", 0.65, "tophat", "relax", "sleepy", flip=True, scale=1.15)],
    [{"type": "sign", "x": 0.3, "y": 0.6, "text": "MONA LİSA"}]),
  S("21 Ağustos'ta tablo yok olur. Hırsız, müzede daha önce çalışmış bir işçi: Vincenzo Peruggia. Tabloyu önlüğünün altına saklayıp çıkar.", "palace",
    [A("peruggia", 0.35, None, "push", "smug", scale=1.2, anim="walk", to_x=0.8, move_dur=4)],
    [popf("KAYIP!", 0.5, 0.2, 0.45, 120, -8)]),
  S("Gazeteler aylarca bunu yazar. Polis o kadar çaresizdir ki genç ressam Picasso'yu bile sorgular!", "plain",
    [A("polis", 0.3, None, "point", "confident", scale=1.2, talk=True), A("picasso", 0.72, None, "shock", "shock", flip=True, scale=1.1, anim="shake")],
    [popf("PİCASSO MU?!", 0.5, 0.2, 0.7, 96, 6)], emotion="şaşkın"),
  S(TURN + "Müze açılınca binlerce kişi, boş duvara bakmak için sıraya girer. Evet, boş duvara!", "palace",
    [A("z1", 0.3, "tophat", "shock", "surprised", scale=1.05), A("z2", 0.65, None, "think", "think", flip=True, scale=1.05)],
    [popf("BOŞ DUVAR!", 0.5, 0.2, 0.65, 110, -5)], emotion="şaşkın"),
  S("Tablo iki yıldan fazla, Peruggia'nın odasında, çift dipli bir sandıkta saklanır. 1913'te Floransa'da satmaya çalışınca yakalanır.", "plain",
    [A("peruggia", 0.4, None, "sad", "sad", scale=1.3)],
    [popf("YAKALANDI!", 0.6, 0.2, 0.75, 110, 6)]),
  S("Mona Lisa Louvre'a döner. Ama artık sıradan bir tablo değil, dünyanın en ünlü yüzü.", "palace",
    [A("ziyaretci", 0.65, "tophat", "cheer", "happy", flip=True, scale=1.15, anim="bounce")],
    [{"type": "sign", "x": 0.3, "y": 0.6, "text": "MONA LİSA"}, popf("DÜNYA ÜNLÜSÜ!", 0.5, 0.2, 0.6, 96, -5)]),
  S("Günün dersi: Bazen bir şeyin değerini, ancak kaybedince anlarız.", "plain",
    [A("ziyaretci", 0.45, "tophat", "think", "think", scale=1.35)], [RIM], emotion="sakin"),
  outro_dm("Bunu müzede hep sıkılan arkadaşına gönder.")]})

# ---------------------------------------------------------------- 033 Tünel
EP.append({"id": "033", "file": "033_istanbul_tunel", "title": "Dünyanın İkinci Metrosu İstanbul'da!", "year": "1875",
 "kanca_yazi": "Dünyanın 2. metrosu hangi şehirde?",
 "caption": cap("Dünyanın ikinci en eski metrosu İstanbul'da ve 1875'ten beri çalışıyor 🚋🤯",
  "Karaköy ile Beyoğlu arasındaki Tünel, 17 Ocak 1875'te açıldı. Fransız mühendis Eugène-Henri Gavand'ın fikriydi. "
  "Yaklaşık 573 metrelik hat, 60 metreden fazla yükseklik farkını bir buçuk dakikada çıkıyor. Ondan önceki tek yeraltı treni Londra'daydı (1863).",
  ["#tarih", "#istanbul", "#tünel", "#metro"]),
 "scenes": [
  intro("Dünyanın ikinci en eski metrosu Paris'te ya da New York'ta değil. İstanbul'da, hem de 1875'ten beri çalışıyor!", "PARİS?", "İSTANBUL!"),
  S("1860'lar, İstanbul. Karaköy'den Beyoğlu'na dik bir yokuş var. Her gün binlerce kişi, nefes nefese bu yokuşu tırmanıyor.", "city",
    [A("hamal", 0.3, "fez", "push", "effort", scale=1.1, anim="walk", to_x=0.5, move_dur=5)],
    [popf("OF!", 0.6, 0.22, 0.6, 120, -8)]),
  S("Fransız mühendis Eugène-Henri Gavand bu manzarayı görür ve aklına bir fikir gelir: Yokuşun altına bir tren!", "city",
    [A("gavand", 0.4, "tophat", "think", "think", scale=1.25)],
    [{"type": "bulb", "actor": "gavand", "f": 0.6}, popf("YERALTI TRENİ!", 0.5, 0.18, 0.75, 92, 5)]),
  S("1869'da izni alır. Kazılar yıllar sürer. Ve 17 Ocak 1875'te Tünel açılır. Sadece yaklaşık 573 metre ama 60 metreden fazla yükseliyor!", "city",
    [A("gavand", 0.3, "tophat", "cheer", "happy", scale=1.15, anim="bounce")],
    [{"type": "ruler", "x": 0.68, "y_top": 0.25, "labels": [[0.2, "61 m yukarı"]]}, popf("1875!", 0.3, 0.2, 0.5, 110, -6)]),
  S(TURN + "Ondan önce yeraltı treni olan tek şehir Londra. Yani İstanbul, yeraltı treninde dünyanın ikincisi!", "city",
    [A("yolcu", 0.38, "fez", "open", "surprised", scale=1.3)],
    [{"type": "sign", "x": 0.75, "y": 0.6, "text": "1. LONDRA  2. İSTANBUL"}], emotion="şaşkın"),
  S("Anlatılana göre ilk zamanlar bazı İstanbullular karanlık tünele binmeye çekinir. Bugün ise yolculuk bir buçuk dakika, yokuş derdi yok.", "city",
    [A("yolcu", 0.3, "fez", "shock", "surprised", scale=1.1, pose2="relax", face2="happy", switch=0.6), A("yolcu2", 0.7, None, "cheer", "happy", flip=True, scale=1.05)],
    [popf("1,5 DAKİKA!", 0.5, 0.2, 0.75, 100, 5)]),
  S("Günün dersi: Herkesin şikâyet ettiği yerde, bir fikir saklıdır.", "city",
    [A("gavand", 0.45, "tophat", "hips", "confident", scale=1.35)], [RIM], emotion="sakin"),
  outro_dm("Bunu her gün yokuş çıkan arkadaşına gönder.")]})

# ---------------------------------------------------------------- 034 İstiklal Marşı
EP.append({"id": "034", "file": "034_istiklal_marsi", "title": "Ödülü İstemedi, Marşı Yazdı!", "year": "1921",
 "kanca_yazi": "Ödül yüzünden yarışmaya katılmadı!",
 "caption": cap("İstiklal Marşı'nı yazan şair, yarışmaya önce katılmadı. Sebebi: para ödülü 🇹🇷✍️",
  "1920'de açılan milli marş yarışmasına 724 şiir gönderildi, ödül 500 liraydı. Mehmet Akif ödül yüzünden katılmak istemedi; ısrarlar üzerine şiirini yazdı. "
  "12 Mart 1921'de Meclis onun şiirini İstiklal Marşı olarak kabul etti. Akif ödülü, yoksul kadın ve çocuklara iş öğreten Darülmesai'ye bağışladı.",
  ["#tarih", "#istiklalmarşı", "#mehmetakifersoy", "#12mart"]),
 "scenes": [
  intro("İstiklal Marşı'nı yazan şair, yarışmaya önce katılmadı. Sebebi de ödüldü!", "KATILMADI?", "NEDEN?!"),
  S("1920, Ankara. Kurtuluş Savaşı sürüyor ve ülkenin bir marşa ihtiyacı var. Bir yarışma açılır, ödül 500 lira.", "plain",
    [A("vekil", 0.35, "fez", "point", "confident", scale=1.25, holds="scroll")],
    [{"type": "coins", "x": 0.72, "y": 0.93, "f": 0.6}, popf("500 LİRA!", 0.6, 0.2, 0.75, 110, 6)]),
  S("Tam 724 şiir gelir! Jüri okur, okur, okur. Ama hiçbiri tam olarak o hissi vermez.", "palace",
    [A("juri", 0.35, "fez", "think", "sleepy", scale=1.2, holds="scroll")],
    [popf("724 ŞİİR!", 0.65, 0.2, 0.25, 110, -5), popf("ESNEME...", 0.65, 0.42, 0.75, 80, 5)]),
  S("Peki Mehmet Akif nerede? Katılmamış! Çünkü para ödüllü bir yarışmada vatan şiiri yazmak istemiyor.", "plain",
    [A("akif", 0.4, "fez", "shrug", "neutral", scale=1.3)],
    [{"type": "ban", "x": 0.75, "y": 0.4, "scale": 0.6, "f": 0.5}], emotion="şaşkın"),
  S("Milli Eğitim Bakanı Hamdullah Suphi ısrar eder: Ödül şartı senin için kaldırılır, yeter ki yaz! Akif sonunda kalemi alır.", "plain",
    [A("hamdullah", 0.28, "fez", "open", "happy", scale=1.15, talk=True), A("akif", 0.72, "fez", "think", "think", flip=True, scale=1.15)],
    [{"type": "bulb", "actor": "akif", "f": 0.8}]),
  S(TURN + "12 Mart 1921'de Meclis onun şiirini milli marş olarak kabul eder. Akif ise 500 lirayı yoksul kadın ve çocuklara iş öğreten bir kuruma bağışlar.", "palace",
    [A("akif", 0.4, "fez", "open", "happy", scale=1.3)],
    [{"type": "flag", "actor": "akif", "emblem": True}, popf("BAĞIŞLADI!", 0.65, 0.2, 0.8, 100, 6)], emotion="şaşkın"),
  S("Günün dersi: Bazı işler para için değil, gönülden yapılır.", "plain",
    [A("akif", 0.45, "fez", "hips", "confident", scale=1.35)], [RIM], emotion="sakin"),
  outro_dm("Bunu işini gönülden yapan birine gönder.")]})

# ---------------------------------------------------------------- 035 Eyfel
EP.append({"id": "035", "file": "035_eyfel_kulesi", "title": "Eyfel Kulesi Sökülecekti!", "year": "1889",
 "kanca_yazi": "Eyfel Kulesi sökülecekti!",
 "caption": cap("Eyfel Kulesi 20 yıl sonra sökülmek üzere yapıldı 🗼😮",
  "Kule 1889 Paris Dünya Fuarı için dikildi. Pek çok ünlü sanatçı ona \"işe yaramaz, korkunç\" diye karşı çıktı. Gustave Eiffel'in arazi izni 20 yıllıktı ve kule 1910'da şehre devredilecekti. "
  "Onu kurtaran, tepesinde yapılan bilim deneyleri ve özellikle radyo yayınları oldu.",
  ["#tarih", "#eyfelkulesi", "#paris", "#mühendislik"]),
 "scenes": [
  intro("Eyfel Kulesi sadece 20 yıl ayakta kalsın diye yapıldı. Sonra sökülecekti!", "SÖKÜLECEK?", "20 YIL!"),
  S("1889, Paris. Büyük bir dünya fuarı var. Mühendis Gustave Eiffel, o güne kadar yapılmış en yüksek yapıyı dikiyor.", "plain",
    [A("eiffel", 0.3, "tophat", "point", "confident", scale=1.2)],
    [{"type": "ruler", "x": 0.7, "y_top": 0.15, "labels": [[0.2, "~300 m"]]}, popf("EN YÜKSEK!", 0.45, 0.2, 0.7, 100, -5)]),
  S("Ama herkes sevinmez. Ünlü sanatçılar gazetede mektup yayımlar: Bu işe yaramaz, korkunç bir demir yığını!", "plain",
    [A("sanatci", 0.35, "tophat", "shock", "shock", scale=1.2, anim="shake", holds="scroll")],
    [popf("KORKUNÇ!", 0.65, 0.2, 0.6, 120, 6)]),
  S("Üstelik Eiffel'in arazi izni sadece 20 yıllık. 1910'da kule şehre geçecek ve sökülebilecek.", "plain",
    [A("eiffel", 0.4, "tophat", "sad", "sad", scale=1.3)],
    [{"type": "sign", "x": 0.75, "y": 0.6, "text": "İZİN: 20 YIL"}]),
  S(TURN + "Kuleyi kurtaran şey güzelliği değil, tepesindeki anten oldu! Eiffel orada bilim deneyleri yaptırır, 1898'de ilk radyo bağlantısı kurulur.", "plain",
    [A("eiffel", 0.35, "tophat", "think", "think", scale=1.25)],
    [{"type": "bulb", "actor": "eiffel", "f": 0.35}, popf("ANTEN!", 0.65, 0.2, 0.55, 120, -6)], emotion="şaşkın"),
  S("Kule bir radyo istasyonuna dönüşür. Bu kadar faydalı bir yapı sökülür mü? Sökülmez! İzin 70 yıl uzatılır.", "plain",
    [A("eiffel", 0.4, "tophat", "cheer", "happy", scale=1.3, anim="bounce")],
    [popf("70 YIL DAHA!", 0.6, 0.2, 0.7, 100, 6)]),
  S("O korkunç denilen demir yığını, bugün dünyanın en çok fotoğrafı çekilen yerlerinden biri. Sanatçılara sürpriz!", "plain",
    [A("sanatci", 0.4, "tophat", "shrug", "happy", scale=1.25)], [{"type": "sun", "x": 0.85, "y": 0.15}]),
  S("Günün dersi: Bir şeyi kurtarmanın en iyi yolu, onu faydalı kılmaktır.", "plain",
    [A("eiffel", 0.45, "tophat", "hips", "confident", scale=1.35)], [RIM], emotion="sakin"),
  outro_dm("Bunu Paris'e gitmeyi hayal eden arkadaşına gönder.")]})

# ---------------------------------------------------------------- 036 Divanü Lügati't-Türk
EP.append({"id": "036", "file": "036_divanu_lugat", "title": "Sahafta Bulunan Hazine", "year": "1072",
 "kanca_yazi": "Bu hazine sahafta satılıyordu!",
 "caption": cap("Türkçenin en eski sözlüğünün bilinen tek nüshası, bir sahaf dükkânında satılıyordu 📜🔍",
  "Kaşgarlı Mahmud, Divanü Lügati't-Türk'ü 1072-1074 yılları arasında Bağdat'ta, Araplara Türkçe öğretmek için yazdı. Eserde bir dünya haritası bile var. "
  "Yüzyıllar sonra Birinci Dünya Savaşı yıllarında Ali Emîrî Efendi, kitabı İstanbul'daki sahaflarda borç parayla satın aldı. Bugün Millet Kütüphanesi'nde.",
  ["#tarih", "#divanulugatitturk", "#kaşgarlımahmud", "#türkçe"]),
 "scenes": [
  intro("Türkçenin en eski sözlüğünün bilinen tek nüshası, bir sahaf dükkânında satılıyordu!", "SAHAFTA?", "TEK NÜSHA!"),
  S("Yıl 1072. Kaşgarlı Mahmud Bağdat'ta oturur ve Araplara Türkçe öğretmek için dev bir eser yazmaya başlar.", "palace",
    [A("kasgarli", 0.35, "selcuk", "think", "think", scale=1.25, holds="scroll")],
    [popf("1072!", 0.7, 0.2, 0.3, 110, 6)]),
  S("Adı Divanü Lügati't-Türk. İçinde binlerce kelime, atasözleri, şiirler, hatta bir dünya haritası var!", "palace",
    [A("kasgarli", 0.35, "selcuk", "open", "happy", scale=1.25, holds="scroll")],
    [popf("HARİTA BİLE!", 0.65, 0.2, 0.75, 100, -5)]),
  S("Ama zamanla kitap ortadan kaybolur. Yüzyıllar boyunca kimse nerede olduğunu bilmez.", "plain",
    [A("kasgarli", 0.45, "selcuk", "shrug", "sad", scale=1.25)],
    [popf("KAYIP!", 0.5, 0.2, 0.5, 120, 6)]),
  S("Birinci Dünya Savaşı yılları, İstanbul. Kitap kurdu Ali Emîrî Efendi sahafları dolaşırken eski bir el yazmasına rastlar.", "city",
    [A("aliemiri", 0.35, "fez", "shock", "surprised", scale=1.25, holds="scroll")], [], emotion="şaşkın"),
  S(TURN + "Cebinde yeterli para yoktur. Borç alır ve kitabı kapar! Ve o kitap, bugün bilinen tek nüsha çıkar.", "city",
    [A("aliemiri", 0.3, "fez", "cheer", "happy", scale=1.2, anim="bounce", holds="scroll")],
    [{"type": "coins", "x": 0.7, "y": 0.93, "f": 0.3}, popf("TEK NÜSHA!", 0.55, 0.2, 0.75, 100, -5)]),
  S("Bugün İstanbul'daki Millet Kütüphanesi'nde saklanıyor. Düşünsene, bir hazine az kalsın kâğıt fiyatına gidiyordu.", "palace",
    [A("aliemiri", 0.4, "fez", "hips", "smug", scale=1.3)], [{"type": "sign", "x": 0.75, "y": 0.6, "text": "MİLLET KÜTÜPHANESİ"}]),
  S("Günün dersi: Eski bir kitabı küçümseme, içinde koca bir dünya saklı olabilir.", "plain",
    [A("aliemiri", 0.45, "fez", "think", "think", scale=1.35)], [RIM], emotion="sakin"),
  outro_dm("Bunu sahaflarda saatlerce dolaşan arkadaşına gönder.")]})

for ep in EP:
    out = {"id": ep["id"], "series": "ÇÖP ADAMLA TARİH", "title": ep["title"], "year": ep["year"],
           "kanca_yazi": ep["kanca_yazi"],
           "voice_fx": {"pitch": 1.15, "noise": 0.2, "noise_w": 0.3},
           "instagram_caption": ep["caption"], "scenes": ep["scenes"]}
    assert len(ep["kanca_yazi"].split()) <= 8, ep["id"]
    assert 8 <= len(ep["scenes"]) <= 10, ep["id"]
    json.dump(out, open(os.path.join(ROOT, "episodes", ep["file"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    words = sum(len(s["say"].split()) for s in ep["scenes"])
    print("yazıldı:", ep["file"], len(ep["scenes"]), "sahne", words, "kelime")
