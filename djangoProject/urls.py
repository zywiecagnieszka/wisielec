"""
URL configuration for djangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main_page, name='main_page'),
    path('zasady/', views.zasady, name='zasady'),
    path('gra/', views.gra_wisielec, name='gra_wisielec'),
    path('graprzyslowie/', views.gra_przyslowie, name='gra_przyslowie'),
    path('wybor_trybu/', views.wybor_trybu, name='wybor_trybu'),
    path('szybki_wisielec/', views.szybki_wisielec, name='szybki_wisielec'),
    path('aktualizuj_czas/', views.aktualizuj_czas, name='aktualizuj_czas'),
    path('rejestracja/', views.rejestracja, name='rejestracja'),
    path('logowanie/', views.logowanie, name='logowanie'),

]
