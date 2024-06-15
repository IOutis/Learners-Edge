from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Note(models.Model):
    title = models.CharField('Title', max_length=200, default="Untitled")
    text = CKEditor5Field('Content', config_name='extends', default='Your default content here.')  # Using CKEditor5Field for rich text editing



from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.conf import settings


class Article(models.Model):
    title = models.CharField('Title', max_length=200)
    text = CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notes',default=None)

