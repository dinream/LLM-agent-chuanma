# encoding:utf-8

"""
wechat channel
"""


import threading
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
            "GameID":0,
            "MyMahjong": {"l": [], "w": [], "o": []}, # "l" 表示"杠"门牌; "w" 表示"万"门牌；"o" 表示"筒"门牌：元素 1-9 表示牌的大小
            "CurPlayer":1, # 表示当前是哪一个玩家的出牌环节。 1：本家；2：下家； 3:对家；4:上家
            "CurTask":0, # 0:非操作环节 1 ：选则缺门； 2：选择出牌： 3：是否碰牌
            }
        self.gameID = 0

    def newgame(self):
        self.gameID = self.gameID +1
        self.curenv = {
            "GameID":0,
            "MyMahjong": {"l": [], "w": [], "o": []},
            "CurPlayer":1, 
            "CurTask":0,
            }
        time.sleep(2)


    def startup(self):
        context = Context()
        self.gameID = 0
        # 点击开始
        while True:
            while True:
                # 循环检测是否开了游戏
                try:
                    ishlmj,_ = find_image_on_screen("image/start.png")
                    logger.info("Please open the game ...")
                    if ishlmj:
                        logger.info("Detecting the game successfully! Begin playing...")
                        # game_thread = threading.Thread(target=self.game_thread)
                        # game_thread.start()
                        break
                except KeyboardInterrupt:
                    print("\nExiting the game...")
                    sys.exit()

            # 循环聊天
            msg_id = 0
            while True:
                # 获取输入
                prompt = self.get_input()
                msg_id += 1
                print(prompt)
                # 结合历史出牌信息和当前的出牌信息向大模型请求下一次出牌请求
                context = self._compose_context(ContextType.TEXT, prompt, msg=HLMJMessage(msg_id, prompt))
                if context:
                    self.produce(context)
                else:
                    raise Exception("context is None")
            
            # 将出牌请求转换为鼠标动作
            # 验证最终出牌动作
    # 统一的发送函数，每个Channel自行实现，根据reply的type字段发送不同类型的消息
    def send(self, reply: Reply, context: Context):
        print('test')

    def get_input(self):
        """
        Multi-line input function
        """
    
        self.curenv["CurTask"] = 0
        # 判断是否是新开局
        while True:
            #! 识别任务
            while True:
                #! 新游戏
                # 开始游戏
                istype, matches = find_image_on_screen("image/Begin.png")
                if istype:  # 点击开始游戏
                    click(matches[0])
                    # print(matches[0])
                    self.newgame()
                    break
                # 下一局
                istype, matches = find_image_on_screen("image/Next.png")
                if istype:  # 点击换对手
                    click(matches[0])
                    self.newgame()
                    break
                # 换对手
                istype, matches = find_image_on_screen("image/Win.png")
                if istype:  # 点击换对手
                    click(matches[0], 0, 25)
                    self.newgame()
                    break
                # 继续游戏
                istype, matches = find_image_on_screen("image/1Con.png")
                if istype:  # 点击换对手
                    click(matches[0])
                    self.newgame()
                    break
            # 缺
            istype,_ = find_image_on_screen("image/SelectType.png")
            if istype:
                self.curenv["CurTask"] = 1
                break
            # 碰 
            istype,_ = find_image_on_screen("image/Touch.png")
            if istype:
                self.curenv["CurTask"] = 3
                break
            # 出
            istype,_ = find_image_on_screen("image/Player.png")
            if istype:
                self.curenv["CurTask"] = 2
                self.curenv["CurPlayer"] = 1
                break
            
        config = self.curenv["MyMahjong"]
        #! 识别手牌
        # 处理 image/l 文件夹
        process_images("image/l", "l", config)

        # 处理 image/w 文件夹
        process_images("image/w", "w", config)

        # 处理 image/o 文件夹
        process_images("image/o", "o", config)
        self.curenv["GameID"] = self.gameID
        json_string = json.dumps(self.curenv, indent=4)
        return json_string
    



    def game_thread(self):
        # 判断是否是新开局
        while True:
            #! 新游戏
            istype, matches = find_image_on_screen("image/Win.png")
            if istype:  # 点击换对手
                click(matches[0], 0, 25)
                self.newgame()
            istype, matches = find_image_on_screen("image/Next.png")
            if istype:  # 点击下一局
                click(matches[0])
                self.newgame()
            istype, matches = find_image_on_screen("image/Begin.png")
            if istype:  # 点击开始游戏
                click(matches[0])
                self.newgame()
            
            time.sleep(3)