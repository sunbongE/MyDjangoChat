from django.shortcuts import render, redirect
from chat.forms import RoomForm
from chat.models import Room
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse


@login_required
def room_users(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    if not room.is_joined_user(request.user):
        return HttpResponse("Unauthorized user", status=401)

    username_list = room.get_online_usernames()
    return JsonResponse({"username_list": username_list})


@login_required
def room_delete(request, room_pk):
    room = get_object_or_404(Room, pk=room_pk)

    if room.owner != request.user:
        messages.error(request, "채팅방 소유자가 아닙니다.")
        return redirect("chat:index")

    if request.method == "POST":
        room.delete()  # db에서 삭제
        messages.success(request, "채팅방을 삭제했습니다.")
        return redirect("chat:index")
    return render(
        request,
        "chat/room_confirm_delete.html",
        {
            "room": room,
        },
    )


@login_required
def room_new(request):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            created_room: Room = form.save(commit=False)
            created_room.owner = request.user
            created_room.save()
            return redirect("chat:room_chat", created_room.pk)
    else:
        form = RoomForm()
    return render(
        request,
        "chat/room_form.html",
        {
            "form": form,
        },
    )


# Create your views here.
def index(request):
    room_qs = Room.objects.all()

    return render(
        request,
        "chat/index.html",
        {
            "room_list": room_qs,
        },
    )


@login_required
def room_chat(request, room_pk):
    user = request.user.username
    # print(user)
    room = get_object_or_404(Room, pk=room_pk)
    return render(
        request,
        "chat/room_chat.html",
        {
            "room": room,
        },
    )
