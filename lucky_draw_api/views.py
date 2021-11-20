from django.shortcuts import render
from django.forms.models import model_to_dict

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *

import random
from datetime import datetime, timedelta

from lucky_draw_api.serializers import UserSerializer, TicketSerializer, RewardSerializer, LuckyDrawSerializer, WinnerSerializer
from lucky_draw_api.models import Ticket, Reward, LuckyDraw, Winner

class UserViewSet(viewsets.ModelViewSet):
  """
    CRUD Model Viewset for User
  """
  queryset = User.objects.all()
  serializer_class = UserSerializer

class RewardViewSet(viewsets.ModelViewSet):
  """
    CRUD Model Viewset for Reward
  """
  queryset = Reward.objects.all()
  serializer_class = RewardSerializer


class TicketViewSet(viewsets.ModelViewSet):
  """
    Task 1 (View): Design an API which allows users to get the raffle tickets.
  """
  queryset = Ticket.objects.all()
  serializer_class = TicketSerializer

class LuckyDrawViewSet(viewsets.ModelViewSet):
  """
    Task 2 (View): Design an API which shows the next Lucky Draw Event timing & the corresponding reward.
  """
  queryset = LuckyDraw.objects.filter(is_active = True)
  serializer_class = LuckyDrawSerializer

class Register(APIView):
  """
    Task 3 (View): Design an API which allows users to participate in the game (only once).
  """
  def post(self, request):
    response = {}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    response['status'] = "error"

    try:
      ticket_id = request.data.get('ticket_id')
      lucky_draw_id = request.data.get('lucky_draw_id')

      if ticket_id is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'ticket_id is required'
          raise Exception('ticket_id is required')
      
      if lucky_draw_id is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'lucky_draw_id is required'
          raise Exception('lucky_draw_id is required')

      lucky_draw = LuckyDraw.objects.get(id = lucky_draw_id)
      ticket = Ticket.objects.get(id = ticket_id)

      if not lucky_draw.is_active:
          status_code = status.HTTP_403_FORBIDDEN
          response['message'] = 'lucky_draw expired'
          raise Exception('lucky_draw expired')

      if ticket.is_used:
          status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
          response['message'] = 'ticket already deposited'
          raise Exception('ticket already deposited')
      
      user = ticket.user

      if lucky_draw.reg_tickets.filter(user = user):
          status_code = status.HTTP_403_FORBIDDEN
          response['message'] = 'you are already registered for this lucky draw'
          raise Exception('already registered')
      
      lucky_draw.reg_tickets.add(ticket)
      lucky_draw.save()

      ticket.is_used = True
      ticket.save()

      response['status'] = "success"
      response['ticket'] = model_to_dict(ticket)
      status_code = status.HTTP_200_OK
    except Exception as e:
        print(e)
    return Response(response, status=status_code)

class WinnerViewSet(viewsets.ModelViewSet):
  """
    Task 4 (View): Design an API which allows users to participate in the game (only once).
  """
  queryset = Winner.objects.filter(win_date__gte = datetime.now() - timedelta(days = 7))
  serializer_class = WinnerSerializer
  
class Draw(APIView):
  """
    Task 5 (View): Compute the winner for the event and announce the winner.
  """
  def post(self, request):
    response = {}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    response['status'] = "error"

    try:
      lucky_draw_id = request.data.get('lucky_draw_id')
      redeem_date = request.data.get('redeem_date')

      if lucky_draw_id is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'lucky_draw_id is required'
          raise Exception('lucky_draw_id is required')
      
      if redeem_date is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'redeem_date is required'
          raise Exception('redeem_date is required')

      redeem_date = datetime.strptime(redeem_date, "%Y-%m-%d").date()
      lucky_draw = LuckyDraw.objects.get(id = lucky_draw_id)
      
      if not lucky_draw.is_active:
          status_code = status.HTTP_403_FORBIDDEN
          response['message'] = 'lucky_draw expired'
          raise Exception('lucky_draw expired')

      tickets = lucky_draw.reg_tickets.all()

      if len(tickets) == 0:
          status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
          response['message'] = 'No tickets registered for the draw'
          raise Exception('no tickets registered for the draw')

      win_ticket = random.choice(tickets)
      winner = win_ticket.user
      
      reward = lucky_draw.rewards.filter(redeem_date=redeem_date).first()

      if reward is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'No reward announced on given date'
          raise Exception('No reward announced on given date')

      if reward.is_won:
          status_code = status.HTTP_403_FORBIDDEN
          response['message'] = 'Reward already claimed for today'
          raise Exception('reward already claimed for today')
      
      reward.is_won = True
      reward.save()

      winner_entry = Winner.objects.create(name = winner.username, ticket = win_ticket, reward = reward, lucky_draw = lucky_draw, win_date = datetime.now())

      status_code = status.HTTP_200_OK
      response['status'] = "success"
      response['winner'] = model_to_dict(winner_entry)
    except Exception as e:
        print(e)
    return Response(response, status=status_code)
