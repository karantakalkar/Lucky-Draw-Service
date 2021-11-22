from django.db import models
from django.contrib.auth.models import User

def generate_code():
    """
      Function to generate unique_code for Ticket model.
    """
    import string, random
    return ''.join(random.choices(string.digits + string.ascii_uppercase, k=10))

class Ticket(models.Model):
    """
      Ticket Model
    """
    unique_code = models.CharField(max_length=10, blank = True)
    is_used = models.BooleanField(default=False)
    user = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.unique_code

class Reward(models.Model):
    """
      Reward Model
    """
    name = models.CharField(max_length=100)
    redeem_date = models.DateField()
    is_won = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class LuckyDraw(models.Model):
    """
      Lucky Draw Model
    """
    name = models.CharField(max_length=100)
    timing = models.TimeField()
    is_active = models.BooleanField(default=True)
    rewards = models.ManyToManyField(Reward, blank = True)
    reg_tickets = models.ManyToManyField(Ticket, blank = True)

    def __str__(self):
        return self.name

class Winner(models.Model):
    """
      Winner Model
    """
    user = models.ForeignKey(User , on_delete=models.CASCADE, null=True , blank=True)
    ticket = models.ForeignKey(Ticket , on_delete=models.SET_NULL , null=True , blank=True)
    reward = models.ForeignKey(Reward , on_delete=models.SET_NULL , null=True , blank=True)
    lucky_draw = models.ForeignKey(LuckyDraw , on_delete=models.SET_NULL , null=True , blank=True)
    win_date =  models.DateField(null=True, blank = True)

    def __str__(self):
        return self.user.username


