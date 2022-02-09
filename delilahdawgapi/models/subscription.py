from tkinter import CASCADE
from django.db import models
from delilahdawgapi.models.rareuser import RareUser

class Subscription(models.Model):

    follower = models.ForeignKey(
        RareUser,
        null= True,
        related_name="following",
        on_delete=models.CASCADE)
    
    author = models.ForeignKey(
        RareUser,
        null=True,
        related_name="followed_by",
        on_delete=models.CASCADE)
    
    created_on = models.DateField(auto_now_add=True)
    ended_on = models.DateField(null=True)
    
    