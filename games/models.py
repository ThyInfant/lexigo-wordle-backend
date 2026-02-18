from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    target_word = models.CharField(max_length=5)
    attempts_remaining = models.IntegerField(default=6)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Game {self.id} - {self.status}"


class Guess(models.Model):
    game = models.ForeignKey(Game, related_name="guesses", on_delete=models.CASCADE)
    guess_word = models.CharField(max_length=5)
    feedback = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Guess {self.guess_word} for Game {self.game.id}"