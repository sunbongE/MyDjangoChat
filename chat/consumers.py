from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from .models import Room


# 클래스로 정의해야한다.
class ChatConsumer(JsonWebsocketConsumer):
    # 고정 그룹명을 사용한 코드
    # SQUARE_GROUP_NAME = "square"
    # groups = [SQUARE_GROUP_NAME]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 인스턴스 변수는 생성자 내에서 정의
        self.group_name = ""  # 인스턴스 변수 이름 추가
        self.room = None

    def connect(self):
        user = self.scope["user"]

        if not user.is_authenticated:
            self.close()
        else:
            room_pk = self.scope["url_route"]["kwargs"]["room_pk"]

            try:
                self.room = Room.objects.get(pk=room_pk)
            except Room.DoesNotExist:
                self.close()
            else:
                self.group_name = self.room.chat_group_name

                is_new_join = self.room.user_join(self.channel_name, user)
                if is_new_join:
                    async_to_sync(self.channel_layer.group_send)(
                        self.group_name,
                        {
                            "type": "chat.user.join",
                            "username": user.username,
                        },
                    )

                async_to_sync(self.channel_layer.group_add)(
                    self.group_name,
                    self.channel_name,
                )

                self.accept()

    def disconnect(self, code):
        # 소속 그룹에서 빠져나옴
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name,
            )
        user = self.scope["user"]
        if self.room is not None:
            is_last_leave = self.room.user_leave(self.channel_name, user)
            if is_last_leave:
                async_to_sync(self.channel_layer.group_send)(
                    self.group_name,
                    {
                        "type": "chat.user.leave",
                        "username": user.username,
                    },
                )

    def chat_user_join(self, message_dict):
        self.send_json(
            {
                "type": "chat.user.join",
                "username": message_dict["username"],
            }
        )

    def chat_user_leave(self, message_dict):
        self.send_json(
            {
                "type": "chat.user.leave",
                "username": message_dict["username"],
            }
        )

    def receive_json(self, content, **kwargs):
        user = self.scope["user"]
        _type = content["type"]
        if _type == "chat.message":
            message = content["message"]
            sender = user.username
            async_to_sync(self.channel_layer.group_send)(
                self.group_name,
                {
                    "type": "chat.message",
                    "message": message,
                    "sender": sender,
                },
            )
        else:
            print(f"Invalid message type : ${_type}")

    def chat_message(self, message_dict):
        self.send_json(
            {
                "type": "chat.message",
                "message": message_dict["message"],
                "sender": message_dict["sender"],
            }
        )

    def chat_room_deleted(self, message_dict):
        custom_code = 4000
        self.close(code=custom_code)
