import re   
from urllib.parse import unquote

def sonderzeichen_entfernen(text):
    return re.sub("[^a-zöäüß ]+", "", text.lower())


def check_text(text):
    fehler_liste = []
    if len(text) > 120:
        raise Exception("Text ist zu lange")
    raw_text = text
    text = re.sub("[`~!@^*()_|+\-=?;:,.\\\}\[\{\]<>]", " ", text)  # Sonderzeichen entfernen
    text = ' '.join(text.split())

    if bool(re.search("[^a-zA-ZäöüÄÖÜß0-9 \s\x21-\x2F\x3A-\x40\x5B-\x60\x7B-\x7E]", text)):
        fehler_liste.append("Bitte nur deutsches Alphabet verwenden.")

    if bool(re.search(r'\d', text)):
        fehler_liste.append("Bitte Zahlen ausschreiben.")

    if bool(re.search("[#%&$€\x23-\x26]", text)):
        fehler_liste.append("Bitte Sonderzeichen ausschreiben.")
    
    if any(wort for wort in text.split() if len(wort) > 25):
        fehler_liste.append("Kein Wort darf länger als 25 Buchstaben lang sein.")
    
    if 119 > len(raw_text) > 100:
        fehler_liste.append(f"Noch {120-len(raw_text)} Buchstaben verbleiben...")
    elif len(raw_text) == 119:
        fehler_liste.append("Noch 1 Buchstabe verbleibend.")
    elif len(raw_text) == 120:
        fehler_liste.append("Maximale Buchstaben erreicht.")
    
    bin_icon_bool = show_bin_icon(len(raw_text))

    return fehler_liste, bin_icon_bool


def show_bin_icon(text_length):
    if text_length > 5:
        return True
    return False


def save_raw_targetsatz(HTTP_TARGETSATZ):
    return re.sub("\s\s+", " ", str(unquote(str(HTTP_TARGETSATZ)))).strip()


def clean_targetsatz(HTTP_TARGETSATZ):
    raw_targetsatz =  re.sub("\s\s+", " ", str(unquote(str(HTTP_TARGETSATZ)))).strip().lower()
    return re.sub('[^a-zäüöß ]+', '', raw_targetsatz)
