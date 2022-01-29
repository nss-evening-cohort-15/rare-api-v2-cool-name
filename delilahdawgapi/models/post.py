from django.db import models
from .category import Category
from .rareuser import RareUser

class Post(models.Model):

    rare_user = models.ForeignKey(
        RareUser,
        related_name="posts",
        null=True,
        on_delete=models.CASCADE
    )
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
    publication_date = models.DateTimeField()
    image_url = models.URLField(max_length=200)
    content = models.CharField(max_length=3000)
    approved = models.BooleanField(default=False)