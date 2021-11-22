from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth.hashers import make_password, check_password

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

  @action(detail=False, methods=['post'])
  def login(self, request):
      response = {}
      status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
      response['status'] = "error"

      # not using serilaizer validation here to overcome name field uniqueness
      try:
        username = request.data.get('username')
        password = request.data.get('password')

        if username is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'username is required'
          raise Exception('username is required')
        
        if password is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'password is required'
          raise Exception('password is required')

        user = User.objects.filter(username = username).first()

        if user is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'no user with given username exists'
          raise Exception('no user with given username exists')

        if not check_password(password, user.password):
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'wrong password'
          raise Exception('wrong password')

        serializer  = UserSerializer(user)

        response['status'] = "success"
        response['user'] = serializer.data
        status_code = status.HTTP_200_OK
      except Exception as e:
        print(e)
      return Response(response, status=status_code)

class RewardViewSet(viewsets.ModelViewSet):
  """
    CRUD Model Viewset for Reward
  """
  queryset = Reward.objects.all()
  serializer_class = RewardSerializer


class TicketViewSet(viewsets.ModelViewSet):
  queryset = Ticket.objects.all()
  serializer_class = TicketSerializer

  # altering default viewset method for creating multiple tickets
  def create(self, request, *args, **kwargs):
    """
      Task 1: Design an API which allows users to get the raffle tickets.
    """
    num = self.request.query_params.get('amount')
    data = [request.data]

    if num:
      data = data*int(num)

    serializer = self.get_serializer(data=data, many= True)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)

    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LuckyDrawViewSet(viewsets.ModelViewSet):
  queryset = LuckyDraw.objects.all()
  serializer_class = LuckyDrawSerializer

  @action(detail=True, methods=['get'])
  def nextevent(self, request, pk = None):
    """
      Task 2: Design an API which shows the next Lucky Draw Event timing & the corresponding reward.
    """
    response = {}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    response['status'] = "error"

    try:
      lucky_draw = LuckyDraw.objects.filter(pk = pk).first()

      if lucky_draw is None:
        status_code = status.HTTP_404_NOT_FOUND
        response['message'] = 'no lucky draw with given id exists'
        raise Exception('no lucky draw with given id exists')

      if not lucky_draw.is_active:
        status_code = status.HTTP_403_FORBIDDEN
        response['message'] = 'lucky_draw expired'
        raise Exception('lucky_draw expired')

      if len(lucky_draw.rewards.all()) == 0:
        status_code = status.HTTP_400_BAD_REQUEST
        response['message'] = 'no rewards announced'
        raise Exception('no rewards announced')
      
      next_event = lucky_draw.rewards.filter(redeem_date__gt = datetime.now(), is_won = False).order_by('redeem_date').first()

      serializer = RewardSerializer(next_event)

      status_code = status.HTTP_200_OK
      response = serializer.data

    except Exception as e:
      print(e)
    return Response(response, status=status_code)
    
  @action(detail=True, methods=['post'])
  def register(self, request, pk = None):
    """
      Task 3: Design an API which allows users to participate in the lcuky draw (only once).
    """
    response = {}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    response['status'] = "error"

    try:
      lucky_draw = LuckyDraw.objects.filter(pk = pk).first()

      if lucky_draw is None:
        status_code = status.HTTP_404_NOT_FOUND
        response['message'] = 'no lucky draw with given id exists'
        raise Exception('no lucky draw with given id exists')

      ticket_id = request.data.get('ticket_id')

      if ticket_id is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'ticket_id is required'
          raise Exception('ticket_id is required')

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
      response['reg_ticket'] = TicketSerializer(ticket).data
      status_code = status.HTTP_200_OK
    except Exception as e:
        print(e)
    return Response(response, status=status_code)
  
  @action(detail=True, methods=['post'])
  def compute(self, request, pk = None):
    """
      Task 5 (View): Compute the winner for the event and announce the winner.
    """
    response = {}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    response['status'] = "error"

    try:
      lucky_draw = LuckyDraw.objects.filter(pk = pk).first()

      if lucky_draw is None:
        status_code = status.HTTP_404_NOT_FOUND
        response['message'] = 'no lucky draw with given id exists'
        raise Exception('no lucky draw with given id exists')
      
      redeem_date = request.data.get('redeem_date')

      if redeem_date is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'redeem_date is required'
          raise Exception('redeem_date is required')

      redeem_date = datetime.strptime(redeem_date, "%Y-%m-%d").date()
      
      if not lucky_draw.is_active:
          status_code = status.HTTP_403_FORBIDDEN
          response['message'] = 'lucky_draw expired'
          raise Exception('lucky_draw expired')

      tickets = lucky_draw.reg_tickets.all()

      if len(tickets) == 0:
          status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
          response['message'] = 'No tickets registered for the draw'
          raise Exception('no tickets registered for the draw')
      
      reward = lucky_draw.rewards.filter(redeem_date=redeem_date).first()

      if reward is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'No reward announced on given date'
          raise Exception('No reward announced on given date')

      if reward.is_won:
          status_code = status.HTTP_403_FORBIDDEN
          response['message'] = 'Reward already claimed for today'
          raise Exception('reward already claimed for today')

      win_ticket = random.choice(tickets)
      win_ticket.save()

      winner = win_ticket.user
      
      reward.is_won = True
      reward.save()

      winner_entry = Winner.objects.create(user = winner, ticket = win_ticket, reward = reward, lucky_draw = lucky_draw, win_date = redeem_date)

      status_code = status.HTTP_200_OK
      response['status'] = "success"
      response['winner'] = WinnerSerializer(winner_entry).data
    except Exception as e:
        print(e)
    return Response(response, status=status_code)


class WinnerViewSet(viewsets.ReadOnlyModelViewSet):
  serializer_class = WinnerSerializer
  queryset = Winner.objects.all()

  def get_queryset(self):
    """
      Task 4: Design an API which lists all the winners of all the events in the last one week.

      (Querying the API with span = 7)
    """
    queryset = self.queryset
    span = self.request.query_params.get('span')
  
    if span:
        queryset = queryset.filter(win_date__gte = datetime.now() - timedelta(days = int(span)))

    return queryset
