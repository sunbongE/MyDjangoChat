from channels.generic.websocket import WebsocketConsumer
import json


class EchoConsumer(WebsocketConsumer):
    def receive(self, text_data=None, bytes_data=None):
        obj = json.loads(text_data)  # 문자열에서 객체로 역직렬화
        print("수신 : ", obj)

        json_string = json.dumps(
            {  # 객체를 문자열로 직렬화
                "content": obj["content"],
                "user": obj["user"],
            }
        )
        self.send(json_string)
        # send api에서는 텍스트 혹은 바이너리 데이터만 전송가능하다.
        # 그래서 객체로 온 데이터를 직렬화해야 한다.


class LiveblogConsumer(WebsocketConsumer):
    # 메시지를 받을 그룹명
    groups = ["liveblog"]
    # 그룹을 통해 받은 메시지를 그대로 웹소켓 클라에게 전달. (self.send(전달매시지))
    # 메시지의 타입값과 같은 이름의 메서드가 호출된다.

    # ex) type "liveblog.post.created" => "liveblog_post_created" 마침표가 언더바로바뀜
    def liveblog_post_created(self, event_dict):
        self.send(json.dumps(event_dict))

    def liveblog_post_updated(self, event_dict):
        self.send(json.dumps(event_dict))

    def liveblog_post_deleted(self, event_dict):
        self.send(json.dumps(event_dict))
