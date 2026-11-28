from django.contrib import admin
from .models import Match

# Register your models here.
@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('white', 'black', 'result', 'time_control', 'played_at',)
    list_filter = ('time_control', 'source',)