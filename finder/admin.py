from django.contrib import admin
from .models import SeekerProfile, Room, Interest
@admin.register(SeekerProfile)
class SeekerAdmin(admin.ModelAdmin):
    list_display=["name","age","gender","city","budget_min","budget_max","food_pref"]
    list_filter=["city","gender","food_pref"]
    search_fields=["name","city"]
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=["title","city","area","rent","room_type"]
    list_filter=["city","room_type"]
@admin.register(Interest)
class InterestAdmin(admin.ModelAdmin):
    list_display=["from_profile","to_profile","status","created_at"]
    list_filter=["status"]
