# Generated by Django 5.0.6 on 2024-06-16 09:38

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0009_remove_article_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, null=True, verbose_name='Text'),
        ),
    ]
