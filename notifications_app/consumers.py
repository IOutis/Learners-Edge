import json
from channels.generic.websocket import AsyncWebsocketConsumer,AsyncJsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import logging
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
logger = logging.getLogger(__name__)

from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.channel_layer = get_channel_layer()
            # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            # self.room_group_name = f"notification_{self.room_name}"
            
            user_id = self.scope['url_route']['kwargs']['user_id']
            # Join room group
            # async_to_sync(self.channel_layer.group_add, self.room_group_name, self.room_name)
            # await self.accept()
            # await async_to_sync(self.channel_layer.group_add)(
            #     self.room_group_name, self.channel_name
            #     )
            # self.accept()
            # self.send(text_data=json.dumps({'status':'connected'}))
            user = await sync_to_async(User.objects.get)(username=user_id)
            if user.is_authenticated:
                self.room_group_name = f"notification_{user_id}"
                await self.channel_layer.group_add(self.room_group_name, self.channel_name)
                
                # Accept the connection
                await self.accept()
                await self.send(text_data=json.dumps({'status': 'connected'}))
                print(f"Adding user to group: {self.room_group_name}")
            else:
                await self.close()

        except KeyError as e:
            logger.error(f"KeyError: {e}")
            await self.close()
    async def disconnect(self, close_code):
        pass
        # Leave room group
        # await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
    # Log the received text_data for debugging
        pass
        # print(f"Received text_data: {text_data}")
        # await (self.channel_layer.group_send)(
        #             self.room_group_name, {"type": "send_message", "message":text_data}
        # )
        # Check if text_data is not empty and is a valid JSON string
        # if text_data and text_data.strip():
        #     try:
        #         text_data_json = json.loads(text_data)
        #         message = text_data_json["message"]

        #         # Send message to room group
        #         await async_to_sync(self.channel_layer.group_send)(
        #             self.room_group_name, {"type": "send_message", "message":"Hello"}
        #         )
        #     except json.JSONDecodeError as e:
        #         # Log JSONDecodeError for debugging
        #         logger.error(f"JSONDecodeError: {e}")
        #         # Optionally, send a message back to the client indicating the error
        #         await self.send(text_data=json.dumps({'status': 'error', 'message': 'Invalid JSON'}))
        # else:
        #     # Optionally, send a message back to the client indicating an empty message was received
        #     await self.send(text_data=json.dumps({'status': 'error', 'message': 'Empty message received'}))

    # Receive message from room group
    async def send_message(self, event):
        print('send_message called')
        print(event)
        data = json.loads(event.get('text_data'))
        # data = data.get('current_notification')
        if data:
            print('Data:', data['New'])
            print('Data:', type(data))
            await self.send(text_data=json.dumps({'payload':data['New']}))
        else:
            print('No data in event')


class Newconsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['url_route']['kwargs']['username']
        self.room_name = 'notification_'+self.user
        self.room_group_name = 'notification_'+self.user
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
            )
        await self.accept()
    