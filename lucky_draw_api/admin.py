from django.contrib import admin

# Register your models here.
from .models import * 

admin.site.register(Ticket)
admin.site.register(Reward)
admin.site.register(LuckyDraw)
admin.site.register(Winner)