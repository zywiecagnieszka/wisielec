from django.shortcuts import render

def main_page(request):
    return render(request, 'strona_glowna.html')

def zasady(request):
    return render(request, 'zasady.html')

def gra_wisielec(request):
    slowo = "przyklad"
    pozostale_proby = 6
    odgadniete_litery = ""

    if request.method == "POST":
        odgadniete_litery = request.POST.get('odgadniete_litery', '')
        litera = request.POST.get('litera', '').lower()
        pozostale_proby = int(request.POST.get('pozostale_proby', 6))

        #sprawdzanie poszczegolnych liter
        if litera and litera not in odgadniete_litery:
            odgadniete_litery += litera
            if litera not in slowo:
                pozostale_proby -= 1

    wyswietl_slowo = ' '.join(
        [litera if litera in odgadniete_litery else '_' for litera in slowo]
    )

    wygrana = '_' not in wyswietl_slowo
    przegrana = pozostale_proby <= 0

    return render(request, 'wisielec.html', {
        'wyswietl_slowo': wyswietl_slowo,
        'pozostale_proby': pozostale_proby,
        'odgadniete_litery': odgadniete_litery,
        'wygrana': wygrana,
        'przegrana': przegrana,
        'slowo': slowo if przegrana else None
    })