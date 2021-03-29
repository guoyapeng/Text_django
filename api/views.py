import json
import pickle

from django.core.cache import cache, caches
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.helper import AgentCursorPagination, CustomThrottle
from api.serializers import DistrictSimpleSerializers, DistrictDetailSerializers, DistrictDetailSerializerd, \
    AgentSimpleSerializer, AgentCreateSerializer, AgentDetailSerializer, HouseTypeSerializer, EstateSimpleSerializer, \
    EstateDetailSerializer
from common.models import District, Agent, HouseType, Estate


# 序列化：手动
def get_provinces_1_1(request: HttpRequest) -> HttpResponse:
    queryset = District.objects.filter(parent__isnull=True)

    provinces = []
    for district in queryset:
        provinces.append({
            "distid": district.distid,
            "name": district.name,
        })

    data = json.dumps(provinces)
    return HttpResponse(data, content_type='application/json; charset=utf-8')


# 序列化：函数
def get_provinces_1_2(request: HttpRequest) -> HttpResponse:
    queryset = District.objects.filter(parent__isnull=True)

    provinces = []
    for district in queryset:
        provinces.append({
            "distid": district.distid,
            "name": district.name,
        })

    return JsonResponse(provinces, safe=False)


# 序列化：自定义
def get_provinces_2_1(request: HttpRequest) -> HttpResponse:
    queryset = District.objects.filter(parent__isnull=True)
    serializer = DistrictSimpleSerializers(queryset, many=True).data

    return JsonResponse({
        'code': 10000,
        'message': '获取省级行政区域成功',
        'results': serializer
    })


# 序列化：自定义。缓存：声明式
@cache_page(timeout=30)
@api_view(("GET",))
def get_provinces_2_2(request: HttpRequest) -> HttpResponse:
    queryset = District.objects.filter(parent__isnull=True).only('distid', 'name')
    serializer = DistrictSimpleSerializers(queryset, many=True).data

    return Response({
        'code': 10000,
        'message': '获取省级行政区域成功',
        'results': serializer
    })


# 序列化：自定义。缓存：声明式
@cache_page(timeout=30)
@api_view(("GET",))
def get_provinces(request: HttpRequest, distid: int) -> HttpResponse:
    # 查询某个指定地区的详情
    district = District.objects.filter(distid=distid).defer('parent').first()
    serializer = DistrictDetailSerializers(district).data

    return Response(serializer)


# 序列化：自定义。缓存：编程式方式一。限流：自定义
@throttle_classes((CustomThrottle,))
@api_view(("GET",))
def get_provinced(request: HttpRequest, distid: int) -> HttpResponse:
    """第一种编程式缓存方式"""
    district = caches['default'].get(f'district:{distid}')
    if district is None:
        # 查询某个指定地区的详情，以及其下一级行政区域。加缓存后框架还会有两次自动查询SQL的请求
        district = District.objects.filter(distid=distid).defer('parent').first()
        caches['default'].set(f'district:{distid}', district, timeout=900)
    serializer = DistrictDetailSerializerd(district).data

    return Response(serializer)


# 类视图。查询所有
class AgentView_L(ListAPIView):
    queryset = Agent.objects.all().only('name', 'tel', 'servstar')
    serializer_class = AgentSimpleSerializer

    def get(self, request, *args, **kwargs):
        resp = super(AgentView_L, self).get(request, *args, **kwargs)
        return Response({
            'code': 10000,
            'message': '获取经理人成功',
            'results': resp.data
        })


# 类视图。查询单个
class AgentView_R(RetrieveAPIView):
    queryset = Agent.objects.all().only('name', 'tel', 'servstar')
    serializer_class = AgentSimpleSerializer


# 类视图。查询单个+更新
class AgentView_RU(RetrieveUpdateAPIView):
    queryset = Agent.objects.all().only('name', 'tel', 'servstar')
    serializer_class = AgentSimpleSerializer


# 类视图。查询列表+新增、查询单个+更新
class AgentView_LC_RU_01(ListCreateAPIView, RetrieveUpdateAPIView):
    queryset = Agent.objects.all().only('name', 'tel', 'servstar')
    serializer_class = AgentSimpleSerializer

    def get(self, request, *args, **kwargs):
        cls = RetrieveUpdateAPIView if 'pk' in kwargs else ListCreateAPIView
        return cls.get(self, request, *args, **kwargs)


# 类视图。查询列表+新增、查询单个+更新
class AgentView_LC_RU_02(ListCreateAPIView, RetrieveUpdateAPIView):
    queryset = Agent.objects.all().only('name', 'tel', 'servstar')

    def get_serializer_class(self):
        return AgentCreateSerializer if self.request.method == "POST" else AgentSimpleSerializer

    def get(self, request, *args, **kwargs):
        cls = RetrieveUpdateAPIView if 'pk' in kwargs else ListCreateAPIView
        return cls.get(self, request, *args, **kwargs)


# 类视图。查询列表+新增、查询单个+更新 及联查询。分页：游标分页
class AgentView_LC_RU_03(RetrieveUpdateAPIView, ListCreateAPIView):
    # 游标分页设置
    pagination_class = AgentCursorPagination

    def get_queryset(self):
        queryset = Agent.objects.all()
        if 'pk' not in self.kwargs:
            queryset = queryset.only('name', 'tel', 'servstar')
        else:
            queryset = queryset.prefetch_related(
                Prefetch('estates', queryset=Estate.objects.all().only('name').order_by('-hot')))
        return queryset.order_by('-servstar')

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AgentCreateSerializer
        else:
            return AgentDetailSerializer if "pk" in self.kwargs else AgentSimpleSerializer

    def get(self, request, *args, **kwargs):
        cls = RetrieveUpdateAPIView if 'pk' in kwargs else ListCreateAPIView
        return cls.get(self, request, *args, **kwargs)


# 类视图集。增加、删除、修改、查单个查列表。分页：禁止分页。缓存：声明式
@method_decorator(decorator=cache_page(timeout=86400), name='list')
@method_decorator(decorator=cache_page(timeout=86400), name='retrieve')
class HouseTypeViewSet(ModelViewSet):
    queryset = HouseType.objects.all()
    serializer_class = HouseTypeSerializer
    pagination_class = None  # 禁止此接口分页


# 类视图集。只读。分页：默认分页。缓存：声明式。限流：自定义
@method_decorator(decorator=cache_page(timeout=86400), name='list')
@method_decorator(decorator=cache_page(timeout=86400), name='retrieve')
class EstateViewSet(ReadOnlyModelViewSet):
    queryset = Estate.objects.all()

    # 用自定义限流类实现对该接口的限流设置
    throttle_classes = (CustomThrottle,)

    def get_queryset(self):
        if self.action == 'list':
            queryset = self.queryset.only('name')
        else:
            queryset = self.queryset.defer('district__parent', 'district__ishot', 'district__intro').select_related(
                'district')
        return queryset

    def get_serializer_class(self):
        return EstateDetailSerializer if self.action == 'retrieve' else EstateSimpleSerializer


# 序列化：自定义。缓存：编程式方式二
@api_view(("GET",))
def districts(request: HttpRequest, distid: int) -> HttpResponse:
    """ 编程式缓存的第二种实现方式。调用原生redis连接"""
    redis_cli = get_redis_connection()
    data = redis_cli.get(f'izufang:district:{distid}')
    if data:
        district = pickle.loads(data)
    else:
        district = District.objects.filter(distid=distid).first()
        redis_cli.set(f'izufang:district:{distid}', pickle.dumps(district))
    serializer = DistrictDetailSerializerd(district).data
    return Response(serializer)
