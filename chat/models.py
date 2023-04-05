from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete

from mysite.json_extended import ExtendedJSONEncoder, ExtendedJSONDecoder


# Create your models here.
class OnlineUserMixin(models.Model):
    class Meta:
        abstract = True

    online_user_set = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        # 하나의관계를 저장할 모델을 지정한다.
        through="RoomMember",
        blank=True,
        # user.joined_room_set.all()코드로 user가 참여한 모든 방 목록 조회
        related_name="joined_room_set",
    )

    # 현재방에 있는 유저들 출력
    def get_online_users(self):
        return self.online_user_set.all()

    def get_online_usernames(self):
        qs = self.get_online_users().values_list("username", flat=True)
        return list(qs)

        # 지정 유정가 현재 방에 접속했는지 여부

    def is_joined_user(self, user):
        return self.get_online_users().filter(pk=user.pk).exists()

    def user_join(self, channel_name, user):
        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            room_member = RoomMember(room=self, user=user)

        is_new_join = len(room_member.channel_names) == 0
        room_member.channel_names.add(channel_name)

        if room_member.pk is None:
            room_member.save()
        else:
            room_member.save(update_fields=["channel_names"])

        return is_new_join

        # 현재 방으로부터 최종 접속 종료 여부 반환

    def user_leave(self, channel_name, user):
        try:
            room_member = RoomMember.objects.get(room=self, user=user)
        except RoomMember.DoesNotExist:
            return True

        room_member.channel_names.remove(channel_name)
        if not room_member.channel_names:
            room_member.delete()
            return True
        else:
            room_member.save(update_fields=["channel_names"])
            return False


class Room(OnlineUserMixin, models.Model):
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


class RoomMember(models.Model):
    # 하나의 유저가 하나의 Room 간의 관계를 1회 저장한다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # 하나의 유저가 하나의 room에 다수 접속할 수 있다.
    # 각 접속에서의 채널명 목록에 집합으로 저장하여, 최초 접속 및 최종 접속종료를 인지하게 한다.
    # 디폴트로 빈 집합이 생성되도록한다.
    channel_names = models.JSONField(
        default=set,
        encoder=ExtendedJSONEncoder,
        decoder=ExtendedJSONDecoder,
    )
