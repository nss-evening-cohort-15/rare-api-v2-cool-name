from django.db import models
from .post import Post

class Tag(models.Model):

    label = models.CharField(
        max_length=20,
        null=True  
    )
    post = models.ForeignKey(
        Post,
        null=True,
        related_name="post_tag",
        on_delete=models.CASCADE
    )