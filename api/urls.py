from django.urls import path

from api.views import get_provinces

urlpatterns = [
    path('districts/', get_provinces)


]