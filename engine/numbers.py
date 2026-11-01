"""Türkçe sayı -> yazı (tarihler için)."""
import re

BIR = ["", "bir", "iki", "üç", "dört", "beş", "altı", "yedi", "sekiz", "dokuz"]
ON = ["", "on", "yirmi", "otuz", "kırk", "elli", "altmış", "yetmiş", "seksen", "doksan"]


def sayi_yaz(n):
    if n == 0:
        return "sıfır"
    parts = []
    if n >= 1000:
        k = n // 1000
        parts.append("bin" if k == 1 else sayi_yaz(k) + " bin")
        n %= 1000
    if n >= 100:
        h = n // 100
        parts.append("yüz" if h == 1 else BIR[h] + " yüz")
        n %= 100
    if n >= 10:
        parts.append(ON[n // 10])
        n %= 10
    if n:
        parts.append(BIR[n])
    return " ".join(parts)


NUM_RE = re.compile(r"(\d+)(?:['’]([a-zA-ZçğıöşüÇĞİÖŞÜ]+))?")


def _sayilari_yaz(text):
    def rep(m):
        w = sayi_yaz(int(m.group(1)))
        return w + (m.group(2) or "")
    return NUM_RE.sub(rep, text)


YEAR_RE = re.compile(r"((?:[^\s.!?,:;]+\s+){0,2})(\d{3,4})(?:['’]([a-zA-ZçğıöşüÇĞİÖŞÜ]+))?")


def segmentler(text):
    """Metni (parça, yavaş_mı) listesine böler.
    Yıllar (3-4 haneli) ve önündeki en fazla 2 kelime tane tane okunur;
    diğer sayılar yazıya çevrilip normal akışta kalır."""
    out, pos = [], 0
    for m in YEAR_RE.finditer(text):
        if m.start() > pos:
            out.append((_sayilari_yaz(text[pos:m.start()]), False))
        phrase = _sayilari_yaz(m.group(1)) + sayi_yaz(int(m.group(2))) + (m.group(3) or "")
        out.append((phrase, True))
        pos = m.end()
    if pos < len(text):
        out.append((_sayilari_yaz(text[pos:]), False))
    res = []
    for t, sl in out:
        lead = t.lstrip()[:1] in ".!?"
        t = t.strip().lstrip(".,:;!? ")
        if t:
            res.append((t, sl, lead))
    return res


if __name__ == "__main__":
    for t in ["Yıl 1453. 21 yaşındaki Fatih", "29 Mayıs 1453'te İstanbul", "70 kadar gemi", "1071'de Malazgirt"]:
        print(segmentler(t))
