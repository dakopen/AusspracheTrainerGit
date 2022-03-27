import random
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

def home(request):
    context = {
        "textgenerator": [
            "Zufälligen Satz",
            "Sch-Satz",
            "S-Satz",
            "Ch-Satz",
            # Satz des Tages
        ]
    }
    return render(request, '../templates/index.html', context=context)


def get_session_id(request):
    session_id = request.GET.get("session", None)
    if not session_id:
        raise Exception(f"Keine session_id (session_id={session_id})")
    return session_id 
    


def satzgenerator(request):
    session_id = get_session_id(request)

    satzart = (request.body).decode("utf-8-sig")  # [Zufälligen Satz / Sch-Satz / ...]
    jetziger_satz = str(request.headers["currenttextarea"])  # *, jeder vom Benutzer eingegebene Satz
    if satzart == "Zufälligen Satz":
        
        # HIER RICHTIGES FILE ANGEBEN
        # TODO: Mit lowercase (nur a-z) vergleichen.
        with open("webprojekt//static//assets//other//random_sentences_de.txt", "r",
                  encoding="utf-8-sig") as random_saetze:
            lines = random_saetze.readlines()
    elif satzart == "Sch-Satz":
        lines = ["Am Strand bauen die Kinder mit dem Spielzeug und der Schaufel eine Sandburg.", "Die Schnecken hinterlassen eine Schleimspur auf der Straße.", "Auf der Schnellstraße herrscht schneller Straßenverkehr.", "Spreewaldgurken schmecken gut, sind aber im Spreewald am schmackhaftesten.", "Die Schlange erschreckt die Spinne im Spind.", "Das Schulkind versteckt sich im Schrank.", "Seine Schüssel sprang in zwei.", "Hirsche haben ein prächtiges Geweih.", "Die schmützige Wärsche gehört in den schwarzen Korb.", "Stefan erscheint als letzter auf dem Schiff.", "Im Schwarzwald gibt es Schmetterlinge zu beobachten.", "Im Schein der Sonne schmilzt der Schneeman dahin.", "Dem Schwein schmeckt die geschälte Kartoffel.", "Hast du im Sportunterricht an Schnelligkeit gewonnen?", "Sterne kann man am Strand bewundern.", "Schneide die Banane in Stücke!"]
    elif satzart == "Ch-Satz":
        lines = ["Die Eichhörnchen sammeln Eicheln für ihren Wintervorrat.", "Ich möchte noch in die Kirche gehen.", "Ich weiß nicht, ob Sie Griechisch sprechen und mein Griechisch verstehen.", "Der jämmerliche König hinterlässt eine Nachricht.", "Das Schweinchen quiekt e fröhlich.", "Wie bleich das Pärchen wurde.", "Es ist mir peinlich, die Zeichnung vorzustellen.", "Die Berichterstattung sah fürchterlich aus.", "Ungerechtigkeit gehört sicherlich zum Leben dazu.", "Das tüchtige Mädchen handelt richtig.", "Ein reicher Scheich kaufte die gesamte Einrichtung.", "Laut meiner Recherche gehört sein Vermächtnis der Tochter.", "Tomaten haben beachtlich viele Vitamine und sind sehr reichhaltig an wichtigen Mineralien.",
         "Es ist echt gefährlich sich im Auto nicht anzuschnallen.", "Ein Eichhörnchen ist leichter als ein Elch."]
    elif satzart == "S-Satz":  # else
        lines = ["Ein Seehund sonnt sich in der Mittagssonne.", "In der Sage wird von Sandstein berichtet.", "Unser Silberbesteck hat etwas ansich.", "Die Szene wird von Susanne vorgelesen.", "In der Suppe fehlt Salz.", "Im Saal sitzt manch seltsamer Mann.", "Sonntags singen sieben Zwwerge am See lustige Lieder.", "Sie segelt schon siebzig Jahre.", "Sechs Ameisen suchen schutz unterm Baum.", "Der Zug fährt vom Zirkus ins Saarland.", "Sauerstoff ist überlebenswichtig für Säugetiere.", "Hase und Gans grasen zusammen auf der Wiese.", "Zwei Sachen noch, dann ist sie fertig.", "Im September gibt es Sauerbraten zu essen.", "Salat und Sellerie sind gesunde Lebensmittel." "Susi sagte, dass sie gerne Salat mit Mais isst.", "Morgens isst Susanne gerne Müsli mit Nüssen.", "Auf der Insel scheint die Sonne übermäßig viel.", "Hans isst gerne Bratwurst mit Senf."]
    lines = [i.strip() for i in lines]
    
    if jetziger_satz in lines:
        lines.remove(jetziger_satz)
    print(random.choice(lines).strip())
    return HttpResponse(random.choice(lines).strip())




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