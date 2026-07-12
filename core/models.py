from django.db import models

class Settings(models.Model):
    company_name = models.CharField(max_length=100, default="Housie Club")
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    theme = models.CharField(max_length=20, default='light')
    sound = models.BooleanField(default=True)
    language = models.CharField(max_length=10, default='en')

    def __str__(self):
        return "Global Settings"
