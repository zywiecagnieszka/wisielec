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
