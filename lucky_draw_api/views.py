from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

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
  queryset = LuckyDraw.objects.filter(is_active = True)
  serializer_class = LuckyDrawSerializer

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
  
