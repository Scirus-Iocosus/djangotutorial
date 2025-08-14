from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from .models import PunteggiRossi, PunteggiVerdi, PunteggiGialli, PunteggiBlu, Iscritto, Presenza, file, cucina, sino, pagamenti, DownloadPerGenitori
from .forms import AnimatoForm, files
from django.contrib.auth.decorators import user_passes_test
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from collections import defaultdict
from django.template.loader import get_template
from datetime import date

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Scemo riprova")

    return render(request, "create_user.html")

def logout_view(request):
    logout(request)
    return redirect("index")

def get_punteggi(request):
    # Calcolare la somma per ogni classe
    punteggi = [
        {"classe": "ClasseA", "punteggio": PunteggiRossi.objects.aggregate(total=Sum('punteggio'))['total'] or 0},
        {"classe": "ClasseB", "punteggio": PunteggiVerdi.objects.aggregate(total=Sum('punteggio'))['total'] or 0},
        {"classe": "ClasseC", "punteggio": PunteggiGialli.objects.aggregate(total=Sum('punteggio'))['total'] or 0},
        {"classe": "ClasseD", "punteggio": PunteggiBlu.objects.aggregate(total=Sum('punteggio'))['total'] or 0},
    ]

    # Ordinare per punteggio crescente
    punteggi_ordinati = sorted(punteggi, key=lambda x: x["punteggio"])

    return JsonResponse({"punteggi": punteggi_ordinati})

def superuser_required(user):
    return user.is_superuser

@user_passes_test(superuser_required)
def admin(request):
    return redirect("admin/")

def index(response):
    return render(response, "base.html", {})

@login_required
def home(response):
    return render(response, 'home2.html', {})
def info(request):
    documenti = DownloadPerGenitori.objects.all()
    return render(request, 'info.html', {'documenti': documenti})
def info2(request):
    documenti = DownloadPerGenitori.objects.all()
    return render(request, 'info2.html', {'documenti': documenti })

def appello(response):
    return render(response, 'appello.html', {})
def squadra(response):
    return render(response, 'squadra.html', {})
def uscita(response):
    return render(response, 'uscita.html', {})
def classifica(response):
    return render(response, 'classifica.html', {})
@api_view(['GET'])
def get_punteggio_rosso(request):
    punteggi = PunteggiRossi.objects.all()
    somma_punteggi = sum([p.punteggio for p in punteggi])  # Somma tutti i punteggi
    return Response({"somma_punteggi": somma_punteggi})
@api_view(['GET'])
def get_punteggio_verde(request):
    punteggi = PunteggiVerdi.objects.all()
    somma_punteggi = sum([p.punteggio for p in punteggi])  # Somma tutti i punteggi
    return Response({"somma_punteggi": somma_punteggi})
@api_view(['GET'])
def get_punteggio_giallo(request):
    punteggi = PunteggiGialli.objects.all()
    somma_punteggi = sum([p.punteggio for p in punteggi])  # Somma tutti i punteggi
    return Response({"somma_punteggi": somma_punteggi})
@api_view(['GET'])
def get_punteggio_blu(request):
    punteggi = PunteggiBlu.objects.all()
    somma_punteggi = sum([p.punteggio for p in punteggi])  # Somma tutti i punteggi
    return Response({"somma_punteggi": somma_punteggi})

def elenco_animati(request):
    animati = Iscritto.objects.all()
    oggi = timezone.now().date()

    return render(request, 'squadra.html', {
        'animati': animati,
        'oggi': oggi,
    })

def entrata(request):
    animati = Iscritto.objects.all()
    oggi = timezone.now().date()
    presenze = Presenza.objects.filter(data=oggi)
    presenze_dict = {p.animato_id: p for p in presenze}

    for animato in animati:
        animato.presenza = presenze_dict.get(animato.id)

    return render(request, 'entrata.html', {
        'animati': animati,
        'today': oggi
    })

@csrf_exempt
@require_POST
def salva_presenze(request):
    oggi = timezone.now().date()
    for key in request.POST:
        if key.startswith('entrata_'):
            animato_id = key.replace('entrata_', '')
            valore = request.POST[key]
            presenza, _ = Presenza.objects.get_or_create(animato_id=animato_id, data=oggi)
            presenza.entrata = valore == 'true'
            presenza.save()

        elif key.startswith('uscita_'):
            animato_id = key.replace('uscita_', '')
            valore = request.POST[key]
            presenza, _ = Presenza.objects.get_or_create(animato_id=animato_id, data=oggi)
            presenza.uscita = valore == 'true'
            presenza.save()

    return JsonResponse({'status': 'ok'})

@csrf_exempt
@require_POST
def cancella_presenze(request):
    oggi = timezone.now().date()
    Presenza.objects.filter(data=oggi).delete()
    return JsonResponse({'status': 'ok'})

def presenze_print(request):
    animati = Iscritto.objects.all()
    oggi = timezone.now().date()
    presenze = Presenza.objects.filter(data=oggi)
    presenze_dict = {p.animato_id: p for p in presenze}

    for animato in animati:
        animato.presenza = presenze_dict.get(animato.id)

    return render(request, 'presenze_print.html', {
        'animati': animati,
        'oggi': oggi,
    })

def blu(request):
    iscritti = Iscritto.objects.filter(squadra="Blu")
    oggi = timezone.now().date()
    return render(request, 'blu.html', {
        'iscritti': iscritti,
        'oggi': oggi,
    })

def gialli(request):
    iscritti = Iscritto.objects.filter(squadra="Gialli")
    oggi = timezone.now().date()
    return render(request, 'gialli.html', {
        'iscritti': iscritti,
        'oggi': oggi,
    })

def rossi(request):
    iscritti = Iscritto.objects.filter(squadra="Rossi")
    oggi = timezone.now().date()
    return render(request, 'rossi.html', {
        'iscritti': iscritti,
        'oggi': oggi,
    })

def verdi(request):
    iscritti = Iscritto.objects.filter(squadra="Verdi")
    oggi = timezone.now().date()
    return render(request, 'verdi.html', {
        'iscritti': iscritti,
        'oggi': oggi,
    })

def iscrizioni(request):
    mansioni = cucina.objects.all()
    siono = sino.objects.all()
    x = pagamenti.objects.all()

    if request.method == 'POST':
        form = AnimatoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'iscrizioni3.html', {})
        else:
            print(form.errors)  # ✅ ora è sicuro
    else:
        form = AnimatoForm()

    return render(request, 'iscrizioni.html', {
        'pagamenti': x,
        'form': form,
        'mansioni': mansioni,
        'siono': siono,
    })


def iscrizioni2(request):
    iscritti = Iscritto.objects.all()
    oggi = date.today

    return render(request, 'iscritti.html', {
        'iscritti': iscritti,
    })

def documenti(request):
    documenti = file.objects.all()
    if request.method == 'POST':
        form = files(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'file.html', {})
    else:
        form = files()
    return render(request, "file.html", {
        'documenti': documenti,
        'form': form,
    })