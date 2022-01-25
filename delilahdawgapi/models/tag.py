from tkinter import CASCADE
from django.db import models
from django.forms import CharField
from .post import Post

class Tag(models.Model):

    label = models.CharField(
        max_length=20,
        null=True  
    )
    post = models.ForeignKey(
        null=True,
        related_name="post_tag",
        on_delete=models.CASCADE
    )