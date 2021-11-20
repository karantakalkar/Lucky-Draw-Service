from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *

import random
from datetime import datetime

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
    response['status_code'] = 500
    response['status_message'] = 'internal server error'

    try:
      ticket_id = request.data.get('ticket_id')
      lucky_draw_id = request.data.get('lucky_draw_id')

      if ticket_id is None:
          response['status_message'] = 'ticket_id is required'
          raise Exception('ticket_id is required')
      
      if lucky_draw_id is None:
          response['status_message'] = 'lucky_draw_id is required'
          raise Exception('lucky_draw_id is required')

      lucky_draw = LuckyDraw.objects.get(id = lucky_draw_id)
      ticket = Ticket.objects.get(id = ticket_id)

      if not lucky_draw.is_active:
          response['status_code'] = 422
          response['status_message'] = 'lucky_draw expired'
          raise Exception('lucky_draw expired')

      if ticket.is_used:
          response['status_code'] = 422
          response['status_message'] = 'ticket already deposited'
          raise Exception('ticket already deposited')
      
      user = ticket.user

      if lucky_draw.reg_tickets.filter(user = user):
          response['status_code'] = 422
          response['status_message'] = 'you are already registered for this lucky draw'
          raise Exception('already registered')
      
      lucky_draw.reg_tickets.add(ticket)
      lucky_draw.save()

      ticket.is_used = True
      ticket.save()

      response['status_code'] = 200
      response['status_message'] = 'registration successfull' 
    except Exception as e:
        print(e)
    return Response(response)
  
class Draw(APIView):

  def post(self, request):
    response = {}
    response['status_code'] = 500
    response['status_message'] = 'internal server error'

    try:
      lucky_draw_id = request.data.get('lucky_draw_id')
      redeem_date = request.data.get('redeem_date')

      if lucky_draw_id is None:
          response['status_message'] = 'lucky_draw_id is required'
          raise Exception('lucky_draw_id is required')
      
      if redeem_date is None:
          response['status_message'] = 'redeem_date is required'
          raise Exception('redeem_date is required')

      redeem_date = datetime.strptime(redeem_date, "%Y-%m-%d").date()
      lucky_draw = LuckyDraw.objects.get(id = lucky_draw_id)
      
      if not lucky_draw.is_active:
          response['status_code'] = 422
          response['status_message'] = 'lucky_draw expired'
          raise Exception('lucky_draw expired')

      tickets = lucky_draw.reg_tickets.all()

      if len(tickets) == 0:
          response['status_code'] = 422
          response['status_message'] = 'No tickets registered for the draw'
          raise Exception('no tickets registered for the draw')

      win_ticket = random.choice(tickets)
      winner = win_ticket.user
      
      reward = lucky_draw.rewards.filter(redeem_date=redeem_date).first()

      if reward is None:
          response['status_message'] = 'No reward announced on given date'
          raise Exception('No reward announced on given date')

      if reward.is_won:
          response['status_message'] = 'Reward already claimed for today'
          raise Exception('reward already claimed for today')
      
      reward.is_won = True
      reward.save()

      winner_entry = Winner.objects.create(name = winner.username, ticket = win_ticket, reward = reward, lucky_draw = lucky_draw)

      response['status_code'] = 200
      response['status_message'] = 'Draw Successfull'
    except Exception as e:
        print(e)
    return Response(response)