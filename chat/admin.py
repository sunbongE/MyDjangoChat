from django.contrib import admin
from chat.models import Room, RoomMember

# Register your models here.


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(RoomMember)
class RoomMemberAdmin(admin.ModelAdmin):
    pass