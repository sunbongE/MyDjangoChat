import asyncio
import os
import django
from channels.layers import get_channel_layer
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
async def main():
 channel_layer = get_channel_layer()
 message_dict = {'content': 'world'}
 # 'hello' 채널에 메세지를 보내고,
 await channel_layer.send('hello', message_dict)
 # 'hello' 채널로부터 메세지를 읽습니다.
 response_dict = await channel_layer.receive('hello')
 is_equal = message_dict == response_dict
 print("송신/수신 데이터가 같습니까?", is_equal)
asyncio.run(main())