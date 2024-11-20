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

        if litera and litera not in odgadniete_litery:
            odgadniete_litery += litera
            if litera not in slowo:
                pozostale_proby -= 1

    wyswietl_slowo = ' '.join(
        [litera if litera in odgadniete_litery else '_' for litera in slowo]
    )
    wygrana = '_' not in wyswietl_slowo
    przegrana = pozostale_proby <= 0

    if wygrana or przegrana:
        # Resetowanie wszystkich danych w sesji
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

