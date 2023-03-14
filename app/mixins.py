from asgiref.sync import async_to_sync  # 비동기에서 동기로

from channels.layers import get_channel_layer

# 현재 Django Channels의 채널 레이어 인스턴스를 반환합니다.
# 채널 레이어는 비동기 작업을 처리하고,
# 클라이언트와 서버 간의 메시지를 처리하는데 사용됩니다.

from django.utils.functional import cached_property

# 속성을 계산하고 결과를 캐시하는 데 사용됩니다.
# 이 클래스를 사용하면 계산 비용이 많이 드는 속성을 미리 계산하여 캐시에 저장하고,
# 나중에 다시 속성을 요청할 때 저장된 값을 반환할 수 있습니다.
# 이를 통해 반복적인 계산을 피하고 성능을 향상시킬 수 있습니다.


class ChannelLayerGroupSendMixin:
    CHANNEL_LAYER_GROUP_NAME = None

    @cached_property
    def channel_layer(self):
        return get_channel_layer()

    def channel_layer_group_send(self, message_dict):
        async_to_sync(self.channel_layer.group_send)(
            self.CHANNEL_LAYER_GROUP_NAME,
            message_dict,
        )
