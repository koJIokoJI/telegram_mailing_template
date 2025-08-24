import logging

from aiogram import Bot

from nats.aio.client import Client
from nats.js.client import JetStreamContext

from app.service.nats.mail_service.consumer import MailingMessageConsumer


logger = logging.getLogger(__name__)


async def start_consumer(
    nc: Client,
    js: JetStreamContext,
    bot: Bot,
    subject: str,
    stream: str,
    durable_name: str,
):
    consumer = MailingMessageConsumer(
        nc=nc, js=js, bot=bot, subject=subject, stream=stream, durable_name=durable_name
    )
    logger.info("Start consumer")
    await consumer.subscribe()
