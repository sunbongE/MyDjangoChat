from django.urls import path
from chat import views

app_name = "chat"

urlpatterns = [
    path("new/", views.room_new, name="room_new"),
    path("", views.index, name="index"),
    path("<str:room_pk>/chat/", views.room_chat, name="room_chat"),
    path("<str:room_pk>/delete/", views.room_delete, name="room_delete"),
]
