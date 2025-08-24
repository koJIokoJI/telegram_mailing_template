import asyncio
import os
import sys

from nats.aio.client import Client
from nats.js.client import JetStreamContext
from nats.js.api import StreamConfig

from config.config import settings


async def main():
    nc = Client()
    await nc.connect(servers=settings.nats.servers)

    js: JetStreamContext = nc.jetstream()

    stream_name = settings.nats.stream

    config = StreamConfig(
        name=stream_name,
        subjects=[settings.nats.subject],
        retention="limits",
        storage="file",
    )

    await js.add_stream(config)

    print(f"Stream `{stream_name}` created")

    await nc.close()


if sys.platform.startswith("win") or os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
