"""Üçüncü bölüm paketini üretir (episodes/016..022). Ton: "karışık" (belgesel + hafif espri)."""
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


EP = []
# ---------------------------------------------------------------- 016 Mimar Sinan / Selimiye
EP.append({"id": "016", "file": "016_selimiye", "title": "80 Yaşında \"Ancak Şimdi Usta Oldum\" Dedi!", "year": "1575",
 "caption": cap("Süleymaniye Camii'ni yapan adam, kendine sadece \"kalfa\" dedi 🕌🤯",
  "Mimar Sinan, Şehzade Camii için \"çıraklık eserim\", Süleymaniye için \"kalfalık eserim\" der. "
  "Ustalık eserim dediği yapı ise 80 yaşını geçmişken Edirne'de bitirdiği Selimiye'dir (1568-1575). "
  "Kubbesi 31 metreyi aşar; minareleri yaklaşık 71 metredir ve cami 2011'den beri UNESCO Dünya Mirası listesinde.",
  ["#tarih", "#mimarsinan", "#selimiye", "#osmanlı"]),
 "scenes": [
  intro("Süleymaniye Camii'ni yapan adam, kendine sadece kalfa dedi. Peki usta olduğu eser hangisi?", "KALFA?!", "SÜLEYMANİYE!"),
  S("Mimar Sinan, Osmanlı'nın baş mimarı. Yaklaşık 50 yılda yüzlerce eser yapar: camiler, köprüler, hamamlar.", "city",
    [A("sinan", 0.35, "sarik", "point", "confident", holds="scroll", scale=1.3)],
    [{"type": "tower", "x": 0.8, "y": 0.93, "scale": 0.8}, pop("YÜZLERCE ESER!", 0.5, 0.22, 2.5, 92, -6)]),
  S("Kendi eserlerini de not verir gibi sıralar. İstanbul'daki Şehzade Camii için: Çıraklık eserim.", "city",
    [A("sinan", 0.4, "sarik", "think", "think", scale=1.35)], [popf("ÇIRAK!", 0.65, 0.25, 0.6, 120, 6)]),
  S("Dev Süleymaniye için ise: Kalfalık eserim. Yani hâlâ öğreniyorum!", "city",
    [A("sinan", 0.4, "sarik", "shrug", "smug", scale=1.35)], [popf("KALFA!", 0.65, 0.25, 0.4, 120, -6)]),
  S(TURN + "Usta olduğunu söylemesi için 80 yaşını geçmesi gerekir. Biz o yaşta kumandayı zor buluyoruz, o Edirne'de Selimiye'yi diker!", "palace",
    [A("sinan", 0.4, "sarik", "cheer", "happy", scale=1.35, anim="bounce")],
    [popf("80 YAŞINDA!", 0.6, 0.22, 0.25, 100, 6)], emotion="şaşkın"),
  S("Hedefi büyük: Ayasofya'nın kubbesini aşmak. Selimiye'nin kubbesi 31 metreyi geçer, minareleri ise yaklaşık 71 metre!", "palace",
    [A("sinan", 0.3, "sarik", "point", "confident", holds="scroll", scale=1.25, talk=True)],
    [{"type": "ruler", "x": 0.72, "y_base": 0.93, "y_top": 0.3, "labels": [[0.95, "71 m"], [0.45, "31 m"]]},
     popf("AYASOFYA'YI AŞ!", 0.5, 0.18, 0.2, 88, -5)]),
  S("1575'te cami tamamlanır. Sinan'ın yorumu kısa: Ustalık eserim.", "palace",
    [A("sinan", 0.42, "sarik", "hips", "confident", scale=1.4)], [popf("USTALIK!", 0.6, 0.22, 0.6, 120, -6)]),
  S("Günün dersi: Gerçek usta, kendine en son usta diyen kişidir.", "palace",
    [A("sinan", 0.45, "sarik", "think", "think", scale=1.35)], [{"type": "bulb", "actor": "sinan", "delay": 1.0}, RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 017 Evliya Çelebi
EP.append({"id": "017", "file": "017_evliya_celebi", "title": "Bir Dil Sürçmesi, 40 Yıllık Yolculuk!", "year": "1630",
 "caption": cap("Bir dil sürçmesi, bir adamı 40 yıl yollara düşürdü 🗺️😅",
  "Evliya Çelebi'nin kendi anlattığına göre 1630'da, 20 yaşlarındayken rüyasında Peygamber'i gördü; \"şefaat\" isteyecekken heyecandan \"seyahat\" dedi. "
  "Sonra 40 yıldan fazla Anadolu'dan Balkanlar'a, Viyana'dan Mısır'a gezdi ve gördüklerini 10 ciltlik Seyahatname'ye yazdı. "
  "Hezarfen'in uçuşunu bize anlatan da odur!",
  ["#tarih", "#evliyaçelebi", "#seyahatname", "#osmanlı"]),
 "scenes": [
  intro("Bir dil sürçmesi, bir adamı 40 yıl yollara düşürdü. Hem de tek bir kelime!", "TEK KELİME!", "40 YIL?!"),
  S("Yıl 1630. İstanbul'da 20 yaşlarında bir genç, Evliya. Kendi anlattığına göre bir gece rüyasında Peygamber'i görür.", "city", night=True,
    actors=[A("evliya", 0.38, "sarik", "relax", "sleepy", scale=1.3)], props=[pop("RÜYA...", 0.6, 0.25, 2.5, 110, -6)]),
  S("Ondan şefaat isteyecektir. Ama heyecandan ağzından başka bir kelime çıkar: Seyahat!", "city", night=True,
    actors=[A("evliya", 0.4, "sarik", "open", "happy", scale=1.35, pose2="shock", face2="shock", switch=0.65)],
    props=[popf("ŞEFAAT?", 0.3, 0.2, 0.15, 96, -8), popf("SEYAHAT!", 0.65, 0.25, 0.7, 120, 6)]),
  S("Anlatıya göre ikisi de kabul olur. Ve Evliya yola çıkar. Anadolu, Kafkasya, Balkanlar, Viyana, Mısır...", "desert",
    [A("evliya", 0.3, "sarik", "point", "happy", anim="walk", to_x=0.55, scale=1.25, y=0.9)],
    [{"type": "palm", "x": 0.82, "y": 0.9, "scale": 0.9}, {"type": "sun", "x": 0.85, "y": 0.15}]),
  S(TURN + "40 yıldan fazla gezer ve her şeyi yazar. Sonuç: 10 ciltlik Seyahatname! Galata'dan uçan Hezarfen'i bize anlatan da o.", "city",
    [A("evliya", 0.35, "sarik", "cheer", "happy", holds="scroll", scale=1.3)],
    [{"type": "tower", "x": 0.8, "y": 0.93, "scale": 0.8}, popf("10 CİLT!", 0.55, 0.22, 0.35, 120, 6)], emotion="şaşkın"),
  S("Bazen biraz abartır, bazen hikâyeyi süsler. Ama 17. yüzyılı en canlı anlatan kaynaklardan biri onun kitabı.", "plain",
    [A("evliya", 0.4, "sarik", "shrug", "smug", holds="scroll", scale=1.35)], [popf("BİRAZ ABARTI!", 0.6, 0.22, 0.2, 92, -6)]),
  S("Günün dersi: Bazen bir hata, hayatının yolunu çizer.", "plain",
    [A("evliya", 0.45, "sarik", "think", "think", scale=1.35)], [{"type": "bulb", "actor": "evliya", "delay": 1.0}, RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 018 Roma idrar vergisi
EP.append({"id": "018", "file": "018_roma_idrar_vergisi", "title": "Romalılar Tuvalete Vergi Koydu!", "year": "MS 70",
 "caption": cap("Romalılar çamaşırlarını çişle yıkadı. İmparator da buna vergi koydu! 🚽💰",
  "Antik Roma'da çamaşırcılar ve deri ustaları, içindeki amonyak yüzünden idrarı temizlik için kullanırdı. "
  "İmparator Vespasianus MS 70 civarında halka açık tuvaletlerden satılan idrara vergi koydu. "
  "Oğlu Titus itiraz edince bir altın para uzatıp \"Kokuyor mu?\" diye sordu; \"Para kokmaz\" sözü buradan gelir.",
  ["#tarih", "#antikroma", "#roma", "#ilginçbilgiler"]),
 "scenes": [
  intro("Romalılar çamaşırlarını çişle yıkadı. Ve imparator buna vergi koydu!", "ÇİŞ?!", "VERGİ!"),
  S("Antik Roma'da çamaşırcılar halka açık tuvaletlerden idrar toplar. İçindeki amonyak, lekeleri söker!", "plain",
    [A("camasirci", 0.35, None, "push", "effort", holds="mug", scale=1.3)], [popf("AMONYAK!", 0.65, 0.22, 0.6, 110, 6)]),
  S("Yani Roma'da çiş, satılan bir maldı. Deri ustaları da bayılarak alıyordu.", "plain",
    [A("camasirci", 0.28, None, "open", "happy", holds="mug", scale=1.15), A("usta", 0.72, None, "point", "smug", flip=True, scale=1.15)],
    [{"type": "coins", "x": 0.5, "y": 0.93, "delay": 1.5}]),
  S("Yıl 70 civarı. İmparator Vespasianus'un hazinesi boş. Aklına parlak bir fikir gelir: Bu ticarete vergi!", "palace",
    [A("vespasian", 0.4, "crown", "think", "think", scale=1.35, pose2="point", face2="smug", switch=0.6)],
    [{"type": "bulb", "actor": "vespasian", "f": 0.55}]),
  S(TURN + "Oğlu Titus itiraz eder: Bu iğrenç! İmparator bir altın para çıkarır, burnuna uzatır: Kokuyor mu?", "palace",
    [A("vespasian", 0.3, "crown", "point", "smug", scale=1.25, talk=True), A("titus", 0.72, None, "shock", "shock", flip=True, scale=1.2)],
    [{"type": "coins", "x": 0.5, "y": 0.93}, popf("İĞRENÇ!", 0.7, 0.22, 0.25, 110, 8)], emotion="şaşkın"),
  S("Titus: Hayır. Vespasianus: Ama çişten geldi! Para kokmaz sözü işte buradan çıkar.", "palace",
    [A("titus", 0.4, None, "shrug", "surprised", scale=1.35)], [popf("PARA KOKMAZ!", 0.55, 0.22, 0.6, 100, -6)]),
  S("Bugün bile Fransa'da eski sokak tuvaletlerine onun adı verilir: Vespasienne. Pek gurur verici bir miras değil!", "plain",
    [A("vespasian", 0.4, "crown", "sad", "sad", scale=1.35)], [{"type": "sign", "x": 0.75, "y": 0.93, "text": "WC"}]),
  S("Günün dersi: Herkesin burun kıvırdığı yerde bazen bir fırsat saklıdır.", "palace",
    [A("vespasian", 0.45, "crown", "hips", "confident", scale=1.4)], [{"type": "coins", "x": 0.75, "y": 0.93}, RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 019 Gordion düğümü
EP.append({"id": "019", "file": "019_gordion_dugumu", "title": "Çözülmeyen Düğümü Böyle Çözdü!", "year": "MÖ 333",
 "caption": cap("Bu düğümü çözen Asya'nın kralı olacaktı. İskender çözmedi... ikiye böldü! 🪢⚔️",
  "Efsaneye göre Ankara Polatlı yakınlarındaki Gordion'da, Frig kralı Gordias'ın öküz arabası ucu görünmeyen bir düğümle bağlıydı. "
  "MÖ 333'te gelen Büyük İskender düğümü kılıcıyla kesti; başka bir anlatıya göre ise arabanın çivisini çekip düğümü gevşetti. "
  "Gordion bugün UNESCO Dünya Mirası listesinde.",
  ["#tarih", "#büyükiskender", "#gordion", "#antiktarih"]),
 "scenes": [
  intro("Bu düğümü çözen, Asya'nın kralı olacaktı. Büyük İskender çözmedi... ikiye böldü!", "DÜĞÜM!", "İKİYE Mİ?!"),
  S("Yer: Bugünkü Ankara, Polatlı yakınları. Frigya'nın başkenti Gordion. Dokunduğunu altına çeviren efsanevi Kral Midas'ın şehri!", "plain",
    [A("midas", 0.35, "crown", "open", "happy", scale=1.3)], [{"type": "coins", "x": 0.7, "y": 0.9}, pop("GORDİON!", 0.5, 0.22, 2.0, 110, -6)]),
  S("Efsaneye göre şehirde bir öküz arabası durur. Arabanın oku öyle karmaşık bir düğümle bağlıdır ki, ucu bile görünmez.", "plain",
    [A("koylu", 0.25, None, "think", "think", scale=1.15)],
    [{"type": "chain", "x1": 0.45, "x2": 0.95, "y": 0.75, "anim": "shake"}, popf("UCU YOK!", 0.65, 0.25, 0.6, 110, 6)]),
  S("Kehanet açık: Bu düğümü çözen, bütün Asya'ya hükmedecek. Yüzyıllar boyunca herkes dener, kimse çözemez.", "plain",
    [A("koylu", 0.3, None, "push", "effort", scale=1.2, pose2="sad", face2="sad", switch=0.6)],
    [{"type": "chain", "x1": 0.5, "x2": 1.0, "y": 0.75}, popf("ASYA!", 0.6, 0.22, 0.2, 120, -6)]),
  S(TURN + "MÖ 333'te 23 yaşındaki İskender gelir. Biraz uğraşır, sonra kılıcını çeker ve düğümü ikiye böler! Kural kitabında kesmek yasak yazmıyordu ki.", "plain",
    [A("iskender", 0.3, "greek", "think", "think", holds="sword", scale=1.25, pose2="cheer", face2="smug", switch=0.55)],
    [{"type": "chain", "x1": 0.55, "x2": 1.0, "y": 0.75}, popf("ŞAK!", 0.7, 0.25, 0.58, 130, 8), {"type": "sfx", "name": "whoosh", "f": 0.55}],
    emotion="şaşkın"),
  S("Ama bir başka anlatıya göre kesmedi. Arabanın okundaki çiviyi çekti, düğüm de kendiliğinden gevşedi.", "plain",
    [A("iskender", 0.4, "greek", "shrug", "smug", scale=1.35)], [popf("ÇİVİ!", 0.65, 0.22, 0.4, 120, -6)]),
  S("Hangisi doğru, bilmiyoruz. Ama İskender gerçekten Hindistan'a kadar uzanır. Gordion ise bugün UNESCO Dünya Mirası.", "battlefield",
    [A("iskender", 0.3, "greek", "point", "confident", scale=1.2, y=0.9)], [{"type": "horse", "x": 0.68, "y": 0.92, "scale": 0.85, "flip": True}]),
  S("Günün dersi: Zor bir soruya bazen kimsenin bakmadığı yerden bakmak gerekir.", "plain",
    [A("iskender", 0.45, "greek", "think", "think", scale=1.35)], [{"type": "bulb", "actor": "iskender", "delay": 1.0}, RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 020 Cem Sultan
EP.append({"id": "020", "file": "020_cem_sultan", "title": "Avrupa'da Rehin Kalan Şehzade", "year": "1482",
 "caption": cap("Bir padişah, kardeşi uzakta kalsın diye her yıl 40 bin altın ödedi 💰👑",
  "Fatih'in 1481'de ölümünden sonra oğulları Bayezid ile Cem taht için karşı karşıya geldi. Kaybeden Cem, 1482'de Rodos şövalyelerine sığındı ama misafir değil rehin oldu. "
  "II. Bayezid şövalyelere, Cem'i tutsunlar diye yılda 40 bin duka altını ödedi. Cem yaklaşık 13 yıl Fransa ve Roma'da elden ele dolaştı, 1495'te İtalya'da 35 yaşında öldü; naaşı Bursa'ya getirildi.",
  ["#tarih", "#cemsultan", "#osmanlı", "#osmanlıtarihi"]),
 "scenes": [
  intro("Bir padişah, kardeşi uzakta kalsın diye her yıl düşmanına 40 bin altın ödedi!", "40 BİN!", "HER YIL?!"),
  S("Yıl 1481. Fatih Sultan Mehmet ölür. İki oğlu, Bayezid ve Cem, aynı tahtı ister.", "palace",
    [A("bayezid", 0.28, "kavuk", "hips", "confident", scale=1.2), A("cem", 0.72, "sarik", "point", "confident", flip=True, scale=1.2)],
    [pop("TEK TAHT!", 0.5, 0.22, 2.5, 110, -6)]),
  S("Taht yarışını Bayezid kazanır. Cem 1482'de gemiyle Rodos'a, şövalyelere sığınır.", "sea",
    [], [{"type": "ship", "x": 0.3, "y": 0.87, "scale": 0.8, "anim": "bob", "to_x": 0.65, "move_dur": 4.0}, popf("RODOS!", 0.6, 0.22, 0.6, 120, 6)]),
  S("Misafir olduğunu sanır. Ama aslında rehindir! Bayezid şövalyelere yılda 40 bin duka altını öder: Kardeşim orada kalsın.", "palace",
    [A("cem", 0.3, "sarik", "shock", "shock", scale=1.2), A("bayezid", 0.72, "kavuk", "point", "smug", flip=True, scale=1.2)],
    [{"type": "coins", "x": 0.5, "y": 0.93, "delay": 2.5}, popf("REHİN!", 0.3, 0.2, 0.3, 120, -8)]),
  S(TURN + "Cem, Avrupa'da bir koz gibi elden ele geçer. Önce Fransa'daki kaleler, sonra Roma'da Papa'nın sarayı.", "palace",
    [A("cem", 0.4, "sarik", "shrug", "surprised", scale=1.35)], [popf("ELDEN ELE!", 0.6, 0.22, 0.3, 110, 6)], emotion="şaşkın"),
  S("Krallar onu Osmanlı'ya karşı kullanmayı hayal eder. Cem ise gurbette şiirler yazar.", "palace",
    [A("cem", 0.4, "sarik", "think", "sad", holds="scroll", scale=1.35)], [popf("GURBET...", 0.65, 0.22, 0.5, 100, -6)]),
  S("Yaklaşık 13 yıl sonra, 1495'te İtalya'da 35 yaşında ölür. Naaşı yıllar sonra Bursa'ya getirilir.", "plain",
    [A("cem", 0.4, "sarik", "sad", "sad", scale=1.3)], []),
  S("Günün dersi: Altından da olsa kafes, kafestir.", "palace",
    [A("cem", 0.45, "sarik", "think", "think", scale=1.35)], [{"type": "coins", "x": 0.75, "y": 0.93}, RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 021 Göbeklitepe
EP.append({"id": "021", "file": "021_gobeklitepe", "title": "Piramitlerden 7000 Yıl Yaşlı Tapınak", "year": "MÖ 9600",
 "caption": cap("Piramitlerden 7000 yıl önce, daha tarla bile yokken, insanlar Urfa'da dev taş sütunlar dikti 🪨🤯",
  "Şanlıurfa'daki Göbeklitepe yaklaşık 11.600 yıl önce, tarım, çanak çömlek ve yazı ortada yokken avcı-toplayıcılar tarafından yapıldı. "
  "1963'te bulunan taşlar önce ortaçağ mezarlığı sanıldı; 1995'te kazılara başlayan Alman arkeolog Klaus Schmidt yapının çok daha eski olduğunu gösterdi. "
  "T biçimli dev dikmelerde tilki, yaban domuzu ve akbaba kabartmaları var.",
  ["#tarih", "#göbeklitepe", "#şanlıurfa", "#arkeoloji"]),
 "scenes": [
  intro("Piramitlerden 7000 yıl önce, daha tarla bile yokken, insanlar Urfa'da dev taş sütunlar dikti!", "7000 YIL!", "TARLA YOK?!"),
  S("Şanlıurfa'da bir tepe: Göbeklitepe. 1963'te araştırmacılar buradaki kırık taşları görür ve ortaçağ mezarlığı sanar.", "desert",
    [A("arastirmaci", 0.35, "slouch", "think", "think", scale=1.25, y=0.9)], [pop("MEZARLIK?", 0.6, 0.22, 3.0, 110, -6)]),
  S("1995'te Alman arkeolog Klaus Schmidt gelir, kazmaya başlar ve gözlerine inanamaz.", "desert",
    [A("schmidt", 0.35, "slouch", "push", "effort", scale=1.25, y=0.9, pose2="shock", face2="shock", switch=0.6)],
    [{"type": "block", "x": 0.72, "y": 0.9, "scale": 1.2}, popf("VAY!", 0.65, 0.25, 0.65, 130, 8)]),
  S(TURN + "Yapı yaklaşık 11.600 yıllık! Henüz tarım yok, çömlek yok, yazı yok. Yapanlar avcı-toplayıcılar!", "desert",
    [A("avci", 0.35, None, "cheer", "happy", scale=1.3, y=0.9)],
    [{"type": "pyramid", "x": 0.78, "y": 0.9, "scale": 0.5}, popf("11.600 YIL!", 0.55, 0.22, 0.25, 110, -6)], emotion="şaşkın"),
  S("Tonlarca ağırlıkta, T biçimli dev taşlar dikerler. Üstlerinde tilki, yaban domuzu, akbaba kabartmaları var. Tekerlek bile yokken! Bel fıtığı garanti.", "desert",
    [A("avci", 0.25, None, "push", "effort", scale=1.2, y=0.9)], [{"type": "block", "x": 0.55, "y": 0.9, "scale": 1.3}, {"type": "block", "x": 0.8, "y": 0.9, "scale": 1.1}]),
  S("Önce tarla, sonra tapınak sanıyorduk. Bazı bilim insanlarına göre sıra tam tersi olabilir: Önce tapınak, sonra tarla!", "farm",
    [A("schmidt", 0.4, "slouch", "point", "confident", scale=1.35, y=0.9)], [{"type": "fence", "x1": 0.65, "x2": 1.0, "y": 0.9}, popf("TERSİ!", 0.65, 0.22, 0.75, 120, -6)]),
  S("Göbeklitepe bugün UNESCO Dünya Mirası ve dünyanın en eski anıtsal yapılarından biri.", "desert",
    [A("avci", 0.4, None, "open", "happy", scale=1.3, y=0.9)], [{"type": "sun", "x": 0.85, "y": 0.15}]),
  S("Günün dersi: Bildiğimizi sandığımız tarih, bir kazma darbesiyle değişebilir.", "desert",
    [A("schmidt", 0.45, "slouch", "think", "think", scale=1.35, y=0.9)], [{"type": "bulb", "actor": "schmidt", "delay": 1.0}, RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 022 Ali Kuşçu
EP.append({"id": "022", "file": "022_ali_kuscu", "title": "Kopernik'ten Önce \"Dünya Dönebilir\" Dedi!", "year": "1470'LER",
 "caption": cap("Kopernik'ten 70 yıl önce bir Türk bilgin yazdı: Dünya'nın döndüğünü hiçbir gözlem çürütemez 🌍🔭",
  "Ali Kuşçu Semerkant'ta doğdu; adını, babasının hükümdar Uluğ Bey'in doğancısı yani kuşçusu olmasından aldı. "
  "Uluğ Bey'in rasathanesinde çalıştı, sonra Fatih Sultan Mehmet'in davetiyle İstanbul'a geldi ve 1474'te burada öldü. "
  "Gökbilim üzerine yazdığı eserde, Dünya'nın dönüşünün gözlemle çürütülemeyeceğini savundu.",
  ["#tarih", "#alikuşçu", "#bilimtarihi", "#astronomi"]),
 "scenes": [
  intro("Kopernik'ten 70 yıl önce bir Türk bilgin şunu yazdı: Dünya dönüyor olabilir!", "KOPERNİK?", "70 YIL ÖNCE!"),
  S("1400'lerin başı, Semerkant. Ali'nin babası hükümdar Uluğ Bey'in doğancısıdır, yani kuşçusu. Soyadı hazır!", "palace",
    [A("ali", 0.38, "sarik", "point", "happy", scale=1.3)], [pop("KUŞÇU!", 0.65, 0.22, 3.0, 120, 6)]),
  S("Uluğ Bey hem hükümdar hem gökbilimci. Semerkant'ta dev bir rasathane kurar. Genç Ali de yıldızları ölçenler arasında.", "plain", night=True,
    actors=[A("ali", 0.4, "sarik", "think", "think", holds="scroll", scale=1.35)], props=[popf("RASATHANE!", 0.6, 0.22, 0.4, 100, -6)]),
  S(TURN + "O dönem herkes, Dünya kıpırdamaz der. Ali Kuşçu ise yazar: Dünya'nın döndüğünü hiçbir gözlem çürütemez!", "plain", night=True,
    actors=[A("ali", 0.35, "sarik", "point", "confident", scale=1.3, talk=True, pose2="hips", face2="smug", switch=0.7)],
    props=[popf("DÖNEBİLİR!", 0.6, 0.22, 0.6, 110, 6)], emotion="şaşkın"),
  S("Ünü yayılır. Fatih Sultan Mehmet onu İstanbul'a davet eder ve büyük bir maaşla Ayasofya'da ders verdirir.", "city",
    [A("fatih", 0.3, "kavuk", "open", "happy", scale=1.2), A("ali", 0.72, "sarik", "cheer", "happy", flip=True, scale=1.2)],
    [{"type": "coins", "x": 0.5, "y": 0.93, "delay": 2.5}]),
  S("Ali Kuşçu 1474'te İstanbul'da ölür. Kopernik'in ünlü kitabı ise ancak 1543'te çıkar.", "city",
    [A("ali", 0.4, "sarik", "hips", "confident", holds="scroll", scale=1.35)], [{"type": "tower", "x": 0.8, "y": 0.93, "scale": 0.8}, popf("1543!", 0.6, 0.22, 0.6, 120, -6)]),
  S("Günün dersi: Herkesin doğru bildiğini sorgulamak, bilimin ilk adımıdır.", "plain", night=True,
    actors=[A("ali", 0.45, "sarik", "think", "think", scale=1.35)], props=[{"type": "bulb", "actor": "ali", "delay": 1.0}, RIM], emotion="sakin"),
  outro()]})

for ep in EP:
    out = {"id": ep["id"], "series": "ÇÖP ADAMLA TARİH", "title": ep["title"], "year": ep["year"],
           "voice_fx": {"pitch": 1.15, "noise": 0.2, "noise_w": 0.3},
           "instagram_caption": ep["caption"], "scenes": ep["scenes"]}
    json.dump(out, open(os.path.join(ROOT, "episodes", ep["file"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    words = sum(len(s["say"].split()) for s in ep["scenes"])
    print("yazıldı:", ep["file"], len(ep["scenes"]), "sahne", words, "kelime")
