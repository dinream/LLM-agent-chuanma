
import signal
import sys

import time 
import threading


from config import conf
from config import load_config
from channel import channel_factory 
from common.log import logger
from common import const
from channel.chat_channel import ChatChannel
def sigterm_handler_wrap(_signo):
    old_handler = signal.getsignal(_signo)

    def func(_signo, _stack_frame):
        logger.info("signal {} received, exiting...".format(_signo))
        conf().save_user_datas()
        if callable(old_handler):  #  check old_handler
            return old_handler(_signo, _stack_frame)
        sys.exit(0)

    signal.signal(_signo, func)


def start_channel(channel_name: str):
    channel = channel_factory.create_channel(channel_name)
    channel.startup()




def run():
    try:
        logger.info("begin {} game, running...".format('1'))
        # ctrl + c
        sigterm_handler_wrap(signal.SIGINT)
        # kill signal
        sigterm_handler_wrap(signal.SIGTERM)
        # 加载配置文件
        load_config()
        # create channel
        channel_name = conf().get("channel_type", "hlmj")

        if "--cmd" in sys.argv:
            channel_name = "terminal"

        start_channel(channel_name)

        while True:
            time.sleep(1)
            print('a')

    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)

if __name__ == "__main__":
    run()
#     ch = ChatChannel()
#     content = "```json\n{\n    \"Touch\": false,\n    \"SelectType\": \"o\",\n    \"SelectOne\": {\"l\": [], \"w\": [], \"o\": []}\n}\n```"
#     dic = ch._decode_content(content)
#     
#     new_cont = """
# {
#     \"Touch\": false,
#     \"SelectType\": \"o\",
#     \"SelectOne\": {\"l\": [], \"w\": [], \"o\": []} 
    
# }
# """
#     dic = ch._decode_content(new_cont)

    # 初始化状态
        # 剩余玩家
        # 已经出牌
        # 玩家手牌情况