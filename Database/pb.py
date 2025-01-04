from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.models.consumer.v3.channel import Channel

from config import config

pn_config = PNConfiguration()
pn_config.subscribe_key = config.get("PUBNUB_SUBSCRIBE_KEY")
pn_config.publish_key = config.get("PUBNUB_PUBLISH_KEY")
pn_config.secret_key = config.get("PUBNUB_SECRET_KEY")
pn_config.uuid = config.get("SIPIFY_USER_UUID")
pubnub = PubNub(pn_config)


def grant_token(auth_key):
    pubnub.set_token(auth_key)
    pubnub.subscribe().channels("Sipify-channel").execute()
    # print(f"GRANTING READ AND WRITE ACCESS {auth_key}")
    envelope = (
        pubnub.grant_token()
        .channels(
            [
                Channel.id("Sipify-channel").read(),
                Channel.id("Get-notification").read().write(),
            ]
        )
        .authorized_uuid(auth_key)
        .ttl(60)
        .sync()
    )
    print("ENVELOPE TOKEN: ", envelope.result.token)
    return envelope.result.token


def revoke_access(token):
    envelope = pubnub.revoke_token(token)


def parse_token_Sipify(token):
    token_details = pubnub.parse_token(token)
    print("Parsing the token")
    print(token_details)
    read_access = token_details["resources"]["channels"]["Sipify-channel"]["read"]
    uuid = token_details["authorized_uuid"]
    return (
        token_details["timestamp"],
        token_details["ttl"],
        uuid,
        read_access,
    )


def parse_token_Notification(token):
    token_details = pubnub.parse_token(token)
    print("Parsing the token")
    print(token_details)
    read_access = token_details["resources"]["channels"]["Get-notification"]["read"]
    write_access = token_details["resources"]["channels"]["Get-notification"]["write"]
    uuid = token_details["authorized_uuid"]
    return (
        token_details["timestamp"],
        token_details["ttl"],
        uuid,
        read_access,
        write_access,
    )
