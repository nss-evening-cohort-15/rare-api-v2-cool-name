from django.db import models

class Subscription(models.Model):

    created_on = models.DateField(null=True)
    ended_on = models.DateField(null=True)