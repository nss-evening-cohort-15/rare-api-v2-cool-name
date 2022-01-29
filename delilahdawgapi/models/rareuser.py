from django.db import models
from django.contrib.auth.models import User

class RareUser(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(
        max_length=150,
        default="I have not created a bio yet"
    )
    profile_image_url = models.URLField(
        null=True,
        max_length=500
    )
    created_on = models.DateField(null=True)
    active = models.BooleanField(
        default=True
    )