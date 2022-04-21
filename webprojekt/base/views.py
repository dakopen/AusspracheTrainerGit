from sqlite3 import Timestamp
import sys
import secrets
import random
import concurrent.futures
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from utils.textCheck import check_text, sonderzeichen_entfernen, save_raw_targetsatz, clean_targetsatz
from utils.audio import generate_time_stamp, Audioverarbeitung
from time import sleep
from utils.Auswertung import auswertung, sprachfehler_from_scores, adjektiv_fuer_score, calculate_colour
import re
import logging

logging.basicConfig(filename='test.log', encoding='utf-8-sig', level=logging.DEBUG)

def home(request):
    request.session["id"] = secrets.token_urlsafe(6)
    context = {
        "textgenerator": [
            "Zufälligen Satz",
            "Sch-Satz",
            "S-Satz",
            "Ch-Satz",
            # Satz des Tages
        ],
        "session_id": request.session["id"]
    }
    return render(request, '../templates/index.html', context=context)



def get_session_id(request):
    session_id = request.GET.get("session", None)
    try:
        if session_id != request.session["id"]:
            del request.session["id"]
            return None
        return session_id 
    except KeyError:
        return None
    


@csrf_exempt
def textinput_check(request):
    session_id = get_session_id(request)
    if not session_id:
        return redirect("/")

    text = (request.body).decode("utf-8-sig")
    fehler_liste, bin_icon_bool = check_text(text)
    return JsonResponse([fehler_liste, bin_icon_bool], safe=False)

@csrf_exempt
def satzgenerator(request):
    session_id = get_session_id(request)

    satzart = (request.body).decode("utf-8-sig")  # [Zufälligen Satz / Sch-Satz / ...]
    jetziger_satz = str(request.headers["currenttextarea"])  # *, jeder vom Benutzer eingegebene Satz
    if satzart == "Zufälligen Satz":
        with open("static/assets/other/random_sentences_de.txt", "r",
                  encoding="utf-8-sig") as random_saetze:
            lines = random_saetze.readlines()
    elif satzart == "Sch-Satz":
        lines = ["Am Strand bauen die Kinder mit dem Spielzeug und der Schaufel eine Sandburg.", "Die Schnecken hinterlassen eine Schleimspur auf der Straße.", "Auf der Schnellstraße herrscht schneller Straßenverkehr.", "Spreewaldgurken schmecken gut, sind aber im Spreewald am schmackhaftesten.", "Die Schlange erschreckt die Spinne im Spind.", "Das Schulkind versteckt sich im Schrank.", "Seine Schüssel sprang in zwei.", "Hirsche haben ein prächtiges Geweih.", "Die schmützige Wärsche gehört in den schwarzen Korb.", "Stefan erscheint als letzter auf dem Schiff.", "Im Schwarzwald gibt es Schmetterlinge zu beobachten.", "Im Schein der Sonne schmilzt der Schneeman dahin.", "Dem Schwein schmeckt die geschälte Kartoffel.", "Hast du im Sportunterricht an Schnelligkeit gewonnen?", "Sterne kann man am Strand bewundern.", "Schneide die Banane in Stücke!"]
    elif satzart == "Ch-Satz":
        lines = ["Die Eichhörnchen sammeln Eicheln für ihren Wintervorrat.", "Ich möchte noch in die Kirche gehen.", "Ich weiß nicht, ob Sie Griechisch sprechen und mein Griechisch verstehen.", "Der jämmerliche König hinterlässt eine Nachricht.", "Das Schweinchen quiekte fröhlich.", "Wie bleich das Pärchen wurde.", "Es ist mir peinlich, die Zeichnung vorzustellen.", "Die Berichterstattung sah fürchterlich aus.", "Ungerechtigkeit gehört sicherlich zum Leben dazu.", "Das tüchtige Mädchen handelt richtig.", "Ein reicher Scheich kaufte die gesamte Einrichtung.", "Laut meiner Recherche gehört sein Vermächtnis der Tochter.", "Tomaten haben beachtlich viele Vitamine und sind sehr reichhaltig an wichtigen Mineralien.",
         "Es ist echt gefährlich sich im Auto nicht anzuschnallen.", "Ein Eichhörnchen ist leichter als ein Elch."]
    elif satzart == "S-Satz":  # else
        lines = ["Ein Seehund sonnt sich in der Mittagssonne.", "In der Sage wird von Sandstein berichtet.", "Unser Silberbesteck hat etwas ansich.", "Die Szene wird von Susanne vorgelesen.", "In der Suppe fehlt Salz.", "Im Saal sitzt manch seltsamer Mann.", "Sonntags singen sieben Zwerge am See lustige Lieder.", "Sie segelt schon siebzig Jahre.", "Sechs Ameisen suchen schutz unterm Baum.", "Der Zug fährt vom Zirkus ins Saarland.", "Sauerstoff ist überlebenswichtig für Säugetiere.", "Hase und Gans grasen zusammen auf der Wiese.", "Zwei Sachen noch, dann ist sie fertig.", "Im September gibt es Sauerbraten zu essen.", "Salat und Sellerie sind gesunde Lebensmittel.", "Susi sagte, dass sie gerne Salat mit Mais isst.", "Morgens isst Susanne gerne Müsli mit Nüssen.", "Auf der Insel scheint die Sonne übermäßig viel.", "Hans isst gerne Bratwurst mit Senf."]
    lines = [i.strip() for i in lines]
    
    for line in lines:
        if sonderzeichen_entfernen(line) == jetziger_satz:
            lines.remove(line)
            break

    return HttpResponse(random.choice(lines).strip())


def audio(request):
    session_id = get_session_id(request)
    if sys.getsizeof(request.body) < 1000:
        logging.debug(f"Aufnahme ist zu kurz: request.body: {sys.getsizeof(request.body)} | {session_id}")
        return HttpResponse("Die Audioaufnahme ist zu kurz. Bitte erneut aufnehmen.")
    elif sys.getsizeof(request.body) > 2300000:  # 2203725 maximale Größe auf Windows 11 Firefox TODO: Checken, ob es eine allgemeine Größe ist
        return HttpResponse("Die Audioaufnahme ist zu lang. Bitte erneut aufnehmen.")

    timestamp = generate_time_stamp()
    request.session["rawtargetsatz_%s" % session_id] = save_raw_targetsatz(request.META["HTTP_TARGETSATZ"])
    if not request.session["rawtargetsatz_%s" % session_id]:
        logging.debug(f"Not request.session[rawtargetsatz]: {request.session['rawtargetsatz_%s' % session_id]}  | {session_id}")
        return HttpResponse("Bitte gib einen Übungssatz ein.")

    elif check_text(request.session["rawtargetsatz_%s" % session_id])[0]:
        logging.debug(f"Check_Text Fehler in request.session[rawtargetsatz]: {request.session['rawtargetsatz_%s' % session_id]}  | {session_id}")
        return HttpResponse("Bitte überprüfe den Übungssatz.")

    request.session["cleantargetsatz_%s" % session_id] = clean_targetsatz(request.META["HTTP_TARGETSATZ"])
    request.session["audiopath_%s" % session_id] = f'./media/{timestamp}_{session_id}.wav'

    with open(request.session["audiopath_%s" % session_id], "wb") as audiofile:
        audiofile.write(request.body)

    return HttpResponse("Audio empfangen")

def result(request):
    session_id = get_session_id(request)

    with concurrent.futures.ThreadPoolExecutor() as executor:

        audioverarbeiter = Audioverarbeitung(str(request.session["audiopath_%s" % session_id]), str(request.session["cleantargetsatz_%s" % session_id]), str(request.session["audiopath_%s" % session_id]))

        future_google = executor.submit(audioverarbeiter.google)
        future_ibm = executor.submit(audioverarbeiter.IBM)
        future_at = executor.submit(audioverarbeiter.AT)

        future_target_ipa = executor.submit(audioverarbeiter.ipa.text_zu_IPA, audioverarbeiter.ipa.text_preparation(str(request.session["cleantargetsatz_%s" % session_id])))
        executor.shutdown()
        audioverarbeiter.delete_audio()

    print(future_target_ipa.result())
    print(future_google.result())
    print(future_ibm.result())
    print(future_at.result())

    request.session["target_ipa_%s" % session_id] = future_target_ipa.result()[0]
    request.session["target_ipa_zuordnungen_%s" % session_id] = future_target_ipa.result()[1]
    request.session["google_ki_ipa_%s" % session_id] = future_google.result()[0]
    request.session["at_ki_%s" % session_id] = future_at.result()
    request.session["ibm_ki_ipa_%s" % session_id] = future_ibm.result()[0]
    
    

    if any(future for future in [future_google.result()[0], future_ibm.result()[0], future_at.result()] if future.startswith("#*# ERROR RECEIVED")):
        return HttpResponse("<span class='red' style='font-size:1em;'>Error erhalten: Der aufgenommene Satz konnte nicht analysiert werden. Bitte erneut aufnehmen oder einen anderen Satz versuchen.</span>")
    
    
    

    auswertungsergebnis, scores, sprachfehler_scores = auswertung(request.session["target_ipa_%s" % session_id], request.session["target_ipa_zuordnungen_%s" % session_id], 
                                                                [request.session["at_ki_%s" % session_id],
                                                                request.session["google_ki_ipa_%s" % session_id],
                                                                request.session["ibm_ki_ipa_%s" % session_id]])
    buchstabenscores = {}
    buchstabenindex = 0

    reg = re.compile('^[a-zA-ZäöüÄÖÜß\s]')
    
    print(auswertungsergebnis, "AUSWERTUNGSERGEBNIS")
    print(scores, "SCORES")

    print(str(request.session["rawtargetsatz_%s" % session_id]), "RAWTARGETSATZ")

    for index, buchstabe in enumerate(str(request.session["rawtargetsatz_%s" % session_id])):
        try:
            if buchstabe.isalnum() and reg.match(buchstabe):
                colour = calculate_colour(auswertungsergebnis[buchstabenindex])
                buchstabenindex += 1
            elif buchstabe == " " and str(request.session["cleantargetsatz_%s" % session_id])[buchstabenindex] == " ":
                colour = calculate_colour(auswertungsergebnis[buchstabenindex])
                buchstabenindex += 1
            else:
                colour = "green"
        except IndexError:
            print("Indexerror, aber nicht schlimm")
        buchstabenscores[index] = (colour, buchstabe)
    request.session["buchstabenscores_%s" % session_id] = buchstabenscores
    farbigeAntwort = buchstaben_scores_interally(request)
    if scores[0] < 0:
        scores = (0, scores[1], scores[2])

    context = {
        "farbigeAntwort": farbigeAntwort,
        "finalscore": ("%.2f" % float(scores[0] * 100)).replace(".", ","),
        "scoreadjektiv": adjektiv_fuer_score(scores[0]),
        "sprachfehler": sprachfehler_from_scores(sprachfehler_scores, scores[1]),
    }

    # TODO: In eine Datenbank schreiben

    return render(request, '../templates/ergebnis.html', context=context)



def buchstaben_scores_interally(request):
    session_id = str(request.GET.get('session'))
    context = {"buchstabenscores": request.session["buchstabenscores_%s" % session_id]}
    return render_to_string('../templates/farbigeAntwort.html', context=context)


def handler404(request, exception):
    return render(request, "../templates/404.html", status=404, )


def privacypolicy(request):
    return render(request, "../templates/privacy-policy.html")


def sources(request):
    return render(request, "../templates/sources.html")


def about(request):
    return render(request, "../templates/about.html")


def faq(request):
    return render(request, "../templates/faq.html")


def kontakt(request):
    return render(request, "../templates/kontakt.html")


def training(request):
    return render(request, "../templates/training.html")


def terms(request):
    return render(request, "../templates/terms.html")


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /"
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
