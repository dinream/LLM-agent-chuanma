
import signal
import sys

import time 
import threading

import pyautogui


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

def get_mouse_position():
    print("请移动鼠标到矩形区域的左上角，然后按下 'Enter'")
    input()  # 等待用户按下 Enter
    x1, y1 = pyautogui.position()
    print(f"左上角坐标: ({x1}, {y1})")

    print("请移动鼠标到矩形区域的右下角，然后按下 'Enter'")
    input()  # 等待用户按下 Enter
    x2, y2 = pyautogui.position()
    print(f"右下角坐标: ({x2}, {y2})")

    width = x2 - x1
    height = y2 - y1

    print(f"指定区域的范围: ({x1}, {y1}, {width}, {height})")


# (11, 1059, 2110, 310)  手牌
# 玩家阶段 (840, 593, 469, 234)
# 杠牌区域 (1160, 911, 954, 291)
# hlmj (887, 132, 325, 46)
# 新游戏(183, 436, 1696, 919)
# 缺 (572, 856, 964, 302)
def run():
    # get_mouse_position()
    # return 
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