from django.shortcuts import render
import random

def losuj_slowo():
    otworz_plik = 'djangoProject/slowa.txt'
    try:
        with open(otworz_plik, 'r') as plik:
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
    slowo = request.session.get('slowo')
    if not slowo:
        slowo = losuj_slowo()
        request.session['slowo'] = slowo

    pozostale_proby = request.session.get('pozostale_proby', 6)
    odgadniete_litery = request.session.get('odgadniete_litery', '')

    if request.method == "POST":
        odgadniete_litery = request.POST.get('odgadniete_litery', odgadniete_litery)
        litera = request.POST.get('litera', '').lower()
        pozostale_proby = int(request.POST.get('pozostale_proby', pozostale_proby))

        if litera not in odgadniete_litery:
            odgadniete_litery += litera
            if litera not in slowo:
                pozostale_proby -= 1

    wyswietl_slowo = ' '.join(
        [litera if litera in odgadniete_litery else '_' for litera in slowo]
    )
    wygrana = '_' not in wyswietl_slowo
    przegrana = pozostale_proby <= 0

    if wygrana or przegrana:
        request.session['pozostale_proby'] = 6
        request.session['odgadniete_litery'] = ''
        request.session['slowo'] = losuj_slowo()

    if not wygrana and not przegrana:
        request.session['pozostale_proby'] = pozostale_proby
        request.session['odgadniete_litery'] = odgadniete_litery

    return render(request, 'wisielec.html', {
        'wyswietl_slowo': wyswietl_slowo,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'slowo': slowo if przegrana else None
    })

def losuj_przyslowie():
    otworz_plik = 'djangoProject/przyslowia.txt'
    try:
        with open(otworz_plik, 'r', encoding='utf-8') as plik:  # Dodano encoding='utf-8'
            przyslowia = plik.readlines()
        przyslowia = [przyslowie.strip() for przyslowie in przyslowia if przyslowie.strip()]
        return random.choice(przyslowia)
    except FileNotFoundError:
        return "przyklad przyslowia"
    except UnicodeDecodeError as e:
        print(f"Błąd odczytu pliku: {e}")
        return "błąd kodowania pliku"



def gra_przyslowie(request):
    przyslowie = request.session.get('przyslowie')
    if not przyslowie:
        przyslowie = losuj_przyslowie()
        request.session['przyslowie'] = przyslowie

    pozostale_proby = request.session.get('pozostale_proby', 6)
    odgadniete_litery = request.session.get('odgadniete_litery', '')

    if request.method == "POST":
        odgadniete_litery = request.POST.get('odgadniete_litery', odgadniete_litery)
        litera = request.POST.get('litera', '').lower()
        pozostale_proby = int(request.POST.get('pozostale_proby', pozostale_proby))

        if litera not in odgadniete_litery:
            odgadniete_litery += litera
            if litera not in przyslowie.lower():
                pozostale_proby -= 1

    wyswietl_przyslowie = ''
    for litera in przyslowie:
        if not litera.isalpha():
            wyswietl_przyslowie += litera
        else:
            if litera.lower() in odgadniete_litery:
                wyswietl_przyslowie += litera
            else:
                wyswietl_przyslowie += '_'

    wygrana = '_' not in wyswietl_przyslowie
    przegrana = pozostale_proby <= 0

    if wygrana or przegrana:
        request.session['pozostale_proby'] = 6
        request.session['odgadniete_litery'] = ''
        request.session['przyslowie'] = losuj_przyslowie()

    if not wygrana and not przegrana:
        request.session['pozostale_proby'] = pozostale_proby
        request.session['odgadniete_litery'] = odgadniete_litery

    return render(request, 'przyslowia.html', {
        'wyswietl_przyslowie': wyswietl_przyslowie,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'przyslowie': przyslowie if przegrana else None
    })


def wybor_trybu(request):
    return render(request, 'wybor_trybu.html')
