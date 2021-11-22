from django.urls import include, path

from rest_framework import routers

from lucky_draw_api.views import UserViewSet, TicketViewSet, RewardViewSet, LuckyDrawViewSet, WinnerViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'rewards', RewardViewSet)
router.register(r'luckydraws', LuckyDrawViewSet)
router.register(r'winners', WinnerViewSet)

urlpatterns = [
   path('', include(router.urls)),
]