from django.urls import path

from api.views import get_provinces_1_1, get_provinces_1_2, get_provinces_2_1, get_provinces_2_2

urlpatterns = [
    # 视图函数的序列化方式，接口实现方式和返回方式测试
    path('districts_1_1/', get_provinces_1_1),
    path('districts_1_2/', get_provinces_1_2),
    path('districts_2_1/', get_provinces_2_1),
    path('districts_2_2/', get_provinces_2_2),

]
