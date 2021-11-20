from django.db import models
from django.contrib.auth.models import User

def generate_code():
    import string, random
    return ''.join(random.choices(string.digits + string.ascii_uppercase, k=10))

class Ticket(models.Model):
    unique_code = models.CharField(max_length=10, blank = True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return self.unique_code

class Reward(models.Model):
    name = models.CharField(max_length=100)
    announce_date = models.DateField()
    is_won = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class LuckyDraw(models.Model):
    name = models.CharField(max_length=100)
    timing = models.DateField()
    is_active = models.BooleanField(default=True)
    rewards = models.ManyToManyField(Reward)
    participants = models.ManyToManyField(Ticket)

    def __str__(self):
        return self.name

class Winner(models.Model):
    name = models.CharField(max_length=100)
    ticket = models.ForeignKey(Ticket , on_delete=models.SET_NULL , null=True , blank=True)
    reward = models.ForeignKey(Reward , on_delete=models.SET_NULL , null=True , blank=True)
    lucky_draw = models.ForeignKey(LuckyDraw , on_delete=models.SET_NULL , null=True , blank=True)    

    def __str__(self):
        return self.name


