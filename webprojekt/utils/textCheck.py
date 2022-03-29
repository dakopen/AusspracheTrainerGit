from os import remove
import re   

def sonderzeichen_entfernen(text):
    return re.sub("[^a-zöäüß ]+", "", text.lower())

def check_text(text):
    fehler_liste = []
    if len(text) > 120:
        raise Exception("Text ist zu lange")

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
    
    return fehler_liste


