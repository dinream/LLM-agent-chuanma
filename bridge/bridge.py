from bot.bot_factory import create_bot
from bridge.context import Context
from bridge.reply import Reply
from common import const
from common.log import logger
from common.singleton import singleton
from config import conf

@singleton
class Bridge(object):
    def __init__(self):
        self.btype = {
            "chat": const.CHATGPT, # 当前仅有唯一的 bot 机器人，无其他聊天
        }
        model_type = conf().get("model") or const.GPT35
        if model_type in ["openAI"]:
            self.btype["chat"] = const.OPEN_AI
        self.bots = {}
        self.chat_bots = {}

    def get_bot(self, typename):
        if self.bots.get(typename) is None:
            logger.info("create bot {} for {}".format(self.btype[typename], typename))
            if typename == "chat":
                self.bots[typename] = create_bot(self.btype[typename])
            # elif typename == "translate":
            #     self.bots[typename] = create_translator(self.btype[typename])
        return self.bots[typename]

    def get_bot_type(self, typename):
        return self.btype[typename]

    def fetch_reply_content(self, query, context: Context) -> Reply:
        return self.get_bot("chat").reply(query, context)


    def find_chat_bot(self, bot_type: str):
        if self.chat_bots.get(bot_type) is None:
            self.chat_bots[bot_type] = create_bot(bot_type)
        return self.chat_bots.get(bot_type)

    def reset_bot(self):
        """
        重置bot路由
        """
        self.__init__()
