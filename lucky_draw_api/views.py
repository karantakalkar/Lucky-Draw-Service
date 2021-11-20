from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *

import random

from lucky_draw_api.serializers import UserSerializer, TicketSerializer, RewardSerializer, LuckyDrawSerializer, WinnerSerializer
from lucky_draw_api.models import Ticket, Reward, LuckyDraw, Winner

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
  queryset = LuckyDraw.objects.filter(is_active = True)
  serializer_class = LuckyDrawSerializer

class WinnerViewSet(viewsets.ModelViewSet):
  queryset = Winner.objects.all()
  serializer_class = WinnerSerializer

class Register(APIView):

  def post(self, request):
    response = {}
    try:
      ticket_id = request.data.get('ticket_id')
      lucky_draw_id = request.data.get('lucky_draw_id')

      lucky_draw = LuckyDraw.objects.get(id = lucky_draw_id)
      ticket = Ticket.objects.get(id = ticket_id)
      
      lucky_draw.participants.add(ticket)
      lucky_draw.save()

      ticket.is_used = True
      ticket.save()

      response['status_code'] = 200
      response['status_message'] = 'Registration Successfull' 
    except Exception as e:
        print(e)
    return Response(response)
  
class Draw(APIView):

  def post(self, request):
    response = {}
    try:
      lucky_draw_id = request.data.get('lucky_draw_id')
      lucky_draw = LuckyDraw.objects.get(id = lucky_draw_id)
      
      participants = lucky_draw.participants.all()
      win_ticket = random.choice(participants)

      winner = win_ticket.user

      reward = lucky_draw.rewards.all().first()
    
      winner_entry = Winner.objects.create(name = winner.username, ticket = win_ticket, reward = reward, lucky_draw = lucky_draw)

      response['status_code'] = 200
      response['status_message'] = 'Draw Successfull'
    except Exception as e:
        print(e)
    return Response(response)