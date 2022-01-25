from django.db import models
from django.forms import URLField

class Reaction(models.Model):

    label = models.CharField(
        null=True,
        max_length=5
    )
    image_url = URLField(
        null=True,
        max_length=200
    )