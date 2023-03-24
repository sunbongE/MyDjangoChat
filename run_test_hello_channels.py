import asyncio
import os
import django
from channels.layers import get_channel_layer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()


async def main():
    channel_layer = get_channel_layer()
    message_dict = {"content": "world"}
    # 'hello' 채널에 메세지를 보내고,
    await channel_layer.send("hello", message_dict)
    # 'hello' 채널로부터 메세지를 읽습니다.
    response_dict = await channel_layer.receive("hello")
    is_equal = message_dict == response_dict
    print("송신/수신 데이터가 같습니까?", is_equal)


asyncio.run(main())

# board = []
# for _ in range(19):
#     board.append([" "] * 10)

# for i in range(0, 19, 3):
#     board[i] = ["X"] * 10

# for i in [1, 2, 13, 14]:
#     board[i][-1:-3] = ["X", "X"]

# for i in [4, 5, 16, 17]:
#     board[i][0:2] = ["X", "X"]

# for i in [7, 8]:
#     board[i][4:6] = ["X", "X"]

# for i in range(19):
#     for j in range(10):
#         print(board[i][j], end="")
#     print()
