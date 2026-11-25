from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Player
from datetime import date
from django.db.models import F

MODES = ['bullet', 'blitz', 'rapid']

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            player = Player.objects.create(user=user, name=user.username, enter_date=date.today())
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

def home(request):
    top_players = (Player.objects.select_related('user')
                   .filter(is_member=True)
                   .order_by('-club_rating')[:5])
    return render(request, "home.html", {"top_players": top_players})

def player_list(request):
    mode = request.GET.get('mode', 'blitz')
    if mode not in MODES: 
        mode = 'blitz'
    all_players = (Player.objects.select_related('user')
                   .filter(is_member=True)
                   .order_by('-club_rating')
                   .annotate(lichess=F(f"lichess_{mode}_rating"), 
                             chesscom=F(f"chesscom_{mode}_rating")))
    return render(request, "players/player_list.html", {"all_players": all_players, "mode": mode, "MODES": MODES})