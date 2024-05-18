import json
from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from channels.layers import get_channel_layer
from asgiref.sync import sync_to_async, async_to_sync
from datetime import *
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import mysql.connector
import logging
logger = logging.getLogger(__name__)
# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.TextField(max_length=100)
    is_seen = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        notification_objs = Notification.objects.filter(is_seen=False).count()
        data = {'count': notification_objs, 'current_notification': self.notification}
        print(f"Sending notification data: {data}")

        # try:
        #     async_to_sync(
        #         channel_layer.group_send)(
        #             str(self.user.username),
        #             {"type": "send_message", "text_data": json.dumps(data)}
        #     )
        #     print(f"Notification data sent to group: {str(self.user.username)}")
        # except Exception as e:
        #     print(f"Error sending notification data: {e}")
        channel_layer = get_channel_layer()
        async_to_sync (channel_layer.group_send)(
            "notification_"+str(self.user.username),
            {
                "type": "send_message",
                "text_data": json.dumps(data)
            }
        )
        print(f'save ended here')

        return super(Notification, self).save(*args, **kwargs)
    
    def task_deadline():
        connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="mmh13138",
                database="learners"
            )
        cursor = connection.cursor()
        
        return datetime.now() + timedelta(minutes=5)
    
    
