from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    title = models.CharField(max_length=20)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

class Reward(models.Model):
    name = models.CharField(max_length=100)
    announce_date = models.DateField()
    is_won = models.BooleanField(default=False)

class LuckyDraw(models.Model):
    name = models.CharField(max_length=100)
    timing = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    rewards = models.ManyToManyField(Reward)
    participants = models.ManyToManyField(Ticket)
    winners = models.ManyToManyField(User)

