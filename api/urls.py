from django.urls import path

from api.views import get_provinces_1_1, get_provinces_1_2, get_provinces_2_1, get_provinces_2_2, get_provinces, \
    get_provinced, AgentViews, AgentViewd, AgentViewRU, AgentView_LC_RU

urlpatterns = [
    # 视图函数的序列化方式，接口实现方式和返回方式测试
    path('districts_1_1/', get_provinces_1_1),
    path('districts_1_2/', get_provinces_1_2),
    path('districts_2_1/', get_provinces_2_1),
    path('districts_2_2/', get_provinces_2_2),

    path('district/<int:distid>/', get_provinces),
    path('districtd/<int:distid>/', get_provinced),

    # 视图类的序列化方式，接口实现方式和返回方式测试
    path('agent/', AgentViews.as_view()),
    path('agent/<int:pk>', AgentViewd.as_view()),
    path('agentRu/<int:pk>', AgentViewRU.as_view()),

    path('agent_LC_RU/', AgentView_LC_RU.as_view()),
    path('agent_LC_RU/<int:pk>', AgentView_LC_RU.as_view()),
]
