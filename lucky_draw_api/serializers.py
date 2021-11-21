from rest_framework import serializers

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
        validated_data['password'] = make_password(validated_data['password'], salt='grofers')

        return User.objects.create(**validated_data)

class TicketSerializer(serializers.ModelSerializer):
    """
      Ticket Model Serializer
    """
    user = serializers.SlugRelatedField(many=True, read_only=True, slug_field='username')

    class Meta:
       model = Ticket
       fields = ('unique_code', 'user', 'is_used','id')
       read_only_fields = ('unique_code', 'is_used', 'used_at' 'id')

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
    rewards = RewardSerializer(many=True, read_only=True)
    reg_tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
       model = LuckyDraw
       fields = ('name', 'timing', 'is_active', 'rewards', 'reg_tickets', 'id')
       read_only_fields = ('id', 'reg_tickets', )

class WinnerSerializer(serializers.ModelSerializer):
    """
      Winner Model Serializer
    """
    user = UserSerializer(many = True, read_only=True)
    ticket = serializers.SlugRelatedField(many=True, read_only=True, slug_field='unique_code')
    reward = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    lucky_draw = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    
    class Meta:
       model = Winner
       fields = ('user', 'ticket', 'reward', 'lucky_draw', 'win_date', 'id')