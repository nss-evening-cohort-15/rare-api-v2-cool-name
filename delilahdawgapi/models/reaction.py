from django.db import models

class Reaction(models.Model):

    label = models.CharField(
        null=True,
        max_length=5
    )
    image_url = models.URLField(
        null=True,
        max_length=200
    )