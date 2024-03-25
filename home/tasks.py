from __future__ import absolute_import, unicode_literals
from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Task
from django.utils import timezone

@shared_task
def check_due_tasks():
    channel_layer = get_channel_layer()
    for task in Task.objects.filter(due_date__lte=timezone.now()):
        async_to_sync(channel_layer.group_send)(
            "notification_group", {"type": "notification.message", "message": f"Task {task.id} is due!"}
        )
