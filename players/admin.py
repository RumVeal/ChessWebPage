from django.contrib import admin
from .models import Player

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'club_rapid_rating', 'is_member')
    list_editable = ('is_member',)
    list_filter = ('is_member',)