from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from lucky_draw_api.models import *

class UserSerializer(serializers.ModelSerializer):
    """
      User Model Serializer
    """
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'id')
    
    # override default method to hash password
    def create(self, validated_data):
        unique_code = generate_code()
        validated_data['password'] = make_password(validated_data['password'])
        return User.objects.create(**validated_data)

class TicketSerializer(serializers.ModelSerializer):
    """
      Ticket Model Serializer
    """
    class Meta:
       model = Ticket
       fields = ('unique_code', 'user', 'is_used','id')
       read_only_fields = ('unique_code', 'is_used', 'id')

    # override default method to add unique_code to ticket
    def create(self, validated_data):
        unique_code = generate_code()
          
        return Ticket.objects.create(unique_code=unique_code, **validated_data)

class RewardSerializer(serializers.ModelSerializer):
    """
      Reward Model Serializer
    """
    class Meta:
       model = Reward
       fields = ('name', 'redeem_date', 'is_won')
       read_only_fields = ('is_won',)

class LuckyDrawSerializer(serializers.ModelSerializer):
    """
      Lucky Draw Model Serializer
    """
    class Meta:
       model = LuckyDraw
       fields = ('name', 'timing', 'is_active', 'rewards', 'reg_tickets', 'id')
       read_only_fields = ('id',)

class WinnerSerializer(serializers.ModelSerializer):
    """
      Winner Model Serializer
    """
    class Meta:
       model = Winner
       fields = ('name', 'ticket', 'reward', 'lucky_draw', 'win_date', 'id')