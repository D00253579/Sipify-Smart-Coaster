from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.models.consumer.v3.channel import Channel
from pubnub.models.consumer.v3.group import Group
from pubnub.models.consumer.v3.uuid import UUID
import config

pn_config = PNConfiguration()
pn_config.subscribe_key = config.get("PUBNUB_SUBSCRIBE_KEY")
pn_config.publish_key = config.get("PUBNUB_PUBLISH_KEY")
pn_config.secret_key = config.get("PUBNUB_SECRET_KEY")
pn_config.user_id = "my_unique_user_id"
pubnub = PubNub(pn_config)

channels = [
    Channel.id("Sipify-channel").read().write(),
    Channel.id("Get-notification").read().write(),
]
