import re, unicodedata

def slugify(text, maxlen=40):
    text = unicodedata.normalize("NFKD", text).encode("ascii","ignore").decode()
    text = re.sub(r"[^\w]+", "-", text).strip("-").lower()
    return text[:maxlen]
