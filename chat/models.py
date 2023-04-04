from django.db import models
from django.conf import settings


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
