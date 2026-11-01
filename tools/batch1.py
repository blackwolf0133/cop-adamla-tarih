"""İlk bölüm paketini üretir (episodes/002..008)."""
import json, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAG = "#çöpadamlatarih"

def intro(say, text, pop1, pop2):
    return {"say": say, "text": text, "voice_delay": 1.0,
            "narrator": {"x": 0.5, "y": 0.97, "scale": 1.6, "pose": "wave", "face": "happy",
                         "beats": [{"t": 0.45, "pose": "point", "face": "wink"}, {"f": 0.0, "pose": "hips", "face": "happy"},
                                   {"f": 0.3, "pose": "think", "face": "think"}, {"f": 0.6, "pose": "open", "face": "surprised"},
                                   {"f": 0.85, "pose": "shrug", "face": "happy"}]},
            "props": [{"type": "pop", "text": pop1, "x": 0.25, "y": 0.15, "size": 130, "f": 0.0, "rot": -10, "until_f": 0.55},
                      {"type": "pop", "text": pop2, "x": 0.5, "y": 0.13, "size": 92, "f": 0.6, "rot": 5}]}

def outro(say="İşte böyle! Yarın yepyeni bir hikâye var. Takip et, kaçırma!",
          text="İşte böyle! Yarın yepyeni bir hikâye var. Takip et, kaçırma!"):
    return {"say": say, "text": text, "voice_delay": 0.5,
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

EP = []

# ---------------------------------------------------------------- 002 Malazgirt
EP.append({"id": "002", "file": "002_malazgirt", "title": "Alparslan Bizans İmparatorunu Nasıl Şok Etti?", "year": "1071",
 "caption": ("Esir düşen imparatora sordu: \"Ben senin elinde olsaydım ne yapardın?\" Cevap korkunçtu... Alparslan'ın cevabı ise efsane 😎\n\n"
  "26 Ağustos 1071'de Malazgirt'te Büyük Selçuklu Sultanı Alparslan, kendisinden çok daha kalabalık Bizans ordusunu yendi ve İmparator Romen Diyojen'i esir aldı. "
  "Sonra onu affedip hediyelerle serbest bıraktı. Bu zafer Anadolu'nun kapılarını Türklere açtı.\n\n"
  "Sen olsan ne yapardın? Yorumlara yaz 👇\nHer gün yeni bir tarih hikâyesi için takip et 📚\n\n"
  f"#tarih #malazgirt #alparslan #selçuklu {TAG}"),
 "scenes": [
  intro("Dur! Bir imparator esir düştü ve ona öyle bir ceza verildi ki, hâlâ konuşuluyor!",
        "Dur! Bir imparator esir düştü ve ona öyle bir ceza verildi ki... hâlâ konuşuluyor!", "DUR!", "NASIL BİR CEZA?!"),
  S("Yıl 1071. Bizans İmparatoru Romen Diyojen, kocaman bir orduyla doğuya yürüyor.", "battlefield",
    [A("romen", 0.62, "crown", "point", "confident", flip=True, scale=1.25, enter="right")],
    [{"type": "tent", "x": 0.85, "y": 0.9, "scale": 0.7}, pop("KOCAMAN ORDU!", 0.35, 0.25, 2.5, 90, -6)]),
  S("Karşısında Büyük Selçuklu Sultanı Alparslan var. Ordusu çok daha küçük, ama kafası çok çalışıyor.", "battlefield",
    [A("alparslan", 0.35, "selcuk", "think", "think", scale=1.3, pose2="point", face2="confident", switch=0.6)],
    [{"type": "horse", "x": 0.72, "y": 0.92, "scale": 0.85, "flip": True}, {"type": "bulb", "actor": "alparslan", "delay": 3.2}]),
  S("Ve 26 Ağustos 1071'de Malazgirt'te savaş başlar. Selçuklular sahte geri çekilir, Bizans peşlerine takılır, sonra sürpriz!", "battlefield",
    [A("alparslan", 0.25, "selcuk", "cheer", "confident", holds="sword", anim="bounce", scale=1.15),
     A("romen", 0.8, "crown", "shock", "shock", flip=True, anim="shake", scale=1.1)],
    [{"type": "horse", "x": 0.5, "y": 0.92, "scale": 0.8, "anim": "gallop", "to_x": 0.6, "move_dur": 4}, pop("SÜRPRİZ!", 0.5, 0.25, 3.8, 110, 8)]),
  S("Sonuç? Bizans ordusu dağılır, imparator da esir düşer.", "battlefield",
    [A("romen", 0.6, "crown", "sad", "sad", flip=True, scale=1.25)], [pop("ESİR!", 0.6, 0.22, 1.5, 120, -5)]),
  S("Alparslan sorar: Ben senin elinde olsaydım ne yapardın? İmparator dürüst: Ya öldürürdüm, ya da zincirle sokaklarda gezdirirdim.", "palace",
    [A("alparslan", 0.25, "selcuk", "hips", "confident", scale=1.2, talk=True), A("romen", 0.75, "crown", "shrug", "sad", flip=True, scale=1.2)],
    [{"type": "bubble", "text": "Ne yapardın?", "x": 0.3, "y": 0.13, "tx": 0.27, "ty": 0.3, "delay": 0.5}]),
  S("Alparslan gülümser: Benim cezam daha ağır. Seni affediyorum! Ve imparatoru hediyelerle serbest bırakır.", "palace",
    [A("alparslan", 0.3, "selcuk", "open", "happy", scale=1.25), A("romen", 0.75, "crown", "shock", "shock", flip=True, scale=1.2, anim="shake")],
    [pop("AFFEDİLDİN!", 0.5, 0.2, 3.0, 110, -6), {"type": "coins", "x": 0.55, "y": 0.93, "delay": 4.0}]),
  S("Bu zafer, Anadolu'nun kapılarını Türklere açtı. Günün dersi: Bazen en büyük güç, affetmektir.", "battlefield",
    [A("alparslan", 0.45, "selcuk", "cheer", "happy", anim="bounce", scale=1.3)],
    [{"type": "flag", "actor": "alparslan", "emblem": False}, {"type": "sfx", "name": "rimshot", "f": 0.75}]),
  outro()]})

# ---------------------------------------------------------------- 003 Piramit
EP.append({"id": "003", "file": "003_piramit_iscileri", "title": "Piramitleri Kim Yaptı? Cevap: Biracılar!", "year": "MÖ 2560",
 "caption": ("Piramitleri köleler yaptı sanıyorsan yanılıyorsun 😅 Maaşlarını ekmek ve birayla alan işçiler yaptı!\n\n"
  "Gize'deki Büyük Piramit yaklaşık 4500 yıl önce Firavun Keops için inşa edildi. Arkeologlar işçilerin köyünü, fırınlarını ve mezarlarını buldu. "
  "Kayıtlara göre işçilere her gün ekmek ve bira tayını veriliyordu.\n\n"
  "Sen olsan bu maaşla çalışır mıydın? Yorumlara yaz 👇\nHer gün yeni bir tarih hikâyesi için takip et 📚\n\n"
  f"#tarih #mısır #piramitler #antikmısır {TAG}"),
 "scenes": [
  intro("Dur, kaydırma! Piramitleri köleler mi yaptı? Hayır! Maaşını birayla alan işçiler yaptı!",
        "Dur, kaydırma! Piramitleri köleler mi yaptı? Hayır! Maaşını birayla alan işçiler yaptı!", "DUR!", "BİRA MAAŞI?!"),
  S("Yaklaşık 4500 yıl önce Mısır. Firavun Keops kendine kocaman bir mezar istiyor.", "desert",
    [A("keops", 0.3, "nemes", "point", "confident", scale=1.3, y=0.9)],
    [{"type": "sun", "x": 0.85, "y": 0.15}, {"type": "pyramid", "x": 0.72, "y": 0.88, "scale": 1.0, "progress": 0.15},
     pop("KOCAMAN!", 0.7, 0.3, 3.0, 100, 6)]),
  S("Ama bu bildiğin mezar değil. Yaklaşık iki milyon taş blok, her biri bir otomobilden ağır!", "desert",
    [A("isci1", 0.2, None, "push", "effort", anim="walk", scale=1.0, y=0.9, to_x=0.42, move_dur=5)],
    [{"type": "sun", "x": 0.85, "y": 0.15}, {"type": "block", "x": 0.32, "y": 0.9, "scale": 1.2, "to_x": 0.54, "move_dur": 5},
     {"type": "pyramid", "x": 0.78, "y": 0.88, "scale": 0.8, "build": 20}, pop("2 MİLYON TAŞ!", 0.5, 0.25, 2.6, 96, -5)]),
  S("Uzun süre bunu kölelerin yaptığı sanıldı. Ama arkeologlar işçilerin köyünü, fırınlarını, hatta mezarlarını buldu.", "desert",
    [A("arkeolog", 0.35, "slouch", "shock", "surprised", scale=1.2, y=0.9, holds="scroll")],
    [{"type": "palm", "x": 0.85, "y": 0.9, "scale": 0.9}, pop("KÖLE DEĞİLLER!", 0.55, 0.25, 4.5, 96, 6)]),
  S("Peki maaşları ne? Ekmek ve bira! Kayıtlara göre her gün bira tayınları dağıtılıyordu.", "desert",
    [A("isci1", 0.3, None, "cheer", "happy", holds="mug", anim="bounce", scale=1.15, y=0.9),
     A("isci2", 0.65, None, "cheer", "happy", holds="mug", anim="bounce", scale=1.15, y=0.9, flip=True)],
    [{"type": "sun", "x": 0.85, "y": 0.15}, pop("ŞEREFE!", 0.5, 0.22, 2.2, 120, -8)]),
  S("Bu bira bugünkü gibi değildi tabii. Koyu, besleyici, neredeyse bir öğün gibiydi. Sıcakta çalışanlar için enerji deposu!", "desert",
    [A("isci1", 0.4, None, "hips", "smug", holds="mug", scale=1.3, y=0.9)],
    [{"type": "sun", "x": 0.85, "y": 0.15}, {"type": "pyramid", "x": 0.8, "y": 0.88, "scale": 0.6, "progress": 0.6}]),
  S("Firavunun ise tek derdi vardı: Mezarım ne zaman bitecek?", "desert",
    [A("keops", 0.3, "nemes", "hips", "sad", scale=1.25, y=0.9, talk=True)],
    [{"type": "pyramid", "x": 0.72, "y": 0.88, "scale": 1.0, "progress": 0.9},
     {"type": "bubble", "text": "Bitmedi mi hâlâ?", "x": 0.4, "y": 0.13, "tx": 0.32, "ty": 0.3, "delay": 0.8}]),
  S("Sonuç: Dünyanın yedi harikasından bugün hâlâ ayakta kalan tek eser. Günün dersi: İyi doyurulan ekip, harikalar yaratır!", "desert",
    [A("keops", 0.22, "nemes", "cheer", "happy", anim="bounce", scale=1.1, y=0.9)],
    [{"type": "sun", "x": 0.85, "y": 0.15}, {"type": "pyramid", "x": 0.65, "y": 0.88, "scale": 1.1}, {"type": "sfx", "name": "rimshot", "f": 0.75}]),
  outro()]})

# ---------------------------------------------------------------- 004 Napolyon
EP.append({"id": "004", "file": "004_napolyon_boyu", "title": "Napolyon Aslında Kısa Değildi!", "year": "1769",
 "caption": ("Napolyon kısa boyluydu, değil mi? Değil! 😅 İki asırdır süren bir yanlış anlaşılma...\n\n"
  "Napolyon yaklaşık 1,69 boyundaydı; dönemin Fransız erkek ortalamasından biraz bile uzundu. "
  "Efsanenin sebebi Fransız ve İngiliz ölçü birimlerinin karışması, İngiliz karikatüristlerin onu minik çizmesi ve 'Küçük Onbaşı' lakabı.\n\n"
  "Sen de kısa sanıyor muydun? Yorumlara yaz 👇\nHer gün yeni bir tarih hikâyesi için takip et 📚\n\n"
  f"#tarih #napolyon #fransa #tarihbilgisi {TAG}"),
 "scenes": [
  intro("Dur! Napolyon kısa boyluydu sanıyorsan, iki yüz yıldır kandırılıyorsun!",
        "Dur! Napolyon kısa boyluydu sanıyorsan, 200 yıldır kandırılıyorsun!", "DUR!", "KANDIRILDIK MI?!"),
  S("Napolyon Bonapart. Avrupa'nın yarısını fetheden Fransız imparatoru. Ve herkes onu kısacık biri olarak hatırlar.", "palace",
    [A("napolyon", 0.4, "bicorne", "hips", "confident", scale=1.35)], [pop("MİNİK Mİ?", 0.72, 0.25, 4.0, 100, 6)]),
  S("Peki gerçek ne? Napolyon yaklaşık bir altmış dokuz boyundaydı. O dönemin Fransız erkeklerinden biraz bile uzundu!", "plain",
    [A("napolyon", 0.3, "bicorne", "point", "smug", scale=1.35)],
    [{"type": "ruler", "x": 0.58, "y_top": 0.18, "labels": [[0.62, "1,65 ortalama"], [0.72, "1,69 Napolyon"]]},
     pop("1,69!", 0.25, 0.2, 3.5, 120, -6)],
    text="Peki gerçek ne? Napolyon yaklaşık 1,69 boyundaydı. O dönemin Fransız erkeklerinden biraz bile uzundu!"),
  S("Karışıklığın ilk sebebi: Ölçü birimi! Fransız inçi, İngiliz inçinden daha uzundu. Kayıtlar çevrilince Napolyon bir anda kısaldı.", "plain",
    [A("katip", 0.3, None, "think", "think", holds="scroll", scale=1.2, pose2="shock", face2="shock", switch=0.6)],
    [pop("İNÇ KARIŞTI!", 0.65, 0.25, 4.5, 96, 6)]),
  S("İkinci sebep: İngiliz karikatüristler! Napolyon'u hep öfkeli, minicik bir adam olarak çizdiler. Kısacası, ilk trollenen imparator oldu.", "plain",
    [A("napolyon", 0.35, "bicorne", "shock", "shock", scale=0.75, anim="shake"), A("ingiliz", 0.72, "tophat", "point", "smug", flip=True, scale=1.3, talk=True)],
    [pop("TROLL!", 0.5, 0.22, 5.0, 120, -8)]),
  S("Üçüncü sebep: Askerleri ona Küçük Onbaşı derdi. Ama bu bir sevgi lakabıydı, boyla ilgisi yoktu.", "plain",
    [A("asker", 0.3, "bicorne", "cheer", "happy", scale=1.1), A("napolyon", 0.7, "bicorne", "hips", "happy", flip=True, scale=1.2)],
    [{"type": "bubble", "text": "Küçük Onbaşı!", "x": 0.35, "y": 0.13, "tx": 0.3, "ty": 0.3, "delay": 0.6}]),
  S("Bir de etrafındaki muhafızlar özellikle uzun boylu seçilirdi. Yanlarında herkes kısa görünürdü!", "plain",
    [A("muhafiz1", 0.2, "bicorne", "stand", "neutral", scale=1.5), A("napolyon", 0.5, "bicorne", "shrug", "sad", scale=1.15),
     A("muhafiz2", 0.8, "bicorne", "stand", "neutral", scale=1.5, flip=True)], []),
  S("Günün dersi: Bir yalanı yeterince tekrarlarsan, iki yüz yıl yaşar. Kaynağını kontrol et!", "palace",
    [A("napolyon", 0.45, "bicorne", "point", "confident", scale=1.35)], [{"type": "sfx", "name": "rimshot", "f": 0.7}],
    text="Günün dersi: Bir yalanı yeterince tekrarlarsan, 200 yıl yaşar. Kaynağını kontrol et!"),
  outro()]})

# ---------------------------------------------------------------- 005 Truva Atı
EP.append({"id": "005", "file": "005_truva_ati", "title": "Truva Atı: Tarihin En Büyük Trollü", "year": "MÖ 1200",
 "caption": ("10 yıl savaştılar, kazanamadılar. Sonra biri dedi ki: \"Dev bir tahta at yapalım!\" 🐴😂\n\n"
  "Truva Savaşı'nın efsanesine göre Yunanlar, içi askerlerle dolu dev bir tahta atı hediye diye kapıya bıraktı. Truvalılar atı şehre soktu ve gece kapılar açıldı. "
  "Truva şehri gerçek, kalıntıları Çanakkale'de; ama atın hikâyesi bir efsane. Bugün bilgisayar virüslerine de bu yüzden 'Truva atı' deniyor!\n\n"
  "Sen bu atı şehre sokar mıydın? Yorumlara yaz 👇\nHer gün yeni bir tarih hikâyesi için takip et 📚\n\n"
  f"#tarih #truva #çanakkale #mitoloji {TAG}"),
 "scenes": [
  intro("Dur! Sana gelmiş geçmiş en büyük trolü anlatacağım. Hediyesi, dev bir tahta at!",
        "Dur! Sana gelmiş geçmiş en büyük trolü anlatacağım. Hediyesi... dev bir tahta at!", "DUR!", "TAHTA AT?!"),
  S("Efsaneye göre Yunanlar, Truva şehrini tam on yıl kuşatır. Ama o surlar bir türlü aşılmaz.", "plain",
    [A("yunan", 0.25, "greek", "push", "effort", scale=1.1)], [{"type": "wall", "x": 0.75, "w": 0.5, "h": 0.42}, pop("10 YIL!", 0.45, 0.25, 2.5, 120, -6)],
    text="Efsaneye göre Yunanlar, Truva şehrini tam 10 yıl kuşatır. Ama o surlar bir türlü aşılmaz."),
  S("Sonunda kurnaz Odisseus'un aklına bir fikir gelir.", "plain",
    [A("odisseus", 0.45, "greek", "think", "think", scale=1.35, pose2="point", face2="happy", switch=0.55)],
    [{"type": "bulb", "actor": "odisseus", "delay": 1.6}]),
  S("Dev bir tahta at yaparlar, içine askerleri saklarlar ve kapının önüne bırakıp gemilerle uzaklaşırlar. Sanki pes etmişler gibi!", "plain",
    [A("yunan", 0.12, "greek", "push", "effort", anim="walk", scale=0.9)],
    [{"type": "trojan", "x": 0.35, "y": 0.93, "scale": 0.9, "to_x": 0.55, "move_dur": 6}, pop("HEDİYE!", 0.6, 0.2, 4.5, 110, 6)]),
  S("Truvalılar sevinir: Kazandık! Bu güzel atı da şehre alalım!", "plain",
    [A("truvali1", 0.2, "helmet", "cheer", "happy", anim="bounce", scale=1.1), A("truvali2", 0.82, "crown", "cheer", "happy", anim="bounce", scale=1.1, flip=True)],
    [{"type": "trojan", "x": 0.5, "y": 0.93, "scale": 0.8}]),
  S("Gece olur. Herkes kutlamadan yorgun düşmüş uyurken, atın kapağı açılır.", "plain",
    [], [{"type": "trojan", "x": 0.5, "y": 0.93, "scale": 0.9, "open": True}, pop("GICIRT!", 0.6, 0.25, 2.5, 100, 8)], night=True),
  S("Askerler iner, kapıları açar, ve Truva düşer. On yıllık savaş, bir hediye paketiyle biter!", "plain",
    [A("yunan1", 0.25, "greek", "cheer", "happy", holds="torch", anim="bounce", scale=1.0),
     A("truvali", 0.75, "helmet", "shock", "shock", flip=True, anim="shake", scale=1.1)],
    [pop("SÜRPRİZ!", 0.5, 0.2, 2.0, 120, -6)], night=True,
    text="Askerler iner, kapıları açar, ve Truva düşer. 10 yıllık savaş, bir hediye paketiyle biter!"),
  S("Truva şehri gerçek, kalıntıları bugün Çanakkale'de. At ise büyük ihtimalle bir efsane. Ama adı yaşıyor: Bilgisayar virüslerine bu yüzden Truva atı deniyor. Günün dersi: Bedava hediyeye dikkat!", "plain",
    [A("hoca_ogrenci", 0.3, None, "point", "smug", scale=1.25)], [{"type": "trojan", "x": 0.72, "y": 0.93, "scale": 0.6}, {"type": "sfx", "name": "rimshot", "f": 0.85}]),
  outro()]})

# ---------------------------------------------------------------- 006 Hezarfen
EP.append({"id": "006", "file": "006_hezarfen", "title": "Galata'dan Üsküdar'a Uçan Adam", "year": "1630'LAR",
 "caption": ("Uçaktan yaklaşık 270 yıl önce, İstanbul'da bir adam kanat takıp Galata Kulesi'nden atladı 🪽\n\n"
  "Evliya Çelebi'nin anlattığına göre Hezarfen Ahmed Çelebi, IV. Murad döneminde Galata Kulesi'nden süzülerek Üsküdar'a indi. "
  "Padişah onu bir kese altınla ödüllendirdi ama 'bu adam istediğini yapabilir' diyerek Cezayir'e sürdü. Hikâyenin tek kaynağı Evliya Çelebi'dir.\n\n"
  "Sen olsan atlar mıydın? Yorumlara yaz 👇\nHer gün yeni bir tarih hikâyesi için takip et 📚\n\n"
  f"#tarih #hezarfenahmedçelebi #galatakulesi #evliyaçelebi {TAG}"),
 "scenes": [
  intro("Dur! Uçak icat edilmeden yüzyıllar önce, İstanbul'da biri gökyüzünde süzüldü!",
        "Dur! Uçak icat edilmeden yüzyıllar önce, İstanbul'da biri gökyüzünde süzüldü!", "DUR!", "UÇAN ADAM?!"),
  S("Yıl 1630'lar. İstanbul'da Hezarfen Ahmed Çelebi adında meraklı bir bilgin yaşıyor. Hezarfen, bin bilim bilen demek.", "city",
    [A("hezarfen", 0.4, "sarik", "think", "think", scale=1.35, holds="scroll")], [pop("BİN BİLİM!", 0.72, 0.25, 4.5, 96, 6)]),
  S("Kuşları saatlerce izler. Kafasında tek soru: İnsan da uçabilir mi?", "city",
    [A("hezarfen", 0.35, "sarik", "think", "think", scale=1.35)], [{"type": "bulb", "actor": "hezarfen", "delay": 2.0}]),
  S("Kendine kanatlar yapar ve rüzgârlı bir günde Galata Kulesi'nin tepesine çıkar.", "city",
    [A("hezarfen", 0.3, "sarik", "shrug", "effort", scale=0.75, wings=True, y=0.39)],
    [{"type": "tower", "x": 0.3, "y": 0.93, "scale": 1.0}, pop("GALATA!", 0.72, 0.3, 2.8, 100, -5)]),
  S("Ve atlar! Evliya Çelebi'ye göre Boğaz'ın üstünden süzülüp tam karşıya, Üsküdar'a iner.", "sea",
    [A("hezarfen", 0.1, "sarik", "open_arms", "happy", scale=0.8, wings=True, y=0.35, to_x=0.9, to_y=0.72, arc=0.15)],
    [pop("UÇUYOR!", 0.5, 0.12, 2.0, 110, -6)]),
  S("Halk şaşkın! Padişah IV. Murad da çok etkilenir ve Hezarfen'e bir kese altın verir.", "palace",
    [A("murad", 0.3, "kavuk", "point", "happy", scale=1.25), A("hezarfen", 0.72, "sarik", "cheer", "happy", flip=True, scale=1.15, anim="bounce")],
    [{"type": "coins", "x": 0.52, "y": 0.93, "delay": 3.5}, pop("ALTIN!", 0.55, 0.25, 3.6, 110, 6)]),
  S("Ama sonra der ki: Bu adam korkutucu, istediği her şeyi yapabilir! Ve Hezarfen'i Cezayir'e sürgüne gönderir.", "palace",
    [A("murad", 0.3, "kavuk", "hips", "smug", scale=1.25, talk=True), A("hezarfen", 0.72, "sarik", "sad", "sad", flip=True, scale=1.15)],
    [pop("SÜRGÜN!", 0.55, 0.22, 4.5, 110, -6)]),
  S("Bu hikâyenin tek kaynağı Evliya Çelebi. Yani doğru mu, abartı mı, hâlâ tartışılıyor. Günün dersi: Fazla parlak fikirler bazen başını derde sokar!", "city",
    [A("hezarfen", 0.45, "sarik", "shrug", "happy", scale=1.3, wings=True)], [{"type": "sfx", "name": "rimshot", "f": 0.8}]),
  outro()]})

# ---------------------------------------------------------------- 007 Emu Savaşı
EP.append({"id": "007", "file": "007_emu_savasi", "title": "Ordu Emulara Yenildi!", "year": "1932",
 "caption": ("Bir ülke kuşlara savaş açtı... ve kaybetti 🦤😂\n\n"
  "1932'de Batı Avustralya'da yaklaşık 20 bin emu buğday tarlalarını talan edince hükümet orduyu gönderdi. "
  "Binlerce mermi harcandı ama hızlı ve kalabalık emular dağılıp kaçtı. Askerler kısa süre sonra geri çekildi. Tarihe 'Büyük Emu Savaşı' olarak geçti!\n\n"
  "Sence kim kazandı? Yorumlara yaz 👇\nHer gün yeni bir tarih hikâyesi için takip et 📚\n\n"
  f"#tarih #avustralya #emusavaşı #ilginçbilgiler {TAG}"),
 "scenes": [
  intro("Dur! Bir ülke kuşlara savaş açtı. Ve tahmin et kim kazandı? Kuşlar!",
        "Dur! Bir ülke kuşlara savaş açtı. Ve tahmin et kim kazandı? Kuşlar!", "DUR!", "KUŞLAR MI?!"),
  S("Yıl 1932, Avustralya. Çiftçiler buğday ekmiş, hasat bekliyor.", "farm",
    [A("ciftci", 0.35, "slouch", "hips", "happy", scale=1.3, y=0.9)], [{"type": "fence", "x1": 0.6, "x2": 1.0, "y": 0.9}]),
  S("Derken ufukta yaklaşık yirmi bin emu belirir. Kocaman, hızlı ve çok aç!", "farm",
    [A("ciftci", 0.2, "slouch", "shock", "shock", scale=1.15, y=0.9, anim="shake")],
    [{"type": "emu", "x": 1.1, "y": 0.92, "flip": True, "anim": "run", "to_x": 0.55, "move_dur": 4},
     {"type": "emu", "x": 1.3, "y": 0.94, "scale": 0.8, "flip": True, "anim": "run", "to_x": 0.8, "move_dur": 4},
     pop("20 BİN EMU!", 0.55, 0.22, 3.0, 100, -6)],
    text="Derken ufukta yaklaşık 20 bin emu belirir. Kocaman, hızlı ve çok aç!"),
  S("Tarlalar talan edilir. Çiftçiler hükümete yalvarır: Bizi kurtarın!", "farm",
    [A("ciftci", 0.25, "slouch", "shrug", "sad", scale=1.15, y=0.9, talk=True)],
    [{"type": "emu", "x": 0.62, "y": 0.92, "flip": True}, {"type": "emu", "x": 0.85, "y": 0.93, "scale": 0.85, "flip": True},
     {"type": "bubble", "text": "Kurtarın bizi!", "x": 0.3, "y": 0.13, "tx": 0.27, "ty": 0.3, "delay": 1.5}]),
  S("Hükümet orduyu gönderir. Askerler kendinden emin: Birkaç günde işi bitiririz!", "farm",
    [A("asker1", 0.25, "slouch", "hips", "confident", scale=1.2, y=0.9), A("asker2", 0.45, "slouch", "point", "confident", scale=1.1, y=0.9)],
    [pop("ORDU GELDİ!", 0.7, 0.25, 1.0, 100, 6)]),
  S("Ama emular çok hızlı ve çok kurnaz. Askerler yaklaşınca küçük gruplara ayrılıp her yöne kaçıyorlar.", "farm",
    [A("asker1", 0.2, "slouch", "push", "effort", scale=1.05, y=0.9, anim="walk")],
    [{"type": "emu", "x": 0.5, "y": 0.92, "anim": "run", "to_x": 1.2, "move_dur": 3},
     {"type": "emu", "x": 0.6, "y": 0.94, "scale": 0.8, "anim": "run", "to_x": 1.3, "move_dur": 2.5},
     pop("FIRT!", 0.6, 0.25, 1.5, 110, 8)]),
  S("Binlerce mermi harcanır ama emular hâlâ ortalıkta! Komutan, bu kuşlar tank gibi dayanıklı, der.", "farm",
    [A("asker1", 0.25, "slouch", "shrug", "sad", scale=1.15, y=0.9), A("komutan", 0.55, "slouch", "think", "think", scale=1.2, y=0.9)],
    [{"type": "emu", "x": 0.85, "y": 0.92, "flip": True}, pop("TANK GİBİ!", 0.6, 0.22, 3.5, 100, -6)]),
  S("Sonunda ordu geri çekilir. Tarihe Büyük Emu Savaşı olarak geçer. Günün dersi: Rakibini asla küçümseme!", "farm",
    [A("asker1", 0.2, "slouch", "sad", "sad", scale=1.1, y=0.9)],
    [{"type": "emu", "x": 0.6, "y": 0.92, "flip": True}, {"type": "emu", "x": 0.82, "y": 0.93, "scale": 0.9, "flip": True},
     pop("EMULAR KAZANDI!", 0.6, 0.2, 2.5, 96, 5), {"type": "sfx", "name": "rimshot", "f": 0.75}]),
  outro()]})

# ---------------------------------------------------------------- 008 Kahve yasağı
EP.append({"id": "008", "file": "008_kahve_yasagi", "title": "Kahve İçmek Yasak! IV. Murad'ın Yasağı", "year": "1633",
 "caption": ("Türk kahvesi içmek bir zamanlar yasaktı ☕🚫 Hem de çok ağır cezası vardı!\n\n"
  "IV. Murad 1633 civarında kahvehaneleri kapattırdı, kahve ve tütünü yasakladı. Gerekçe: Kahvehaneler dedikodu ve isyan sohbetlerinin merkeziydi. "
  "Rivayete göre padişah geceleri kılık değiştirip yasağa uyulup uyulmadığını kendisi kontrol ederdi. Ama kahve sevgisi yasağı yendi!\n\n"
  "Sen kahvesiz kaç gün dayanırsın? Yorumlara yaz 👇\nHer gün yeni bir tarih hikâyesi için takip et 📚\n\n"
  f"#tarih #türkkahvesi #4murad #osmanlıtarihi {TAG}"),
 "scenes": [
  intro("Dur! Bir zamanlar İstanbul'da kahve içmek yasaktı. Hem de yakalanmak çok pahalıya patlıyordu!",
        "Dur! Bir zamanlar İstanbul'da kahve içmek yasaktı. Hem de yakalanmak çok pahalıya patlıyordu!", "DUR!", "KAHVE YASAK?!"),
  S("Yıl 1633. İstanbul kahvehaneleri tıklım tıklım. Herkes kahvesini yudumluyor, sohbet koyu.", "city",
    [A("adam1", 0.25, "sarik", "hips", "happy", holds="cup", scale=1.15), A("adam2", 0.7, "sarik", "point", "happy", holds="cup", scale=1.15, flip=True, talk=True)],
    [pop("KEYİF!", 0.5, 0.25, 3.5, 110, -6)]),
  S("Ama padişah IV. Murad bu durumdan hiç hoşnut değil. Ona göre kahvehaneler dedikodu ve isyan yuvası!", "palace",
    [A("murad", 0.4, "kavuk", "hips", "confident", scale=1.4)], [pop("İSYAN YUVASI!", 0.72, 0.25, 3.5, 90, 6)]),
  S("Ve emir çıkar: Kahvehaneler kapatılsın! Kahve de tütün de yasak!", "palace",
    [A("murad", 0.3, "kavuk", "point", "confident", scale=1.3, talk=True)],
    [{"type": "cezve", "x": 0.7, "y": 0.9, "scale": 0.9}, {"type": "ban", "x": 0.7, "y": 0.62, "scale": 0.9, "delay": 1.5}, pop("YASAK!", 0.7, 0.22, 1.6, 120, -6)]),
  S("Rivayete göre padişah geceleri kılık değiştirip sokaklarda dolaşır, yasağa uyan var mı diye kendisi kontrol eder.", "city",
    [A("murad", 0.15, "sarik", "stand", "smug", scale=1.1, anim="walk", to_x=0.55, move_dur=5)],
    [pop("GİZLİ DEVRİYE!", 0.6, 0.2, 3.0, 96, 6)], night=True),
  S("Yakalananlara çok ağır cezalar verilir. Kahvesever İstanbul'da büyük bir sessizlik!", "city",
    [A("adam1", 0.4, "sarik", "sad", "sad", scale=1.3)], [{"type": "ban", "x": 0.75, "y": 0.4, "scale": 0.6}]),
  S("Ama Türk insanının kahve sevgisi padişahtan da güçlü çıkar. Yasaklar zamanla gevşer, kahvehaneler yeniden açılır.", "city",
    [A("adam1", 0.25, "sarik", "cheer", "happy", holds="cup", scale=1.15, anim="bounce"), A("adam2", 0.7, "sarik", "cheer", "happy", holds="cup", scale=1.15, flip=True, anim="bounce")],
    [pop("KAHVE GERİ DÖNDÜ!", 0.5, 0.22, 3.5, 92, -5)]),
  S("Bugün Türk kahvesi UNESCO listesinde. Günün dersi: Bir Türk'ün kahvesine sakın karışma!", "plain",
    [A("adam1", 0.35, "sarik", "hips", "smug", holds="cup", scale=1.35)], [{"type": "cezve", "x": 0.75, "y": 0.93, "scale": 0.8}, {"type": "sfx", "name": "rimshot", "f": 0.75}]),
  outro()]})

for ep in EP:
    out = {"id": ep["id"], "series": "ÇÖP ADAMLA TARİH", "title": ep["title"], "year": ep["year"],
           "voice_fx": {"pitch": 1.15, "noise": 0.2, "noise_w": 0.3},
           "instagram_caption": ep["caption"], "scenes": ep["scenes"]}
    json.dump(out, open(os.path.join(ROOT, "episodes", ep["file"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("yazıldı:", ep["file"], len(ep["scenes"]), "sahne")
