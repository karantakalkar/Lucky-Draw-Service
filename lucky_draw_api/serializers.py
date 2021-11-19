from rest_framework import serializers

from lucky_draw_api.models import Ticket, Reward, LuckyDraw

class TicketSerializer(serializers.ModelSerializer):
   class Meta:
       model = Ticket
       fields = ('title', 'user', 'is_used')

class RewardSerializer(serializers.ModelSerializer):
   class Meta:
       model = Reward
       fields = ('name', 'announce_date', 'is_won')

class LuckDrawSerializer(serializers.ModelSerializer):
   class Meta:
       model = LuckyDraw
       fields = ('name', 'timing', 'is_active', 'rewards', 'participants', 'winners')