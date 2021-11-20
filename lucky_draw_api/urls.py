from django.urls import include, path

from rest_framework import routers

from lucky_draw_api.views import UserViewSet, TicketViewSet, RewardViewSet, LuckyDrawViewSet, WinnerViewSet,  Register, Draw

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'reward', RewardViewSet)

# Task 1 Endpoint
router.register(r'ticket', TicketViewSet) 
# Task 2 Endpoint
router.register(r'luckydraw', LuckyDrawViewSet)
# Task 4 Endpoint
router.register(r'winners', WinnerViewSet)

urlpatterns = [
   path('', include(router.urls)),
   # Task 3 Endpoint
   path('register/', Register.as_view()),
   # Task 5 Endpoint
   path('draw/', Draw.as_view())
]