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