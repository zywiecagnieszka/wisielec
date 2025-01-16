from django.shortcuts import render, redirect
from django.http import JsonResponse
import random
from django.contrib import messages
from djangoProject.models import Slowo, Przyslowie, Uzytkownik
from datetime import date
from django.utils.timezone import now

def aktualizuj_punkty(uzytkownik, punkty_do_dodania):
    dzisiaj = date.today()
    if uzytkownik.data == dzisiaj:
        uzytkownik.punkty += punkty_do_dodania
        uzytkownik.punkty_dzien += punkty_do_dodania
    else:
        uzytkownik.punkty_dzien = punkty_do_dodania
        uzytkownik.punkty += punkty_do_dodania
        uzytkownik.data = dzisiaj
    uzytkownik.save()

def rejestracja(request):
    if request.method == 'POST':
        login = request.POST['login']
        email = request.POST['email']
        haslo = request.POST['haslo']

        if Uzytkownik.objects.filter(email=email).exists():
            messages.error(request, "Podany email już istnieje!")
            return redirect('rejestracja')

        Uzytkownik.objects.create(login=login, email=email, haslo=haslo)

        messages.success(request, "Rejestracja zakończona sukcesem! Możesz się teraz zalogować.")
        return redirect('logowanie')
    return render(request, 'rejestracja.html')

def logowanie(request):
    if request.method == 'POST':
        login = request.POST['login']
        haslo = request.POST['haslo']
        try:
            uzytkownik = Uzytkownik.objects.get(login=login, haslo=haslo)
            request.session['user_id'] = uzytkownik.id
            request.session['user_login'] = uzytkownik.login
            messages.success(request, f"Witaj, {uzytkownik.login}!")
            return redirect('wybor_trybu')
        except Uzytkownik.DoesNotExist:
            messages.error(request, "Nieprawidłowy email lub hasło!")
    return render(request, 'logowanie.html')

def wylogowanie(request):
    request.session.flush()
    messages.success(request, "Zostałeś wylogowany.")
    return redirect('logowanie')

def losuj_slowo():
    try:
        slowa = Slowo.objects.all()
        if not slowa.exists():
            return "przyklad"
        slowo = random.choice(slowa)
        return slowo.tekst
    except Exception as e:
        return str(e)

def main_page(request):
    return render(request, 'strona_glowna.html')

def zasady(request):
    return render(request, 'zasady.html')


def gra_wisielec(request):
    alfabet = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"  # Polski alfabet

    slowo = request.session.get('slowo')
    if not slowo:
        slowo = losuj_slowo()
        request.session['slowo'] = slowo

    pozostale_proby = request.session.get('pozostale_proby', 6)
    odgadniete_litery = request.session.get('odgadniete_litery', '')

    if request.method == "POST":
        litera = request.POST.get('litera', '').lower()
        if litera and litera not in odgadniete_litery:
            odgadniete_litery += litera
            if litera not in slowo.lower():
                pozostale_proby -= 1

    wyswietl_slowo = ''.join(
        [litera if litera.lower() in odgadniete_litery else '_' for litera in slowo]
    )
    wygrana = '_' not in wyswietl_slowo
    przegrana = pozostale_proby <= 0

    litery_status = {lit: "zielony" if lit in odgadniete_litery and lit in slowo.lower()
                     else "czerwony" if lit in odgadniete_litery else "szary"
                     for lit in alfabet}
    numer_img = 6 - pozostale_proby

    if wygrana:
        uzytkownik = Uzytkownik.objects.get(id=request.session['user_id'])
        aktualizuj_punkty(uzytkownik, 3)

    if wygrana or przegrana:
        request.session['pozostale_proby'] = 6
        request.session['odgadniete_litery'] = ''
        request.session['slowo'] = losuj_slowo()
        request.session['numer_img'] = numer_img
    else:
        request.session['pozostale_proby'] = pozostale_proby
        request.session['odgadniete_litery'] = odgadniete_litery
        request.session['numer_img'] = numer_img

    top_punkty = Uzytkownik.objects.all().order_by('-punkty')[:5]
    top_punkty_dzien = Uzytkownik.objects.all().order_by('-punkty_dzien')[:5]

    return render(request, 'wisielec.html', {
        'wyswietl_slowo': wyswietl_slowo,
        'numer_img': numer_img,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'slowo': slowo if przegrana else None,
        'litery_status': litery_status,
        'top_punkty': top_punkty,
        'top_punkty_dzien': top_punkty_dzien,
    })

def losuj_przyslowie():
    try:
        przyslowia = Przyslowie.objects.all()
        if not przyslowia.exists():
            return "przyklad"
        przyslowie = random.choice(przyslowia)
        return przyslowie.tekst
    except Exception as e:
        return str(e)

def gra_przyslowie(request):
    alfabet = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"

    przyslowie = request.session.get('przyslowie')
    if not przyslowie:
        przyslowie = losuj_przyslowie()
        request.session['przyslowie'] = przyslowie

    pozostale_proby = request.session.get('pozostale_proby', 6)
    odgadniete_litery = request.session.get('odgadniete_litery', '')

    if request.method == "POST":
        litera = request.POST.get('litera', '').lower()
        if litera and litera not in odgadniete_litery:
            odgadniete_litery += litera
            if litera not in przyslowie.lower():
                pozostale_proby -= 1

    wyswietl_przyslowie = ''.join(
        [litera if litera.lower() in odgadniete_litery else '_' if litera.isalpha() else litera
         for litera in przyslowie]
    )
    wygrana = '_' not in wyswietl_przyslowie
    przegrana = pozostale_proby <= 0

    litery_status = {lit: "zielony" if lit in odgadniete_litery and lit in przyslowie.lower()
                     else "czerwony" if lit in odgadniete_litery else "szary"
                     for lit in alfabet}
    numer_img = 6 - pozostale_proby

    if wygrana:
        uzytkownik = Uzytkownik.objects.get(id=request.session['user_id'])
        aktualizuj_punkty(uzytkownik, 2)

    if wygrana or przegrana:
        request.session['pozostale_proby'] = 6
        request.session['odgadniete_litery'] = ''
        request.session['przyslowie'] = losuj_przyslowie()
        request.session['numer_img'] = numer_img
    else:
        request.session['pozostale_proby'] = pozostale_proby
        request.session['odgadniete_litery'] = odgadniete_litery
        request.session['numer_img'] = numer_img

    top_punkty = Uzytkownik.objects.all().order_by('-punkty')[:5]
    top_punkty_dzien = Uzytkownik.objects.all().order_by('-punkty_dzien')[:5]

    return render(request, 'przyslowia.html', {
        'wyswietl_przyslowie': wyswietl_przyslowie,
        'numer_img': numer_img,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'przyslowie': przyslowie if przegrana else None,
        'litery_status': litery_status,
        'top_punkty': top_punkty,
        'top_punkty_dzien': top_punkty_dzien,
    })



def wybor_trybu(request):
    # Resetowanie danych sesji
    request.session['slowo'] = None
    request.session['przyslowie'] = None
    request.session['odgadniete_litery'] = ''
    request.session['pozostale_proby'] = 6
    request.session['czas_start'] = None
    request.session['czas_limit'] = None
    return render(request, 'wybor_trybu.html')


def szybki_wisielec(request):
    alfabet = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"
    slowo = request.session.get('slowo')
    pozostale_proby = request.session.get('pozostale_proby', 6)
    odgadniete_litery = request.session.get('odgadniete_litery', '')
    czas_pozostaly = request.session.get('czas_pozostaly', 30)
    numer_img = 6 - pozostale_proby
    if not slowo:
        slowo = losuj_slowo()
        pozostale_proby = 6
        odgadniete_litery = ''
        czas_pozostaly = 30
        request.session['slowo'] = slowo
        request.session['pozostale_proby'] = pozostale_proby
        request.session['odgadniete_litery'] = odgadniete_litery
        request.session['czas_pozostaly'] = czas_pozostaly
        request.session['numer_img'] = numer_img

    if request.method == "POST" and 'litera' in request.POST:
        litera = request.POST.get('litera', '').lower()
        if litera and litera not in odgadniete_litery:
            odgadniete_litery += litera
            if litera not in slowo.lower():
                pozostale_proby -= 1
        request.session['odgadniete_litery'] = odgadniete_litery
        request.session['pozostale_proby'] = pozostale_proby
        request.session['numer_img'] = numer_img

    wyswietl_slowo = ''.join(
        [litera if litera.lower() in odgadniete_litery else '_' for litera in slowo]
    ) if slowo else ''
    wygrana = '_' not in wyswietl_slowo and slowo
    przegrana = pozostale_proby <= 0 or czas_pozostaly <= 0

    if request.method == "POST" and request.POST.get('nowa_gra') == 'true':
        slowo = losuj_slowo()
        pozostale_proby = 6
        odgadniete_litery = ''
        czas_pozostaly = 30
        request.session['slowo'] = slowo
        request.session['pozostale_proby'] = pozostale_proby
        request.session['odgadniete_litery'] = odgadniete_litery
        request.session['czas_pozostaly'] = czas_pozostaly
        request.session['numer_img'] = numer_img

    if wygrana:
        uzytkownik = Uzytkownik.objects.get(id=request.session['user_id'])
        aktualizuj_punkty(uzytkownik, 5)

    if wygrana or przegrana:
        request.session['slowo'] = None

    litery_status = {lit: "zielony" if lit in odgadniete_litery and lit in (slowo or '').lower()
                     else "czerwony" if lit in odgadniete_litery else "szary"
                     for lit in alfabet}

    top_punkty = Uzytkownik.objects.all().order_by('-punkty')[:5]
    top_punkty_dzien = Uzytkownik.objects.all().order_by('-punkty_dzien')[:5]

    return render(request, 'szybki_wisielec.html', {
        'wyswietl_slowo': wyswietl_slowo,
        'numer_img': numer_img,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'slowo': slowo,
        'litery_status': litery_status,
        'czas_pozostaly': czas_pozostaly,
        'top_punkty': top_punkty,
        'top_punkty_dzien': top_punkty_dzien,
    })


def aktualizuj_czas(request):
    slowo = request.session.get('slowo')
    czas_pozostaly = request.session.get('czas_pozostaly', 0)

    if slowo and czas_pozostaly > 0:  # Odliczaj czas tylko podczas gry
        czas_pozostaly -= 1
        request.session['czas_pozostaly'] = czas_pozostaly

    return JsonResponse({'czas_pozostaly': czas_pozostaly})
