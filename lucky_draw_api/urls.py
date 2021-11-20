from django.urls import include, path

from rest_framework import routers

from lucky_draw_api.views import UserViewSet, TicketViewSet, RewardViewSet, LuckyDrawViewSet, WinnerViewSet,  Register, Draw

router = routers.DefaultRouter()

router.register(r'user', UserViewSet)
router.register(r'ticket', TicketViewSet)
router.register(r'reward', RewardViewSet)
router.register(r'luckydraw', LuckyDrawViewSet)
router.register(r'winners', WinnerViewSet)

urlpatterns = [
   path('', include(router.urls)),
   path('register/', Register.as_view()),
   path('draw/', Draw.as_view())
]