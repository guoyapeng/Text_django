from django.urls import path

from api.views import get_provinces_1_1, get_provinces_1_2

urlpatterns = [
    path('districts_1_1/', get_provinces_1_1),
    path('districts_1_2/', get_provinces_1_2)

]
