from django import forms
from .models import Player

class PlayerProfileForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'lichess_nickname', 'chesscom_nickname']

class PlayerNameForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']