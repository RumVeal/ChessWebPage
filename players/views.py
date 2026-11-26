from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.contrib import messages
from django.http import Http404
from .models import Player
from datetime import date
from .forms import PlayerProfileForm, PlayerNameForm
from .services import update_player_ratings



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

def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    if not player.is_member and request.user != player.user:
        raise Http404
    return render(request, "players/player_detail.html", {"player": player})

@login_required
def profile_edit(request):
    player = get_object_or_404(Player, user=request.user)
    if player.is_member:
        FormClass = PlayerProfileForm
    else:
        FormClass = PlayerNameForm
    if request.method == "POST":
        form = FormClass(request.POST, instance=player)
        if form.is_valid():
            form.save()
            errors = []
            if player.is_member:
                errors = update_player_ratings(player)
            if not errors:
                messages.success(request, "Profile updated")
            for error in errors:
                messages.warning(request, error)
            return redirect('player_detail', pk=player.pk)
    else:
        form = FormClass(instance=player)
    return render(request, "players/profile_edit.html", {"form": form})