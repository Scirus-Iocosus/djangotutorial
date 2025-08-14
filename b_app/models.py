from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date

TEAM_CHOICES = [
    ('Rossi', 'Rossi'),
    ('Blu', 'Blu'),
    ('Verdi', 'Verdi'),
    ('Gialli', 'Gialli'),
]

class PunteggiRossi(models.Model):
    punteggio = models.IntegerField()  
    def __str__(self):
        return f"Punteggio: {self.punteggio}"

class PunteggiVerdi(models.Model):
    punteggio = models.IntegerField()  
    def __str__(self):
        return f"Punteggio: {self.punteggio}"

class PunteggiGialli(models.Model):
    punteggio = models.IntegerField()  
    def __str__(self):
        return f"Punteggio: {self.punteggio}"

class PunteggiBlu(models.Model):
    punteggio = models.IntegerField()  
    def __str__(self):
        return f"Punteggio: {self.punteggio}"

class cucina(models.Model):
    mansione = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.mansione}"
class sino(models.Model):
    risposta = models.CharField(max_length=2)
    def __str__(self):
        return f"{self.risposta}"
class pagamenti(models.Model):
    cash = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.cash}"

class Iscritto(models.Model):
    nome_figlio = models.CharField(max_length=100)
    cognome_figlio = models.CharField(max_length=100)
    squadra = models.CharField(max_length=10, blank=True, null=True, choices=TEAM_CHOICES)
    padre = models.CharField(max_length=100, blank=True, null=True)
    madre = models.CharField(max_length=100, blank=True, null=True)
    tutore = models.CharField(max_length=100, blank=True, null=True)
    data_figlio = models.DateField()
    luogo_nascita = models.CharField(max_length=100)
    residenza = models.CharField(max_length=150)
    fratelli = models.BooleanField(default=False)
    telefono1 = PhoneNumberField(region='IT')
    telefono2 = PhoneNumberField(region='IT', blank=True, null=True)
    allergie = models.CharField(max_length=255, blank=True, null=True)
    foto = models.BooleanField(default=False)
    sito = models.BooleanField(default=False)
    uscita_autonoma = models.BooleanField(default=False)
    cucina = models.ManyToManyField('cucina', blank=True)
    contatti = models.CharField(max_length=200, blank=True, null=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    gita = models.BooleanField(default=False)
    necessita = models.CharField(max_length=500, blank=True, null=True)
    documento = models.FileField(upload_to='documenti/', blank=True, null=True)
    pagamenti = models.ManyToManyField('pagamenti', blank=True)
    laboratori = models.BooleanField(default=False)

    @property
    def eta(self):
        if self.data_figlio:
            oggi = date.today()
            return oggi.year - self.data_figlio.year - (
                (oggi.month, oggi.day) < (self.data_figlio.month, self.data_figlio.day)
            )
        return None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cognome_figlio} {self.nome_figlio} - { self.eta } - { self.squadra }"

class Presenza(models.Model):
    animato = models.ForeignKey(Iscritto, on_delete=models.CASCADE)
    data = models.DateField()
    entrata = models.BooleanField(default=False)
    uscita = models.BooleanField(default=False)

class file(models.Model):
    Nome = models.CharField(max_length=500)
    Documento = models.FileField(upload_to='documenti/')
    
    def __str__(self):
        return f"{self.Nome} ({self.Documento})"

class DownloadPerGenitori(models.Model):
    Nome = models.CharField(max_length=500)
    Documento = models.FileField(upload_to='documenti/')
    
    def __str__(self):
        return f"{self.Nome} ({self.Documento})"

