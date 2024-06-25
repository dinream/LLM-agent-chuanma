"""
channel factory
"""
from common import const
from .channel import Channel


def create_channel(channel_type) -> Channel:
    """
    create a channel instance
    :param channel_type: channel type code
    :return: channel instance
    """
    ch = Channel()
    if channel_type == "hlmj":
        from channel.hlmj.hlmj_channel import HLMJChannel
        ch = HLMJChannel()
    else:
        raise RuntimeError
    ch.channel_type = channel_type
    return ch
