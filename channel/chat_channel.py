import os
import re
import threading
import json
from asyncio import CancelledError
from concurrent.futures import Future, ThreadPoolExecutor
from concurrent import futures

from bridge.context import *
from bridge.reply import *
from channel.channel import Channel
from common.dequeue import Dequeue
from common import memory
from common import *
from common.log import logger
from config import conf
handler_pool = ThreadPoolExecutor(max_workers=8)  # 处理消息的线程池


# 抽象类, 它包含了与消息通道无关的通用处理逻辑
class ChatChannel(Channel):
    name = None  # 登录的用户名
    user_id = None  # 登录的用户id
    futures = {}  # 记录每个session_id提交到线程池的future对象, 用于重置会话时把没执行的future取消掉，正在执行的不会被取消
    sessions = {}  # 用于控制并发，每个session_id同时只能有一个context在处理
    lock = threading.Lock()  # 用于控制对sessions的访问



    # 根据消息构造context，消息内容相关的触发项写在这里
    def _compose_context(self, ctype: ContextType, content, **kwargs):
        context = Context(ctype, content)
        context.kwargs = kwargs
        context["session_id"] = 1
        if "origin_ctype" not in context:
            context["origin_ctype"] = ctype
        #context["openai_api_key"] = user_data.get("openai_api_key")
        # context["gpt_model"] = "gpt-3.5-turbo"
        return context


    def _generate_reply(self, context: Context, reply: Reply = Reply()) -> Reply:
        reply = super().build_reply_content(context.content, context)
        return reply
    
    def _decode_content(self,content) -> dict:
        # 去除 Markdown 代码块标记
        json_str = content.replace('```json\n', '').replace('```', '').strip()
        print(json_str)
        print(type(json_str))

        content_dict = {}
        # 将 JSON 字符串解析为字典
        try:
            content_dict = json.loads(json_str)
            print(content_dict)
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")

        # 打印解析结果
        # print(content_dict)
        return content_dict
