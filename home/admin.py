from django.contrib import admin

# Register your models here.
from django.contrib import admin
from notifications_app.models import Notification
from notes.models import Note
# Register your models here.
admin.site.register(Notification)
admin.site.register(Note)