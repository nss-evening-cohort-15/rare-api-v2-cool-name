import imp
from django.db import models

class Category(models.Model):

    label = models.CharField(
        max_length=20,
        null=True
    )