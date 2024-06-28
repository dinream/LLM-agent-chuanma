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
from channel.chat_channel import ChatChannel
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
        self.isnew = False
        self.gameID = 0

    def newgame(self):
        self.gameID = self.gameID +1
        self.isnew = True
        self.curenv = {
            "GameID":0,
            "MyMahjong": {"l": [], "w": [], "o": []},
            "CurPlayer":1, 
            "CurTask": 1,
            }


        # time.sleep(2)

    def startup(self):
        context = Context()
        self.gameID = 0
        # process_handimages_in_threads( {"l": [], "w": [], "o": []})
        # config = self.curenv["MyMahjong"]
        # process_handimages_in_threads(config)
        # prompt =  json.dumps(self.curenv, indent=4)
        # print("-------------" +prompt)
        # self.process_reply({})
        # return 
        # 点击开始
        while True:
            while True:
                # 循环检测是否开了游戏
                #! 测试 api break 
                # prompt = self.get_input()
                # print(prompt)
                # return
                try:
                    ishlmj,matches = find_image_on_screen_reigion("image/start.png",(887, 132, 325, 46))
                    logger.info("Please open the game ...")
                    if ishlmj and len(matches)>0:
                        click(matches[0])
                        logger.info("Detecting the game successfully! Begin playing...")
                        break
                except KeyboardInterrupt:
                    print("\nExiting the game...")
                    sys.exit()
            lock = threading.Lock()  # 用于确保线程安全地访问共享资源
            threads = []
            for image_path in ["image/Over_ok.png","image/Begin.png","image/Next.png","image/winn.png","image/1Con.png"]:
                thread = threading.Thread(target=self.process_NewGame_image, args=(image_path, lock))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()

            if self.isnew:
                iffind = False
                matches = None
                while not iffind:
                    iffind, matches = find_image_on_screen_reigion("image/SelectType.png",(459, 791, 1251, 397))
                time.sleep(1)
            # 循环聊天
            msg_id = 0
            while True:
                # 获取输入
                msg_id += 1
                prompt = self.get_input()
                #! 测试api prompt =  json.dumps(self.curenv, indent=4)
                # print(prompt)
                reply= None
                reply_dict = None
                # 结合历史出牌信息和当前的出牌信息向大模型请求下一次出牌请求
                
                context = self._compose_context(ContextType.TEXT, prompt, msg=HLMJMessage(msg_id, prompt))
                if context:
                    reply = self._generate_reply(context)
                else:
                    raise Exception("context is None")
                if reply:
                    reply_dict =self._decode_content(reply.content)
                    self.process_reply(reply_dict)
                else:
                    raise Exception("reply's content is None")
                    break


    def process_reply(self, reply_dict):
        # #! 测试 识别
        # reply_dict = json.loads(read_file("./test.json"))
        # self.curenv["CurTask"] =1
        if reply_dict:
            if self.curenv["CurTask"] == 1: # 缺
                key = ""
                
                if "SelectType" in reply_dict:
                    key = reply_dict["SelectType"]
                else:
                    key = get_key_with_min_elements(self.curenv["MyMahjong"])
                if key != "":
                    istype, matches = find_image_on_screen_reigion("image/"+key+".png",(459, 791, 1251, 397))
                    if istype:  # 点击缺门
                        print("click image/"+key+".png")
                        click(matches[0])
            elif self.curenv["CurTask"] == 2: # 出
                path = ""
                if "SelectOne" in reply_dict:
                    key = find_first_non_empty_key(reply_dict["SelectOne"])
                    if key:
                        path = "image/"+key+"/"+str(reply_dict["SelectOne"][key][0])+".png"
                else:
                    key = find_first_non_empty_key(self.curenv["MyMahjong"])
                    if key:
                        path = "image/"+key+"/"+str(self.curenv["MyMahjong"][key][0])+".png"
                if path != "":
                    istype, matches = find_image_on_screen_reigion(path,(11, 1059, 2110, 310) )
                    if istype and len(matches)>0:  # 点击出牌
                        click(matches[0])
                        click(matches[0])
            elif self.curenv["CurTask"] == 3: # 碰
                tch = False
                if "Touch" in reply_dict:
                    tch = reply_dict["Touch"]
                if tch:
                    istype, matches = find_image_on_screen_reigion("image/Touch-ok.png",(1160, 911, 954, 291))
                    if istype:  # 点击开始游戏
                        click(matches[0])
                istype, matches = find_image_on_screen_reigion("image/Pass.png",(1160, 911, 954, 291))
                if istype:  # 点击开始游戏
                    click(matches[0])
        self.curenv["CurTask"] = 0


    def get_input(self):
        #  self.curenv["CurTask"] = 0
        self.curenv["MyMahjong"] = {"l": [], "w": [], "o": []}
        self.curenv["GameID"] = self.gameID
        # 判断是否是新开局
        while self.curenv["CurTask"] == 0:
            # 缺
            process_task_images_in_threads(self.curenv)
        config = self.curenv["MyMahjong"]
        #! 识别手牌
        process_handimages_in_threads(config)
        json_string = json.dumps(self.curenv, indent=4)
        return json_string
    
    def process_NewGame_image(self, image_path, lock):
        iffind, matches = find_image_on_screen_reigion(image_path,(10, 824, 2113, 480))
        if iffind:
            click(matches[0])
            with lock:
                self.newgame()
                

def get_key_with_min_elements(d):
    # 初始化一个变量来存储最小长度和对应的键
    min_key = None
    min_length = float('inf')

    # 遍历字典中的键和值
    for key, value in d.items():
        # 检查当前列表的长度是否比当前最小长度小
        if len(value) < min_length:
            min_length = len(value)
            min_key = key

    return min_key

def find_first_non_empty_key(d):
    # 遍历字典中的键和值
    for key, value in d.items():
        # 检查当前列表是否包含元素
        if len(value) > 0:
            return key
    # 如果所有的列表都是空的，返回 None 或者其他指示值
    return None

def read_file(path):
    with open(path, mode="r", encoding="utf-8") as f:
        return f.read()
    


