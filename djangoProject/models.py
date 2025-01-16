from django.db import models

class Slowo(models.Model):
    tekst = models.CharField(max_length=255, db_column='tresc')  

    class Meta:
        db_table = 'slowa'

    def __str__(self):
        return self.tekst

class Przyslowie(models.Model):
    tekst = models.CharField(max_length=255, db_column='tresc')

    class Meta:
        db_table = 'przyslowia'

    def __str__(self):
        return self.tekst

class Uzytkownik(models.Model):
    login = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    haslo = models.CharField(max_length=255)
    punkty = models.IntegerField(default=0)
    punkty_dzien = models.IntegerField(default=0)
    data = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.login