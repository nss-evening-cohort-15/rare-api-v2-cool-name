from django.db import models
from delilahdawgapi.models.rareuser import RareUser
from delilahdawgapi.models.reaction import Reaction
from delilahdawgapi.models.post import Post

class PostReaction(models.Model):

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
    reaction = models.ForeignKey(
        Reaction,
        related_name="post_reactions",
        on_delete=models.CASCADE
    )