from unicodedata import category
from django.db import models
from .category import Category
from .reaction import Reaction

class Post(models.Model):

    title = models.CharField(
        max_length=50,
        default='none'
    )
    category = models.ForeignKey(
        Category,
        verbose_name="Category",
        null=True,
        on_delete=models.SET_NULL
    )
    reaction = models.ForeignKey(
        Reaction,
        related_name="post_reaction"
    )
    publication_date = models.DateTimeField()
    image_url = models.URLField(max_length=200)
    content = models.CharField(max_length=3000)
    approved = models.BinaryField()