from contextlib import asynccontextmanager

from faststream import FastStream, Logger, BaseMiddleware
from faststream.nats import NatsBroker


class Mid(BaseMiddleware):
    @asynccontextmanager
    async def publish_scope(self, msg):
        yield msg + 1


broker = NatsBroker(middlewares=(Mid,))
app = FastStream(broker)

@broker.subscriber("in")
async def handler(msg, logger: Logger):
    logger.info(msg)
    return msg

@broker.subscriber("out")
async def handler2(msg, logger: Logger):
    logger.info(msg)

@app.after_startup
async def t():
    print(await broker.publish(1, "in", rpc=True))
    # await broker.publish(2, "in")
