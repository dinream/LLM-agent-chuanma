
import signal
import sys

import time 
import threading


from config import conf
from config import load_config
from channel import channel_factory 
from common.log import logger
from common import const

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
    target_image_path = 'image/invite1.png'  # 替换为目标图像的路径
    # 点击开始
    
    # 初始化状态
        # 剩余玩家
        # 已经出牌
        # 玩家手牌情况
# TODO 别人出牌
    # 局内游戏
    while True:
        print("a") 
        # 识别手牌
        # 转换为文字信息
        # 将每一次的手牌
        # 对每一次别人出牌
        # # 判别自己是否可以杠牌或者胡牌
        # 对自己的出牌
        # 结合历史出牌信息和当前的出牌信息向大模型请求下一次出牌请求
        # 将出牌请求转换为鼠标动作
        # 验证最终出牌动作
        break