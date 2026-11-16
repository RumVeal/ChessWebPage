from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Player
from datetime import date

# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            player = Player.objects.create(user=user, name=user.username, enter_date=date.today())
            login(request, user)
            return redirect('/admin/')
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})