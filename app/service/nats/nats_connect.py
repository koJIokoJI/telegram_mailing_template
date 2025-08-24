from nats.aio.client import Client
from nats.js.client import JetStreamContext


async def connect_to_nats(servers: list[str]):
    nc = Client()
    await nc.connect(servers=servers)
    js: JetStreamContext = nc.jetstream()

    return nc, js
