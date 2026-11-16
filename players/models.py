from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    # Account
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Club
    name = models.CharField(max_length=100)
    enter_date = models.DateField(verbose_name="Join date")
    club_rating = models.IntegerField(default=500)
    ratings_updated_at = models.DateTimeField(null=True, blank=True)
    
    # Chesscom
    chesscom_nickname = models.CharField(max_length=100, verbose_name="Chess.com Nickname", blank=True)
    chesscom_rapid_rating = models.IntegerField(null=True, verbose_name="Chess.com Rapid", blank=True)
    chesscom_bullet_rating = models.IntegerField(null=True, verbose_name="Chess.com Bullet", blank=True)
    chesscom_blitz_rating = models.IntegerField(null=True, verbose_name="Chess.com Blitz", blank=True)
    
    # Lichess
    lichess_nickname = models.CharField(max_length=100, verbose_name="Lichess Nickname", blank=True)
    lichess_rapid_rating = models.IntegerField(null=True, verbose_name="Lichess Rapid", blank=True)
    lichess_rapid_prov = models.BooleanField(default=False, verbose_name="Lichess Rapid provisional")
    lichess_bullet_rating = models.IntegerField(null=True, verbose_name="Lichess Bullet", blank=True)
    lichess_bullet_prov = models.BooleanField(default=False, verbose_name="Lichess Bullet provisional")
    lichess_blitz_rating = models.IntegerField(null=True, verbose_name="Lichess Blitz", blank=True)
    lichess_blitz_prov = models.BooleanField(default=False, verbose_name="Lichess Blitz provisional")
    
    def __str__(self):
        return self.name