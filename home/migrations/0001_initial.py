# Generated by Django 5.0.2 on 2024-03-18 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimetableEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot', models.TimeField()),
                ('date', models.DateField()),
                ('task_activity', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Planned', 'Planned'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20)),
                ('recurring', models.BooleanField(default=False)),
            ],
        ),
    ]
