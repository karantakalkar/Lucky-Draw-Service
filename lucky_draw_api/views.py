from django.shortcuts import render

from rest_framework import viewsets

from lucky_draw_api.serializers import TicketSerializer, RewardSerializer, LuckyDrawSerializer
from lucky_draw_api.models import Ticket, Reward, LuckyDraw

class TicketViewSet(viewsets.ModelViewSet):
   queryset = Ticket.objects.all()
   serializer_class = TicketSerializer

class RewardViewSet(viewsets.ModelViewSet):
   queryset = Ticket.objects.all()
   serializer_class = TicketSerializer

class LuckyDrawViewSet(viewsets.ModelViewSet):
  queryset = LuckyDraw.objects.all()
  serializer_class = LuckyDrawSerializer