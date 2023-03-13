from channels.generic.websocket import WebsocketConsumer
import json
class EchoConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        obj = json.loads(text_data) # 문자열에서 객체로 역직렬화
        print("수신 : ",obj)

        json_string = json.dumps({ # 객체를 문자열로 직렬화
            "content": obj["content"],
            "user": obj["user"],
        })
        self.send(json_string)
        # send api에서는 텍스트 혹은 바이너리 데이터만 전송가능하다.
        # 그래서 객체로 온 데이터를 직렬화해야 한다.