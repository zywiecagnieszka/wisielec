from django.shortcuts import render

def main_page(request):
    return render(request, 'strona_glowna.html')

def zasady(request):
    return render(request, 'zasady.html')
