from django.urls import path
from rest_framework.routers import SimpleRouter

from api.views import get_provinces_1_1, get_provinces_1_2, get_provinces_2_1, get_provinces_2_2, get_provinces, \
    get_provinced, AgentView_LC_RU_02, AgentView_LC_RU_01, AgentView_L, AgentView_RU, AgentView_R, AgentView_LC_RU_03, \
    HouseTypeViewSet, EstateViewSet, districts, AgentView

urlpatterns = [
    # 视图函数的序列化方式，接口实现方式和返回方式测试
    path('districts_1_1/', get_provinces_1_1),
    path('districts_1_2/', get_provinces_1_2),
    path('districts_2_1/', get_provinces_2_1),
    path('districts_2_2/', get_provinces_2_2),

    path('district/<int:distid>/', get_provinces),
    path('districtd/<int:distid>/', get_provinced),


    # 视图父类的序列化方式，接口实现方式和返回方式测试
    path('agent_L/', AgentView_L.as_view()),
    path('agent_R/<int:pk>', AgentView_R.as_view()),
    path('agent_RU/<int:pk>', AgentView_RU.as_view()),

    path('agent_LC_RU_01/', AgentView_LC_RU_01.as_view()),
    path('agent_LC_RU_01/<int:pk>', AgentView_LC_RU_01.as_view()),
    path('agent_LC_RU_02/', AgentView_LC_RU_02.as_view()),
    path('agent_LC_RU_02/<int:pk>', AgentView_LC_RU_02.as_view()),
    path('agent_LC_RU_03/', AgentView_LC_RU_03.as_view()),
    path('agent_LC_RU_03/<int:pk>', AgentView_LC_RU_03.as_view()),


    # 编程式缓存的第二种实现方式。调用原生redis连接
    path('districts/<int:distid>', districts),


    # 数据筛选
    path('agent/', AgentView.as_view())

]

# 视图类集的序列化方式，接口实现方式和返回方式测试
router = SimpleRouter()

router.register('housetypes', HouseTypeViewSet)
router.register('estates', EstateViewSet)

urlpatterns += router.urls
