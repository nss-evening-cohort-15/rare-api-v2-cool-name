from django.db import models
from .rareuser import RareUser
from .reaction import Reaction
from .post import Post

class PostReaction(models.Model):

    user = models.ForeignKey(
        RareUser,
        related_name="user_reactions",
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        related_name="post_reactions",
        on_delete=models.CASCADE
    )
    reaction = models.ForeignKey(
        Reaction,
        related_name="post_reactions",
        on_delete=models.CASCADE
    )