from django.shortcuts import render

from rest_framework import viewsets

from .models import *

from lucky_draw_api.serializers import UserSerializer, TicketSerializer, RewardSerializer, LuckyDrawSerializer
from lucky_draw_api.models import Ticket, Reward, LuckyDraw

class UserViewSet(viewsets.ModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer 

class TicketViewSet(viewsets.ModelViewSet):
   queryset = Ticket.objects.all()
   serializer_class = TicketSerializer 

class RewardViewSet(viewsets.ModelViewSet):
   queryset = Reward.objects.all()
   serializer_class = RewardSerializer

class LuckyDrawViewSet(viewsets.ModelViewSet):
  queryset = LuckyDraw.objects.all()
  serializer_class = LuckyDrawSerializer