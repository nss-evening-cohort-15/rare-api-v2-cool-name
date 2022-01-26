from django.db import models
from delilahdawgapi.models.rareuser import RareUser
from .post import Post


class Reaction(models.Model):

    label = models.CharField(
        null=True,
        max_length=5
    )
    image_url = models.URLField(
        null=True,
        max_length=200
    )
    user = models.ForeignKey(
        RareUser,
        related_name="user_reaction",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name="post_reaction",
        on_delete=models.CASCADE
        
    )