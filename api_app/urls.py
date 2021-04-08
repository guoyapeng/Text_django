from django.urls import path
from rest_framework.routers import SimpleRouter

from api_app.views import get_district, HotCityView, \
    AgentViewSet, HouseTypeViewSet, EstateViewSet, TagViewSet, HouseInfoViewSet, get_code_by_sms, login, ProvincesView, \
    UserViewSet

urlpatterns = [
    path('token/', login),
    path('mobile/<str:tel>/', get_code_by_sms),

    path('districts/<int:distid>/', get_district),

    path('districts/', ProvincesView.as_view()),
    path('hotcities/', HotCityView.as_view()),
]

router = SimpleRouter()
router.register('housetypes', HouseTypeViewSet)
router.register('estates', EstateViewSet)
router.register('agents', AgentViewSet)
router.register('tags', TagViewSet)
router.register('houseinfos', HouseInfoViewSet)
router.register('users', UserViewSet)
urlpatterns += router.urls
