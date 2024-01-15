import asyncio
import random
from pyrogram.types import Message

from .base import Monitor
from ...utils import async_partial

__ignore__ = True


class JudogMonitor(Monitor):
    name = "剧狗"
    chat_name = "Mulgoreemby"
    chat_keyword = r"剩余可注册人数：\d+"
    bot_username = "mulgorebot"
    notify_create_name = True

    async def init(self):
        channel = await self.client.get_chat("Mulgoreemby")
        self.chat_name = channel.linked_chat.id
        self.log.info(f"已读取剧狗频道关联群: {channel.linked_chat.title}")
        return True

    async def on_trigger(self, message: Message, key, reply):
        wr = async_partial(self.client.wait_reply, self.bot_username)
        msg: Message = await wr("/start")
        if "选择您要使用的功能" in (msg.caption or msg.text):
            await asyncio.sleep(random.uniform(2, 4))
            msg = await wr("🔱账号")
        if "账号管理中心" in (msg.caption or msg.text):
            await asyncio.sleep(random.uniform(2, 4))
            msg = await wr("💡注册")
        if "目前已无可注册资格" in (msg.caption or msg.text):
            return
        else:
            self.log.bind(notify=True).info(f"已在{self.name}抢注成功, 请及时登录查看.")
