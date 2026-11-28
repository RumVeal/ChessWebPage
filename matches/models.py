from django.db import models
from players.models import Player

# Create your models here.
class Match(models.Model):
    class Result(models.TextChoices):
        WHITE_WON = "1-0", "White won"
        BLACK_WON = "0-1", "Black won"
        DRAW = "1/2-1/2", "Draw"
    
    class TimeControl(models.TextChoices):
        BULLET = "bullet", "Bullet"
        BLITZ = "blitz", "Blitz"
        RAPID = "rapid", "Rapid"
    
    class Source(models.TextChoices):
        LICHESS = "lichess", "Lichess"
        CHESSCOM = "chesscom", "Chess.com"
        MANUAL = "manual", "Manual"
        
    class Meta:
        verbose_name_plural = "Matches"
    
    white = models.ForeignKey(Player, on_delete=models.PROTECT, related_name="games_as_white")
    black = models.ForeignKey(Player, on_delete=models.PROTECT, related_name="games_as_black")
    
    result = models.CharField(max_length=10, choices=Result.choices)
    time_control = models.CharField(max_length=10, choices=TimeControl.choices)
    source = models.CharField(max_length=10, choices=Source.choices, default=Source.MANUAL)
    
    external_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    url = models.URLField(blank=True)
    
    white_rating_change = models.IntegerField(null=True, verbose_name="White rating change", blank=True)
    black_rating_change = models.IntegerField(null=True, verbose_name="Black rating change", blank=True)
    
    played_at = models.DateTimeField()
    
    def __str__(self):
        return f"{self.white} - {self.black} {self.result}"