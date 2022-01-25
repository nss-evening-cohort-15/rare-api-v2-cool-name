from pyexpat import model
from django.db import models
from .post import Post
from .rareuser import RareUser

class Comment(models.Model):

    content = models.CharField(
        max_length=3000,
        default="I forgot to write a comment",
        on_delete=models.CASCADE
    )       
    created_on = models.DateTimeField()
    post = models.ForeignKey(
        Post,
        related_name='post_comment',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        RareUser,
        related_name='commenter'
    )