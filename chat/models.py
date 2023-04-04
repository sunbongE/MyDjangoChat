from django.db import models
from django.conf import settings
from channels.layers import get_channel_layer
from django.db.models.signals import post_delete
from asgiref.sync import async_to_sync


# Create your models here.
class Room(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_room_set",
    )
    # 한글 채팅방 이름 필드
    name = models.CharField(max_length=100)

    class Meta:
        # 퀘리셋 디폴트 정렬옵션 지정을 추천
        ordering = ["-pk"]

    @property
    def chat_group_name(self):
        return self.make_chat_group_name(room=self)

    @staticmethod
    def make_chat_group_name(room=None, room_pk=None):
        return "chat-%s" % (room_pk or room.pk)


def room__on_post_delete(instance, **kwargs):
    # Consumer Instance밖에서 채팅방 그룹에 속한
    # 모든 Consumer Instance들에게
    # send message =>  chat.room.deletd
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        instance.chat_group_name,
        {
            "type": "chat.room.deleted",
        },
    )


post_delete.connect(  # Room 삭제시 호출될 함수를 지정한다.
    room__on_post_delete, sender=Room, dispatch_uid="room__on_post_delete"
)
