# Generated by Django 5.0.6 on 2024-06-16 09:27

import django_ckeditor_5.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0006_remove_article_content_article_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='text',
            field=django_ckeditor_5.fields.CKEditor5Field(default='', verbose_name='Text'),
        ),
    ]
