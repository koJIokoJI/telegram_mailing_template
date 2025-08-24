import logging

from aiogram import Bot

from nats.aio.client import Client
from nats.aio.msg import Msg
from nats.js import JetStreamContext


logger = logging.getLogger(__name__)


class MailingMessageConsumer:
    def __init__(
        self,
        nc: Client,
        js: JetStreamContext,
        bot: Bot,
        subject: str,
        stream: str,
        durable_name: str,
    ):
        self.nc = nc
        self.js = js
        self.bot = bot
        self.subject = subject
        self.stream = stream
        self.durable_name = durable_name

    async def subscribe(self):
        self.stream_sub = await self.js.subscribe(
            subject=self.subject,
            stream=self.stream,
            cb=self.on_message,
            durable=self.durable_name,
            manual_ack=True,
        )

    # TODO: chat_ids из базы данных; возможно передавать данные уже в нужном формате; если по ошибке в стриме есть сообщения, то после исправления ошибки они тоже будут отправлены
    async def on_message(self, msg: Msg):
        if msg.headers.get("Chat-Ids"):
            chat_ids = list(map(int, msg.headers.get("Chat-Ids").split()))
            photo_id = msg.headers.get("Photo-Id")
            text = msg.data.decode(encoding="utf-8")
            if photo_id:
                for i in chat_ids:
                    await self.bot.send_photo(
                        chat_id=i,
                        photo=photo_id,
                        caption=text,
                    )
                    logger.info(
                        f"Message: '{text}' with photo id: '{photo_id}' sent to chat: '{i}'"
                    )
            else:
                for i in chat_ids:
                    await self.bot.send_message(chat_id=i, text=text)
                    logger.info(
                        f"Message: '{text}' with photo id: '{photo_id}' sent to chat: '{i}'"
                    )
            await msg.ack()

    async def ubsubscribe(self):
        await self.stream_sub.unsubscribe()
        logger.info("Consumer unsibscribed")
