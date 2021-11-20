from rest_framework import serializers

from lucky_draw_api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')

class TicketSerializer(serializers.ModelSerializer):
   class Meta:
       model = Ticket
       fields = ('unique_code', 'user', 'is_used')
       read_only_fields = ('unique_code', 'is_used')

   def create(self, validated_data):
      unique_code = generate_code()
        
      return Ticket.objects.create(unique_code=unique_code, **validated_data)

class RewardSerializer(serializers.ModelSerializer):
   class Meta:
       model = Reward
       fields = ('name', 'announce_date', 'is_won')
       read_only_fields = ('is_won')

class LuckyDrawSerializer(serializers.ModelSerializer):
   class Meta:
       model = LuckyDraw
       fields = ('name', 'timing', 'is_active', 'rewards', 'participants', 'winner')
       read_only_fields = ('winner')