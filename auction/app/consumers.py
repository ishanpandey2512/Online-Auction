from channels.consumer import AsyncConsumer
from .models import *
import asyncio
from channels.db import database_sync_to_async
import json


class LiveBiddingConsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        print("connected", event)
        self.product_id = self.scope['url_route']['kwargs']['p_id']

        await self.send({
            "type": "websocket.accept"
        })

        await self.channel_layer.group_add(
            self.product_id,
            self.channel_name
        )

    async def websocket_receive(self, event):
        print("receive",  event)
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            bid = loaded_dict_data.get('bid')
            user_obj = self.scope['user']
            p_id = self.product_id
            await self.update_bid(p_id, bid, user_obj)

            await self.channel_layer.group_send(
                self.product_id,
                {
                    'type': 'chat_message',
                    'text': bid
                }
            )

    async def websocket_disconnect(self, event):
        print("disconnected", event)

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    @database_sync_to_async
    def update_bid(self, p_id, bid, user_obj):
        product = Product.objects.get(id=p_id)
        if product.seller_id == user_obj:
            return None
        else:
            product.current_bid = bid
            product.bidder_id = user_obj
            product.save()
            return product
