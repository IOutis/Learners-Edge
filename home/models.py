
# # models.py
# from django.db import models
# from django.contrib.auth.models import User

# class TimetableEntry(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='timetable_entries')
#     time_slot = models.TimeField()
#     date = models.DateField()
#     task_activity = models.CharField(max_length=255)
#     description = models.TextField(blank=True, null=True)
#     status = models.CharField(max_length=20, choices=[('Planned', 'Planned'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])
#     recurring = models.BooleanField(default=False)

#     def __str__(self):
#         return self.task_activity

#     class Meta:
#         db_table = 'timetable'

# from django.db import models
# from django.utils import timezone
