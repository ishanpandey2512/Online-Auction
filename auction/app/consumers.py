from channels.consumer import AsyncConsumer
from .models import *
import asyncio
from channels.db import database_sync_to_async
import json


class LiveBiddingConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("receive",  event)

    async def websocket_disconnect(self, event):
        print("disconnected", event)

