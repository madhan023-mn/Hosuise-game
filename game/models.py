from django.db import models
from django.conf import settings

class Game(models.Model):
    STATUS_CHOICES = (
        ('Waiting', 'Waiting'),
        ('Running', 'Running'),
        ('Paused', 'Paused'),
        ('Finished', 'Finished'),
    )
    
    game_code = models.CharField(max_length=10, unique=True)
    operator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='games_operated')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Waiting')
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Game {self.game_code} - {self.status}"

class CalledNumber(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='called_numbers')
    number = models.IntegerField()
    order = models.IntegerField()
    called_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('game', 'number')
        ordering = ['order']

    def __str__(self):
        return f"{self.game.game_code} - {self.number} (Order: {self.order})"
