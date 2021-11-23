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

    GET /users
    POST /users/
    POST /users/login/
    PUT /users/{{pk}}/
    DELETE /users/{{pk}}/

  """
  queryset = User.objects.all()
  serializer_class = UserSerializer

  # login endpoint
  @action(detail=False, methods=['post'])
  def login(self, request):
      response = {}
      status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
      response['status'] = "error"

      # not using serilaizer validation here to overcome name field uniqueness
      try:
        username = request.data.get('username')
        password = request.data.get('password')

        # check username
        if username is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'username is required'
          raise Exception('username is required')
        
        # check password
        if password is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'password is required'
          raise Exception('password is required')
        
        # using filter instead of get for error handling
        user = User.objects.filter(username = username).first()

        if user is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'no user with given username exists'
          raise Exception('no user with given username exists')
        
        # password validation
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
    CRUD Model Viewset for Rewards

    GET /rewards
    POST /rewards/
    PUT /rewards/{{pk}}/
    DELETE /rewards/{{pk}}/

  """
  queryset = Reward.objects.all()
  serializer_class = RewardSerializer


class TicketViewSet(viewsets.ModelViewSet):
  """
    CRUD Model Viewset for Tickets

    GET /tickets
    POST /tickets/
    POST /tickets/?amount=x
    PUT /tickets/{{pk}}/
    DELETE /tickets/{{pk}}/

  """
  queryset = Ticket.objects.all()
  serializer_class = TicketSerializer

  # altering default viewset method for creating multiple tickets
  def create(self, request, *args, **kwargs):
    """
      Task 1: Design an API which allows users to get the raffle tickets.
    """
    num = self.request.query_params.get('amount')
    data = [request.data]

    # multiple tickets
    if num:
      data = data*int(num)

    serializer = self.get_serializer(data=data, many= True)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)

    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class LuckyDrawViewSet(viewsets.ModelViewSet):
  """
    CRUD Model Viewset for LuckyDraws

    GET /luckydraws
    GET /luckydraws/{{pk}}/nextevent/
    POST /luckydraws/
    POST /luckydraws/{{pk}}/register/
    POST /luckydraws/{{pk}}/compute/
    PUT /luckydraws/{{pk}}/
    DELETE /luckydraws/{{pk}}/

  """
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

      # check lucky draw
      if lucky_draw is None:
        status_code = status.HTTP_404_NOT_FOUND
        response['message'] = 'no lucky draw with given id exists'
        raise Exception('no lucky draw with given id exists')
      
      # check if lucky draw is active
      if not lucky_draw.is_active:
        status_code = status.HTTP_403_FORBIDDEN
        response['message'] = 'lucky_draw expired'
        raise Exception('lucky_draw expired')
      
      # check if lucky draw has rewards
      if len(lucky_draw.rewards.all()) == 0:
        status_code = status.HTTP_400_BAD_REQUEST
        response['message'] = 'no rewards announced'
        raise Exception('no rewards announced')
      
      # return the next active event ordered by redeem date
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
      Task 3: Design an API which allows users to participate in the lucky draw (only once).
    """
    response = {}
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    response['status'] = "error"

    try:
      lucky_draw = LuckyDraw.objects.filter(pk = pk).first()

      # check lucky draw
      if lucky_draw is None:
        status_code = status.HTTP_404_NOT_FOUND
        response['message'] = 'no lucky draw with given id exists'
        raise Exception('no lucky draw with given id exists')

      ticket_id = request.data.get('ticket_id')

      # check ticket
      if ticket_id is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'ticket_id is required'
          raise Exception('ticket_id is required')

      ticket = Ticket.objects.get(id = ticket_id)

      # check if lucky draw is active
      if not lucky_draw.is_active:
          status_code = status.HTTP_403_FORBIDDEN
          response['message'] = 'lucky_draw expired'
          raise Exception('lucky_draw expired')
      
      # check if ticket is used
      if ticket.is_used:
          status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
          response['message'] = 'ticket already deposited'
          raise Exception('ticket already deposited')
      
      user = ticket.user

      # check if user already registered
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

      # check lucky draw
      if lucky_draw is None:
        status_code = status.HTTP_404_NOT_FOUND
        response['message'] = 'no lucky draw with given id exists'
        raise Exception('no lucky draw with given id exists')
      
      redeem_date = request.data.get('redeem_date')

      # check redeem date
      if redeem_date is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'redeem_date is required'
          raise Exception('redeem_date is required')
      
      # format text to date
      redeem_date = datetime.strptime(redeem_date, "%Y-%m-%d").date()
      
      # check if lucky draw is active
      if not lucky_draw.is_active:
          status_code = status.HTTP_403_FORBIDDEN
          response['message'] = 'lucky_draw expired'
          raise Exception('lucky_draw expired')

      tickets = lucky_draw.reg_tickets.all()

      # check if there are tickets registered for the draw
      if len(tickets) == 0:
          status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
          response['message'] = 'No tickets registered for the draw'
          raise Exception('no tickets registered for the draw')
      
      # find the upcoming reward with given redeem date
      reward = lucky_draw.rewards.filter(redeem_date=redeem_date).first()

      # check if reward exists
      if reward is None:
          status_code = status.HTTP_400_BAD_REQUEST
          response['message'] = 'No reward announced on given date'
          raise Exception('No reward announced on given date')
      
      # check if reward has been won
      if reward.is_won:
          status_code = status.HTTP_403_FORBIDDEN
          response['message'] = 'Reward already claimed for today'
          raise Exception('reward already claimed for today')

      win_ticket = random.choice(tickets)
      win_ticket.save()

      winner = win_ticket.user
      
      reward.is_won = True
      reward.save()

      # create winner entry
      winner_entry = Winner.objects.create(user = winner, ticket = win_ticket, reward = reward, lucky_draw = lucky_draw, win_date = redeem_date)

      status_code = status.HTTP_200_OK
      response['status'] = "success"
      response['winner'] = WinnerSerializer(winner_entry).data
    except Exception as e:
        print(e)
    return Response(response, status=status_code)


class WinnerViewSet(viewsets.ReadOnlyModelViewSet):
  """
    CRUD Model Viewset for Winners

    GET /winners
    GET /winners/?span=x
    POST /winners/
    PUT /winners/{{pk}}/
    DELETE /winners/{{pk}}/

  """
  serializer_class = WinnerSerializer
  queryset = Winner.objects.all()

  def get_queryset(self):
    """
      Task 4: Design an API which lists all the winners of all the events in the last one week.

      (Querying the API with span = 7)
    """
    queryset = self.queryset
    span = self.request.query_params.get('span')
    
    # modify queryset to include winners in last `span` days only
    if span:
        queryset = queryset.filter(win_date__gte = datetime.now() - timedelta(days = int(span)))

    return queryset
