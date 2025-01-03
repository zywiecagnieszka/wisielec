from django.shortcuts import render
import random
import time
from django.http import JsonResponse
import json

def losuj_slowo():
    otworz_plik = 'djangoProject/slowa.txt'
    try:
        with open(otworz_plik, 'r', encoding='utf-8') as plik:
            slowa = plik.readlines()
        slowa = [slowo.strip() for slowo in slowa if slowo.strip()]
        return random.choice(slowa)
    except FileNotFoundError:
        return "przyklad"
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

    if wygrana or przegrana:
        request.session['pozostale_proby'] = 6
        request.session['odgadniete_litery'] = ''
        request.session['slowo'] = losuj_slowo()
        request.session['numer_img'] = numer_img
    else:
        request.session['pozostale_proby'] = pozostale_proby
        request.session['odgadniete_litery'] = odgadniete_litery
        request.session['numer_img'] = numer_img

    return render(request, 'wisielec.html', {
        'wyswietl_slowo': wyswietl_slowo,
        'numer_img': numer_img,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'slowo': slowo if przegrana else None,
        'litery_status': litery_status
    })


def losuj_przyslowie():
    otworz_plik = 'djangoProject/przyslowia.txt'
    try:
        with open(otworz_plik, 'r', encoding='utf-8') as plik:
            przyslowia = plik.readlines()
        przyslowia = [przyslowie.strip() for przyslowie in przyslowia if przyslowie.strip()]
        return random.choice(przyslowia)
    except FileNotFoundError:
        return "przyklad przyslowia"
    except UnicodeDecodeError as e:
        print(f"Błąd odczytu pliku: {e}")
        return "błąd kodowania pliku"



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

    if wygrana or przegrana:
        request.session['pozostale_proby'] = 6
        request.session['odgadniete_litery'] = ''
        request.session['przyslowie'] = losuj_przyslowie()
        request.session['numer_img'] = numer_img
    else:
        request.session['pozostale_proby'] = pozostale_proby
        request.session['odgadniete_litery'] = odgadniete_litery
        request.session['numer_img'] = numer_img

    return render(request, 'przyslowia.html', {
        'wyswietl_przyslowie': wyswietl_przyslowie,
        'numer_img': numer_img,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'przyslowie': przyslowie if przegrana else None,
        'litery_status': litery_status
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

    if wygrana or przegrana:
        request.session['slowo'] = None

    litery_status = {lit: "zielony" if lit in odgadniete_litery and lit in (slowo or '').lower()
                     else "czerwony" if lit in odgadniete_litery else "szary"
                     for lit in alfabet}

    return render(request, 'szybki_wisielec.html', {
        'wyswietl_slowo': wyswietl_slowo,
        'numer_img': numer_img,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'slowo': slowo,
        'litery_status': litery_status,
        'czas_pozostaly': czas_pozostaly
    })



def aktualizuj_gra(request):

    alfabet = "aąbcćdeęfghijklłmnńoópqrsśtuvwxyzźż"
    slowo = request.session.get('slowo')
    pozostale_proby = request.session.get('pozostale_proby', 6)
    odgadniete_litery = request.session.get('odgadniete_litery', '')
    czas_pozostaly = request.session.get('czas_pozostaly', 30)
    numer_img = 6 - pozostale_proby

    data = json.loads(request.body)
    litera = data.get('litera')


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
    
    if wygrana or przegrana:
        request.session['slowo'] = None

    litery_status = {lit: "zielony" if lit in odgadniete_litery and lit in (slowo or '').lower()
                     else "czerwony" if lit in odgadniete_litery else "szary"
                     for lit in alfabet}

    print (litera)
    print(pozostale_proby)
    print(odgadniete_litery)
    print(wyswietl_slowo)
    print(numer_img)
    print(wygrana)
    return JsonResponse({
        'wyswietl_slowo': wyswietl_slowo,
        'numer_img': numer_img,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'slowo': slowo,
        'litery_status': litery_status,
    })

def aktualizuj_czas(request):
    slowo = request.session.get('slowo')
    czas_pozostaly = request.session.get('czas_pozostaly', 0)

    if slowo and czas_pozostaly > 0:  # Odliczaj czas tylko podczas gry
        czas_pozostaly -= 1
        request.session['czas_pozostaly'] = czas_pozostaly

    return JsonResponse({'czas_pozostaly': czas_pozostaly})
