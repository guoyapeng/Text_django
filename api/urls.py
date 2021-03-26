from django.urls import path

from api.views import get_provinces_1_1, get_provinces_1_2, get_provinces_2_1, get_provinces_2_2, get_provinces, \
    get_provinced, AgentView

urlpatterns = [
    # 视图函数的序列化方式，接口实现方式和返回方式测试
    path('districts_1_1/', get_provinces_1_1),
    path('districts_1_2/', get_provinces_1_2),
    path('districts_2_1/', get_provinces_2_1),
    path('districts_2_2/', get_provinces_2_2),

    path('district/<int:distid>/', get_provinces),
    path('districtd/<int:distid>/', get_provinced),

    # 视图类的序列化方式，接口实现方式和返回方式测试
    path('agent/', AgentView.as_view())
]
