# encoding:utf-8

"""
wechat channel
"""


import time
import sys
import json

from bridge.context import *
from bridge.reply import *
from channel.chat_channel import ChatChannel, check_prefix
from channel import chat_channel
from channel.hlmj.hlmj_message import *
from common.expired_dict import ExpiredDict
from common.log import logger
from common.singleton import singleton
from common.time_check import time_checker
from config import conf, get_appdata_dir

from interface_win.imgIdtfy import *

@singleton
class HLMJChannel(ChatChannel):
    NOT_SUPPORT_REPLYTYPE = []

    def __init__(self):
        super().__init__()
        self.receivedMsgs = ExpiredDict(60 * 60)
        self.auto_login_times = 0
        self.left = [4,4,4,4,4,4,4,4,4,
                        4,4,4,4,4,4,4,4,4,
                        4,4,4,4,4,4,4,4,4
                    ]
        self.curenv = {
            "MyMahjong": {"l": [], "w": [], "o": []}, # "l" 表示"杠"门牌; "w" 表示"万"门牌；"o" 表示"筒"门牌：元素 1-9 表示牌的大小
            "CurPlayer":1, # 表示当前是哪一个玩家的出牌环节。 1：本家；2：下家； 3:对家；4:上家
            "CurTask":0, # 0:非操作环节 1 ：选则缺门； 2：选择出牌： 3：是否碰牌
            }

    def startup(self):
        context = Context()
        msg_id = 0
        # 点击开始
        
            # 剩余玩家
            # 已经出牌
            # 玩家手牌情况
        # 开始循环
        while True:
            try:
                while True:
                    ishlmj,_ = find_image_on_screen("image/start.png")
                    logger.info("Detecting the game ...")
                    if ishlmj:
                        logger.info("Detecting the game successfully! Begin playing...")
                        break
                    # time.sleep(1)
                # 初始化状态
                prompt = self.get_input()
                print(prompt)
            except KeyboardInterrupt:
                print("\nExiting...")
                sys.exit()
                # 点击开始

                # 初始化状态
                    # 剩余玩家
                    # 已经出牌
                    # 玩家手牌情况
                # 开始循环

            # 识别手牌
            # 转换为文字信息
            # 将每一次的手牌
            # 对每一次别人出牌
            # # 判别自己是否可以杠牌或者胡牌
            # 对自己的出牌
            # 结合历史出牌信息和当前的出牌信息向大模型请求下一次出牌请求
            # 将出牌请求转换为鼠标动作
            # 验证最终出牌动作
            msg_id += 1
            trigger_prefixs = conf().get("single_chat_prefix", [""])
            if check_prefix(prompt, trigger_prefixs) is None:
                prompt = trigger_prefixs[0] + prompt  # 给没触发的消息加上触发前缀

            context = self._compose_context(ContextType.TEXT, prompt, msg=HLMJMessage(msg_id, prompt))
            if context:
                self.produce(context)
            else:
                raise Exception("context is None")

    # 统一的发送函数，每个Channel自行实现，根据reply的type字段发送不同类型的消息
    def send(self, reply: Reply, context: Context):
        print('test')

    def get_input(self):
        """
        Multi-line input function
        """
        
        config = self.curenv["MyMahjong"]
        #! 识别手牌
        # 处理 image/l 文件夹
        process_images("image/l", "l", config)

        # 处理 image/w 文件夹
        process_images("image/w", "w", config)

        # 处理 image/o 文件夹
        process_images("image/o", "o", config)
        
        #! 识别任务
        istype,_ = find_image_on_screen("image/SelectType.png")
        if istype:
            self.curenv["CurTask"] = 1

        istype,_ = find_image_on_screen("image/Touch.png")
        if istype:
            self.curenv["CurTask"] = 3
        #! 识别玩家
        istype,_ = find_image_on_screen("image/Player.png")
        if istype:
            self.curenv["CurTask"] = 2
            self.curenv["CurPlayer"] = 1

        sys.stdout.flush()
        json_string = json.dumps(self.curenv, indent=4)
        return json_string