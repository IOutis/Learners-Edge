
# models.py
from django.db import models

class TimetableEntry(models.Model):
    time_slot = models.TimeField()
    date = models.DateField()
    task_activity = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('Planned', 'Planned'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
    recurring = models.BooleanField(default=False)

    def __str__(self):
        return self.task_activity
    class Meta:
        db_table = 'timetable'

from django.db import models
from django.utils import timezone

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateTimeField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
