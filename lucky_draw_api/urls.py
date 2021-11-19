from django.urls import include, path

from rest_framework import routers

from lucky_draw_api.views import UserViewSet, TicketViewSet, RewardViewSet, LuckyDrawViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet)
router.register(r'ticket', TicketViewSet)
router.register(r'reward', RewardViewSet)
router.register(r'luckydraw', LuckyDrawViewSet)

urlpatterns = [
   path('', include(router.urls)),
]