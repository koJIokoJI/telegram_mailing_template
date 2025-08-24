import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram_dialog import setup_dialogs

from redis.asyncio import Redis

from config.config import settings
from app.bot.handlers import commands_router
from app.bot.dialogs import dialog
from app.service.nats import connect_to_nats
from app.service.nats.mail_service import start_consumer


logger = logging.getLogger(__name__)


async def main():
    nc, js = await connect_to_nats(servers=settings.nats_servers)

    redis = Redis(
        host=settings.redis_host, port=settings.redis_port, db=settings.redis_db
    )
    storage = RedisStorage(
        redis=redis, key_builder=DefaultKeyBuilder(with_destiny=True, separator=".")
    )

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher(storage=storage)

    dp.include_routers(commands_router, dialog)
    setup_dialogs(dp)

    try:
        await asyncio.gather(
            dp.start_polling(
                bot,
                js=js,
            ),
            start_consumer(
                nc=nc,
                js=js,
                bot=bot,
                subject=settings.nats.subject,
                stream=settings.nats.stream,
                durable_name=settings.nats.durable_name,
            ),
        )
    except Exception as e:
        logger.exception(e)
    finally:
        await nc.close()
        logger.info("Connection to NATS closed")
        await redis.close()
        logger.info("Connection to Redis closed")
