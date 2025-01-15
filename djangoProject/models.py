from django.db import models

class Slowo(models.Model):
    tekst = models.CharField(max_length=255, db_column='tresc')  # Mapowanie na kolumnę 'tresc'

    class Meta:
        db_table = 'slowa'  # Powiązanie z tabelą 'slowo'

    def __str__(self):
        return self.tekst
