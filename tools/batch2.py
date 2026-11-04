"""İkinci bölüm paketini üretir (episodes/009..015). Ton: "karışık" (belgesel + hafif espri)."""
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


def cap(hook, info, question, tags):
    assert len(tags) == 4
    return f"{hook}\n\n{info}\n\n{question} Yorumlara yaz 👇\n{FOLLOW}\n\n" + " ".join(tags + [TAG])


EP = []

# ---------------------------------------------------------------- 009 Lale çılgınlığı
EP.append({"id": "009", "file": "009_lale_cilginligi", "title": "Bir Lale Soğanına Ev Verdiler!", "year": "1637",
 "caption": cap("Bir zamanlar tek bir çiçek soğanı, bir evden daha pahalıydı 🌷😳",
  "1630'larda Hollanda'da lale çılgınlığı yaşandı. İnsanlar henüz topraktaki soğanların kâğıtlarını meyhanelerde alıp sattı. "
  "En nadir lale Semper Augustus'un 10 soğanına 12.000 gulden teklif edildiği anlatılır; bu, Amsterdam'da lüks bir evden fazlaydı. "
  "Şubat 1637'de Haarlem'de alıcı çıkmayınca fiyatlar çöktü. Lalenin Avrupa'ya yolculuğu ise Osmanlı bahçelerinden başlamıştı.",
  "Sen bir çiçeğe ne kadar verirdin?", ["#tarih", "#lale", "#hollanda", "#tarihbilgisi"]),
 "scenes": [
  intro("Bir zamanlar tek bir çiçek soğanı, koca bir evden daha pahalıydı. Şaka değil!", "SOĞAN!", "EV FİYATINA?!"),
  S("Hikâye bizden başlıyor. 1500'lerde lale, Osmanlı bahçelerinin gözdesi. Avrupalı elçiler soğanları ülkelerine götürür.", "palace",
    [A("osmanli", 0.3, "sarik", "open", "happy", scale=1.25), A("elci", 0.72, None, "point", "surprised", flip=True, scale=1.2, holds="scroll")],
    [pop("LALE!", 0.5, 0.22, 3.0, 120, -6)]),
  S("Hollandalılar laleye âşık olur. En çok da alevli, çizgili desenlilere. Oysa o desenlerin sebebi bir virüsmüş!", "farm",
    [A("hollandali", 0.35, None, "cheer", "happy", scale=1.25, y=0.9, pose2="shock", face2="shock", switch=0.7)],
    [{"type": "fence", "x1": 0.6, "x2": 1.0, "y": 0.9}, popf("VİRÜS!", 0.68, 0.25, 0.8, 120, 6)]),
  S("1636'da çılgınlık başlar. İnsanlar meyhanelerde, daha topraktan çıkmamış soğanların kâğıtlarını alıp satar.", "plain",
    [A("tuccar1", 0.27, None, "point", "smug", holds="scroll", scale=1.15, talk=True), A("tuccar2", 0.72, None, "open", "happy", holds="mug", flip=True, scale=1.15)],
    [{"type": "coins", "x": 0.5, "y": 0.93, "delay": 2.0}, pop("KÂĞIT ÜSTÜNDE!", 0.5, 0.22, 3.0, 92, -5)]),
  S(TURN + "Anlatılana göre en nadir lalenin 10 soğanına 12 bin gulden teklif edilir. Amsterdam'da lüks bir evden fazla! Düşünsene, evini verip saksı alıyorsun.", "plain",
    [A("hollandali", 0.35, None, "shock", "shock", anim="shake", scale=1.3)],
    [{"type": "coins", "x": 0.72, "y": 0.93, "delay": 3.0}, popf("12.000 GULDEN!", 0.55, 0.22, 0.4, 92, 6)], emotion="şaşkın"),
  S("Ve Şubat 1637'de Haarlem'de bir açık artırmada kimse alıcı çıkmaz. Fiyatlar bir anda çöker.", "plain",
    [A("tuccar1", 0.4, None, "sad", "sad", holds="scroll", scale=1.3)], [popf("ÇÖKÜŞ!", 0.6, 0.22, 0.6, 130, -8)]),
  S("Gerçi bugün bazı tarihçiler, hikâyenin biraz abartıldığını söylüyor. Ama Hollanda hâlâ dünyanın lale ülkesi.", "farm",
    [A("hollandali", 0.4, None, "shrug", "happy", scale=1.3, y=0.9)], [{"type": "sun", "x": 0.85, "y": 0.15}]),
  S("Günün dersi: Herkes bir şeye koşuyorsa, önce dur ve düşün.", "farm",
    [A("hollandali", 0.45, None, "think", "think", scale=1.35, y=0.9)], [{"type": "bulb", "actor": "hollandali", "delay": 1.0}, RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 010 Kanuni
EP.append({"id": "010", "file": "010_kanuni", "title": "Avrupa'ya Göre \"Muhteşem\", Bize Göre \"Kanuni\"", "year": "1520",
 "caption": cap("Aynı padişaha Avrupa \"Muhteşem\" dedi, biz \"Kanuni\" 👑📜 Peki neden?",
  "I. Süleyman 1520'den 1566'ya kadar 46 yıl tahtta kaldı; bu Osmanlı'nın en uzun saltanatıdır. "
  "Avrupalılar onun gücüne ve sarayının ihtişamına bakıp \"Muhteşem\" dedi. Halkı ise dağınık kuralları toplatıp kanunnameler hazırlattığı için onu \"Kanuni\" diye andı. "
  "Üstelik \"Muhibbi\" mahlasıyla şiirler yazan bir şairdi!",
  "Sence hangisi daha güzel bir lakap?", ["#tarih", "#kanunisultansüleyman", "#osmanlı", "#osmanlıtarihi"]),
 "scenes": [
  intro("Aynı padişaha Avrupa Muhteşem dedi, biz Kanuni. Peki neden bir adama iki farklı isim?", "MUHTEŞEM?", "KANUNİ?!"),
  S("Yıl 1520. Süleyman tahta çıkar ve tam 46 yıl tahtta kalır. Osmanlı tarihinin en uzun saltanatı!", "palace",
    [A("suleyman", 0.4, "kavuk", "hips", "confident", scale=1.4)], [pop("46 YIL!", 0.72, 0.25, 3.0, 120, 6)]),
  S("Ordusu Belgrad'dan Bağdat'a, Viyana kapılarına kadar uzanır. Avrupa onun gücüne şaşkın.", "battlefield",
    [A("suleyman", 0.3, "kavuk", "point", "confident", scale=1.2, y=0.9)],
    [{"type": "horse", "x": 0.68, "y": 0.92, "scale": 0.85, "flip": True}, {"type": "tent", "x": 0.88, "y": 0.9, "scale": 0.6}, pop("VİYANA!", 0.55, 0.25, 2.8, 110, -6)]),
  S("Sarayının ihtişamını gören Avrupalı elçiler, ona Muhteşem Süleyman der. Gözleri kamaşmış resmen!", "palace",
    [A("elci", 0.28, None, "shock", "surprised", scale=1.15, holds="scroll"), A("suleyman", 0.72, "kavuk", "open", "smug", flip=True, scale=1.3)],
    [{"type": "coins", "x": 0.5, "y": 0.93, "delay": 1.5}, popf("MUHTEŞEM!", 0.5, 0.22, 0.4, 110, 6)]),
  S(TURN + "Kendi halkı onu savaşlarla değil, kanunlarla hatırlar.", "palace",
    [A("suleyman", 0.4, "kavuk", "think", "think", scale=1.35)], [{"type": "bulb", "actor": "suleyman", "f": 0.5}], emotion="şaşkın"),
  S("Dağınık kuralları toplatır, kanunnameler hazırlatır. Vergiden toprağa kadar her şey yazıya geçer. Yanında da Şeyhülislam Ebussuud Efendi.", "palace",
    [A("suleyman", 0.3, "kavuk", "point", "confident", scale=1.25, talk=True), A("ebussuud", 0.72, "sarik", "stand", "happy", holds="scroll", flip=True, scale=1.2)],
    [popf("KANUNNAME!", 0.5, 0.22, 0.3, 100, -6)]),
  S("Bir sürpriz daha: Muhibbi mahlasıyla şiirler yazardı. Hem cihan padişahı, hem şair. Mesai dolu!", "palace",
    [A("suleyman", 0.42, "kavuk", "point", "happy", holds="scroll", scale=1.35)], [popf("ŞAİR!", 0.7, 0.25, 0.4, 120, 8)]),
  S("Günün dersi: Kılıçla kazanılan yer, ancak adaletle korunur.", "palace",
    [A("suleyman", 0.45, "kavuk", "hips", "confident", scale=1.4)], [RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 011 Seyit Onbaşı
EP.append({"id": "011", "file": "011_seyit_onbasi", "title": "Vinç Bozuldu, Seyit Onbaşı Durmadı!", "year": "1915",
 "caption": cap("Bir asker 215 kiloluk top mermisini sırtladı 💪 Hem de üç kere!",
  "18 Mart 1915'te Çanakkale'de Rumeli Mecidiye Tabyası'nın mermi vinci bozulunca, Balıkesir Havranlı topçu Seyit Ali mermileri sırtında taşıyıp topa sürdü. "
  "Anlatılana göre bu mermilerden biri Ocean zırhlısını vurdu; bazı tarihçiler ise geminin mayına çarptığını söyler. "
  "Kesin olan şu: O gün düşman donanması boğazı geçemedi.",
  "Sen hiç kendini aşacak kadar güçlü hissettin mi?", ["#tarih", "#çanakkale", "#seyitonbaşı", "#18mart"]),
 "scenes": [
  intro("Bir asker, 215 kiloluk bir top mermisini sırtladı. Hem de üç kere!", "215 KİLO!", "ÜÇ KERE?!"),
  S("18 Mart 1915. Dev İngiliz ve Fransız gemileri Çanakkale Boğazı'nı geçmek için yola çıkar.", "battlefield",
    [A("seyit", 0.3, None, "point", "surprised", scale=1.25, y=0.9)], [pop("DEV DONANMA!", 0.6, 0.25, 2.5, 96, -5)]),
  S("Rumeli Mecidiye Tabyası'nda topçular hazır. Aralarında Balıkesir Havranlı Seyit Ali var. Herkes ona Koca Seyit der.", "battlefield",
    [A("seyit", 0.35, None, "hips", "confident", scale=1.35, y=0.9)], [popf("KOCA SEYİT!", 0.65, 0.22, 0.6, 100, 6)]),
  S("Ama atışlar sırasında tabyanın vinci bozulur. Dev mermiler yerden kalkmıyor!", "battlefield",
    [A("seyit", 0.35, None, "shock", "shock", scale=1.25, y=0.9, anim="shake")],
    [{"type": "block", "x": 0.7, "y": 0.9, "scale": 1.6}, popf("VİNÇ BOZULDU!", 0.55, 0.22, 0.5, 96, -6)]),
  S(TURN + "Seyit mermiyi sırtına alır, merdivenleri tırmanır ve topa sürer. Bir, iki, üç!", "battlefield",
    [A("seyit", 0.25, None, "push", "effort", scale=1.2, y=0.9, anim="walk", to_x=0.5, move_dur=5)],
    [{"type": "block", "x": 0.37, "y": 0.9, "scale": 1.4, "to_x": 0.62, "move_dur": 5}, popf("HEYYT!", 0.65, 0.22, 0.7, 120, 8)], emotion="şaşkın"),
  S("Anlatılana göre bu mermilerden biri Ocean zırhlısını vurdu. Bazı tarihçiler geminin mayına çarptığını söyler. Kesin olan şu: Düşman boğazı geçemedi.", "battlefield",
    [A("seyit", 0.3, None, "cheer", "happy", scale=1.25, y=0.9, anim="bounce")],
    [{"type": "sign", "x": 0.72, "y": 0.6, "text": "ÇANAKKALE"}, popf("GEÇİLEMEDİ!", 0.5, 0.22, 0.75, 110, -6)]),
  S("Sonra fotoğrafı çekilecek, mermiyi yeniden kaldırması istenir. Kaldıramaz! Rivayete göre şöyle der: Savaş olursa yine kaldırırım.", "plain",
    [A("seyit", 0.35, None, "shrug", "happy", scale=1.3, talk=True)],
    [{"type": "bubble", "text": "Savaş olursa yine kaldırırım!", "x": 0.55, "y": 0.13, "tx": 0.38, "ty": 0.3, "f": 0.6}]),
  S("Günün dersi: Bazen güç kaslardan değil, yürekten gelir.", "battlefield",
    [A("seyit", 0.45, None, "cheer", "happy", scale=1.35, y=0.9)], [{"type": "flag", "actor": "seyit", "emblem": True}, RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 012 Harezmi
EP.append({"id": "012", "file": "012_harezmi_algoritma", "title": "Bilgisayarın Dedesi Bir Matematikçi", "year": "820'LER",
 "caption": cap("Telefonundaki her uygulama, 1200 yıl önce yaşamış bir bilginin adını taşıyor 📱🤯",
  "Harezmi 800'lerde Bağdat'taki Beytülhikme'de çalıştı. Denklemleri adım adım çözdüğü kitabındaki \"el-cebr\" kelimesi bugünkü \"cebir\" oldu. "
  "Hint rakamlarını anlatan kitabının Latince çevirisi \"Dixit Algorizmi\" (Algoritmi dedi ki) diye başlıyordu; \"algoritma\" kelimesi buradan geliyor. "
  "Bu kitap sıfırlı rakamların Avrupa'ya yayılmasına da yardım etti.",
  "Matematik mi seversin, tarih mi?", ["#tarih", "#harezmi", "#matematik", "#bilimtarihi"]),
 "scenes": [
  intro("Telefonundaki her uygulama, 1200 yıl önce yaşamış bir adamın adını taşıyor.", "1200 YIL!", "KİMİN ADI?!"),
  S("Yıl 820'ler, Bağdat. Beytülhikme'de, yani Bilgelik Evi'nde, dünyanın dört bir yanından kitaplar çevriliyor.", "palace",
    [A("katip", 0.3, "sarik", "stand", "happy", holds="scroll", scale=1.2), A("katip2", 0.72, "sarik", "point", "happy", flip=True, scale=1.2)],
    [pop("BİLGELİK EVİ!", 0.5, 0.22, 3.0, 96, -6)]),
  S("Burada bir bilgin çalışıyor: Harezmi. Adını Orta Asya'daki memleketi Harezm'den alıyor.", "palace",
    [A("harezmi", 0.4, "sarik", "think", "think", scale=1.35, pose2="point", face2="confident", switch=0.6)],
    [{"type": "bulb", "actor": "harezmi", "f": 0.6}]),
  S("Harezmi, denklemleri adım adım çözmeyi bir kitapta anlatır. Kitabın adındaki el-cebr kelimesi, bugünkü cebir olur.", "plain",
    [A("harezmi", 0.35, "sarik", "point", "confident", holds="scroll", scale=1.3, talk=True)],
    [{"type": "sign", "x": 0.75, "y": 0.6, "text": "x + 3 = 5"}, popf("CEBİR!", 0.62, 0.22, 0.7, 120, 6)]),
  S(TURN + "Hint rakamlarını anlattığı kitap Latinceye çevrilir. İlk cümlesi: Algoritmi dedi ki.", "plain",
    [A("kesis", 0.4, None, "shock", "surprised", holds="scroll", scale=1.3)], [popf("ALGORİTMİ!", 0.6, 0.22, 0.6, 110, -6)], emotion="şaşkın"),
  S("Avrupalılar onun adını, adım adım hesap yöntemine verir: Algoritma! Aynı kitap, sıfırlı rakamların Avrupa'ya yayılmasına da yardım eder.", "plain",
    [A("kesis", 0.3, None, "cheer", "happy", anim="bounce", scale=1.2), A("harezmi", 0.72, "sarik", "hips", "smug", flip=True, scale=1.25)],
    [popf("ALGORİTMA!", 0.5, 0.22, 0.25, 110, 6)]),
  S("Düşünsene, sıfırsız Romen rakamlarıyla çarpma yapıyorsun. Kafa duman!", "plain",
    [A("kesis", 0.4, None, "shock", "shock", anim="shake", scale=1.3)], [{"type": "sign", "x": 0.72, "y": 0.6, "text": "MCMXC x XIV = ?"}]),
  S("Günün dersi: İyi bir fikir, bin yıl sonra bile cebinde çalışır.", "palace",
    [A("harezmi", 0.45, "sarik", "open", "happy", scale=1.4)], [RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 013 Viking boynuzları
EP.append({"id": "013", "file": "013_viking_boynuz", "title": "Vikinglerin Boynuzu Yoktu!", "year": "800'LER",
 "caption": cap("Boynuzlu Viking miğferi mi? Bunu tarihe değil, bir operaya borçluyuz 🎭",
  "Arkeologlar bugüne kadar boynuzlu tek bir Viking savaş miğferi bulmadı. En sağlam Viking miğferi, 1943'te Norveç'te bulunan yuvarlak ve sade Gjermundbu miğferidir. "
  "Boynuzlar 1876'da Wagner'in operası için kostüm tasarımcısı Carl Emil Doepler'in çizimleriyle ünlendi.",
  "Sen de boynuzlu sanıyor muydun?", ["#tarih", "#vikingler", "#tarihbilgisi", "#efsane"]),
 "scenes": [
  intro("Vikingleri boynuzlu miğferle hayal ediyorsan, bunu tarihe değil, bir operaya borçlusun.", "BOYNUZ?", "OPERA MI?!"),
  S("800'lerden itibaren Vikingler İskandinavya'dan gemilerle yola çıkar. İngiltere'den Bizans'a kadar her yere uğrarlar.", "plain",
    [A("viking", 0.2, "helmet", "point", "confident", scale=1.3, anim="walk", to_x=0.45, move_dur=4)],
    [pop("VİKİNGLER!", 0.6, 0.25, 2.5, 110, -6)]),
  S("Hatta bazıları İstanbul'da Bizans imparatorunun muhafızı olur. Onlara Varank Muhafızları denir.", "palace",
    [A("imparator", 0.3, "crown", "hips", "confident", scale=1.2), A("viking", 0.72, "helmet", "stand", "confident", flip=True, scale=1.4)],
    [popf("VARANK!", 0.55, 0.22, 0.6, 120, 6)]),
  S("Peki ya boynuzlar? Arkeologlar bugüne kadar boynuzlu tek bir Viking savaş miğferi bulmadı.", "plain",
    [A("arkeolog", 0.4, "slouch", "shrug", "surprised", holds="scroll", scale=1.3)], [popf("SIFIR BOYNUZ!", 0.6, 0.22, 0.6, 96, -6)]),
  S(TURN + "En sağlam Viking miğferi, 1943'te Norveç'te bulunan Gjermundbu miğferi. Yuvarlak, sade ve boynuzsuz!", "plain",
    [A("viking", 0.4, "helmet", "hips", "smug", scale=1.4)], [popf("BOYNUZSUZ!", 0.62, 0.22, 0.7, 110, 6)], emotion="şaşkın",
    text=None),
  S("Boynuzlar 1876'da sahneye çıkar. Wagner'in operasında kostüm tasarımcısı Carl Emil Doepler, Viking kahramanlara boynuz takar. Ve moda tutar!", "palace",
    [A("doepler", 0.35, "tophat", "point", "smug", holds="scroll", scale=1.3, talk=True)], [popf("1876!", 0.68, 0.25, 0.2, 130, -8)]),
  S("Boynuzlu miğferler aslında Vikinglerden çok önce, törenlerde kullanılırdı. Savaşta mı? Boynuzun bir dala takılır, kalırsın!", "plain",
    [A("viking", 0.4, "helmet", "shock", "shock", anim="shake", scale=1.3)], [{"type": "palm", "x": 0.78, "y": 0.93, "scale": 0.9}]),
  S("Günün dersi: Bir şeyi çok sık görmen, onu doğru yapmaz.", "plain",
    [A("viking", 0.45, "helmet", "think", "think", scale=1.4)], [RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 014 Kleopatra
EP.append({"id": "014", "file": "014_kleopatra_zaman", "title": "Kleopatra, Piramitlerden Çok Bize Yakın!", "year": "MÖ 30",
 "caption": cap("Kleopatra, Büyük Piramit'in yapılışından çok Ay'a inişe yakın yaşadı 🌙🔺",
  "Büyük Piramit yaklaşık MÖ 2560'ta yapıldı, Kleopatra MÖ 30'da öldü: Arada yaklaşık 2500 yıl var. Ay'a iniş ise 1969'da, Kleopatra'dan yaklaşık 2000 yıl sonra. "
  "Kleopatra Makedon kökenli Ptolemaios hanedanındandı; Plutarkhos'a göre ailesinde Mısır dilini öğrenen ilk kişiydi.",
  "Bu bilgi seni de şaşırttı mı?", ["#tarih", "#kleopatra", "#antikmısır", "#piramitler"]),
 "scenes": [
  intro("Kleopatra, piramitlerin yapılışına değil, Ay'a inişe daha yakın bir zamanda yaşadı.", "KLEOPATRA!", "AY'A İNİŞ?!"),
  S("Gize'deki Büyük Piramit, milattan önce yaklaşık 2560'ta yapıldı.", "desert",
    [A("firavun", 0.28, "nemes", "point", "confident", scale=1.25, y=0.9)],
    [{"type": "sun", "x": 0.85, "y": 0.15}, {"type": "pyramid", "x": 0.7, "y": 0.88, "scale": 1.0}],
    text="Gize'deki Büyük Piramit, MÖ yaklaşık 2560'ta yapıldı."),
  S("Kleopatra ise milattan önce 30'da öldü. Arada yaklaşık 2500 yıl var!", "desert",
    [A("kleopatra", 0.3, "crown", "hips", "confident", scale=1.3, y=0.9)],
    [{"type": "pyramid", "x": 0.75, "y": 0.88, "scale": 0.7}, popf("2500 YIL!", 0.6, 0.25, 0.6, 120, 6)],
    text="Kleopatra ise MÖ 30'da öldü. Arada yaklaşık 2500 yıl var!"),
  S("Ay'a iniş ise 1969'da. Kleopatra'dan sadece 2000 yıl sonra!", "plain",
    [A("astronot", 0.4, None, "cheer", "happy", anim="bounce", scale=1.3)], [popf("1969!", 0.65, 0.25, 0.3, 130, -6)], night=True),
  S(TURN + "Kleopatra için bile piramitler antikaydı. Turist gibi gezip bakacağı eski eserler!", "desert",
    [A("kleopatra", 0.3, "crown", "point", "surprised", scale=1.25, y=0.9)],
    [{"type": "pyramid", "x": 0.72, "y": 0.88, "scale": 0.9}, {"type": "palm", "x": 0.93, "y": 0.9, "scale": 0.7}, popf("ANTİKA!", 0.55, 0.22, 0.6, 120, 8)],
    emotion="şaşkın"),
  S("Üstelik Kleopatra'nın ailesi Makedon kökenliydi. Plutarkhos'a göre ailesinde Mısır dilini öğrenen ilk kişi oydu.", "palace",
    [A("kleopatra", 0.4, "crown", "open", "smug", holds="scroll", scale=1.35)], [popf("MAKEDON!", 0.65, 0.22, 0.3, 110, -6)]),
  S("Bir şok daha: Piramitler yapılırken Sibirya açıklarındaki Wrangel Adası'nda hâlâ mamutlar yaşıyordu!", "plain",
    [A("arkeolog", 0.4, "slouch", "shock", "shock", anim="shake", scale=1.3)], [popf("MAMUT!", 0.65, 0.25, 0.75, 130, 6)]),
  S("Günün dersi: Tarih sandığından çok daha uzun, ve sen onun en yeni sayfasısın.", "desert",
    [A("kleopatra", 0.3, "crown", "relax", "happy", scale=1.25, y=0.9)], [{"type": "pyramid", "x": 0.72, "y": 0.88, "scale": 0.9}, RIM], emotion="sakin"),
  outro()]})

# ---------------------------------------------------------------- 015 Piri Reis
EP.append({"id": "015", "file": "015_piri_reis", "title": "500 Yıllık Esrarengiz Harita", "year": "1513",
 "caption": cap("1929'da Topkapı Sarayı'nda unutulmuş bir harita bulundu. Üstünde 1513'te çizilmiş bir Amerika vardı! 🗺️",
  "Osmanlı denizcisi Piri Reis, 1513'te Gelibolu'da ceylan derisi üzerine bir dünya haritası çizdi. Yaklaşık 20 kaynaktan yararlandı; bunlardan biri bugün kayıp olan bir Kristof Kolomb haritasıydı. "
  "Haritanın yalnızca üçte biri bugüne ulaştı ve Topkapı Sarayı Müzesi'nde saklanıyor. \"Buzsuz Antarktika\" iddiası ise bilim insanlarına göre bir efsane.",
  "Haritalar mı, gemiler mi?", ["#tarih", "#pirireis", "#osmanlı", "#harita"]),
 "scenes": [
  intro("1929'da bir sarayda unutulmuş bir harita bulundu. Üstünde 1513'te çizilmiş bir Amerika vardı!", "1929!", "AMERİKA?!"),
  S("Haritayı çizen Piri Reis. Gençliğini amcası Kemal Reis'le Akdeniz'de gemilerde geçiren bir Osmanlı denizcisi.", "sea",
    [], [{"type": "ship", "x": 0.5, "y": 0.87, "scale": 0.85, "anim": "bob"}, pop("PİRİ REİS!", 0.5, 0.22, 2.0, 110, -6)]),
  S("1513'te Gelibolu'da oturur ve bir dünya haritası çizer. Hem de ceylan derisi üzerine!", "plain",
    [A("piri", 0.4, "sarik", "think", "think", holds="scroll", scale=1.35, pose2="cheer", face2="happy", switch=0.6)],
    [popf("CEYLAN DERİSİ!", 0.55, 0.22, 0.7, 92, 6)]),
  S(TURN + "Haritayı yaklaşık 20 kaynaktan derler. Bunlardan biri, bugün kayıp olan bir Kristof Kolomb haritası!", "plain",
    [A("piri", 0.3, "sarik", "point", "confident", holds="scroll", scale=1.25, talk=True)],
    [{"type": "sign", "x": 0.72, "y": 0.6, "text": "KOLOMB"}, popf("20 KAYNAK!", 0.6, 0.22, 0.35, 100, -6)], emotion="şaşkın"),
  S("Yani Kolomb'un kaybolan haritasının izleri, bugün bir Osmanlı haritasında yaşıyor.", "sea",
    [], [{"type": "ship", "x": 0.4, "y": 0.87, "scale": 0.7, "anim": "bob"}, popf("KAYIP İZ!", 0.6, 0.25, 0.4, 110, 6)]),
  S("Haritanın sadece üçte biri bugüne ulaştı. Bazıları altta buzsuz Antarktika olduğunu, hatta uzaylıların çizdiğini iddia eder. Bilim insanlarına göre bu bir efsane. Çizen Piri Reis!", "plain",
    [A("piri", 0.4, "sarik", "hips", "smug", scale=1.35)], [popf("UZAYLI DEĞİL!", 0.6, 0.22, 0.7, 96, -6)]),
  S("Haritası bugün Topkapı Sarayı Müzesi'nde saklanıyor. Piri Reis denizciler için Kitab-ı Bahriye'yi de yazdı.", "city",
    [A("piri", 0.35, "sarik", "open", "happy", holds="scroll", scale=1.3)], [{"type": "tower", "x": 0.8, "y": 0.93, "scale": 0.8}]),
  S("Günün dersi: Herkesten bir parça öğrenen, yepyeni bir dünya çizer.", "sea",
    [], [{"type": "ship", "x": 0.5, "y": 0.87, "scale": 0.85, "anim": "bob"}, RIM], emotion="sakin"),
  outro()]})

for ep in EP:
    out = {"id": ep["id"], "series": "ÇÖP ADAMLA TARİH", "title": ep["title"], "year": ep["year"],
           "voice_fx": {"pitch": 1.15, "noise": 0.2, "noise_w": 0.3},
           "instagram_caption": ep["caption"], "scenes": ep["scenes"]}
    json.dump(out, open(os.path.join(ROOT, "episodes", ep["file"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    words = sum(len(s["say"].split()) for s in ep["scenes"])
    print("yazıldı:", ep["file"], len(ep["scenes"]), "sahne", words, "kelime")
