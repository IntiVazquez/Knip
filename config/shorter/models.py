from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import random, string


class URL(models.Model):
    # Validación que permite solo letras y números
    short_url_validator = RegexValidator(
        regex='^[a-zA-Z0-9]*$',
        message="El short_url solo puede contener letras y números."
    )

    raw_url = models.URLField()
    short_url = models.CharField(
        max_length=20, 
        unique=True, 
        validators=[short_url_validator]
    )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    creation_date = models.DateTimeField(default=timezone.now)
    clicks = models.IntegerField(default=0)
    last_click_date = models.DateTimeField(null=True, blank=True)

    def used(self):
        self.clicks += 1
        self.last_click_date = timezone.now()
        self.save()

    def random_url():
        random_url = ''.join(random.choices(string.ascii_letters, k=6))
        return random_url

    def __str__(self):
        page_url = 'knip.vercel.app'
        return f"{page_url}/{self.short_url}"

    def get_creation_date(self):
        return self.creation_date.strftime('%d de %B de %Y').capitalize()

    def get_last_click_date(self):
        if self.clicks == 0:
            return "Nunca clickeado"
        else:
            fecha = self.last_click_date.strftime('%d de %B de %Y').capitalize()
            return f"Ultimo click: {fecha}"