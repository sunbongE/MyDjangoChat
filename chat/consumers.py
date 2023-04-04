from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from .models import Room


class ChatConsumer(JsonWebsocketConsumer):
    # 고정 그룹명을 사용한 코드
    # SQUARE_GROUP_NAME = "square"
    # groups = [SQUARE_GROUP_NAME]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 인스턴스 변수는 생성자 내에서 정의
        self.group_name = ""  # 인스턴스 변수 이름 추가

    def connect(self):
        user = self.scope["user"]
        if not user.is_authenticated:
            self.close()
        else:
            # chat/routing.py에 변수로 오는 url에 따라서 방이름이 변하는것
            # 예시
            # /ws/chat/test/chat/ 요청이면 self.scope["url_route"]값은
            # {'args':(),'kwargs':{'room_name':'test'}} 이다.
            room_pk = self.scope["url_route"]["kwargs"]["room_pk"]
            self.group_name = Room.make_chat_group_name(room_pk=room_pk)
            # self.group_name = f"chat-{room_pk}"
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name,
            )  # 본 웹소켓 허용
            # connect 메서드 기본 구현에서는 self.accpet()호출부만 있다.
            self.accept()

    def disconnect(self, code):
        # 소속 그룹에서 빠져나옴
        if self.group_name:
            async_to_sync(self.channel_layer.group_discard)(
                self.group_name,
                self.channel_name,
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
