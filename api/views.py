import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, ListCreateAPIView
from rest_framework.response import Response

from api.serializers import DistrictSimpleSerializers, DistrictDetailSerializers, DistrictDetailSerializerd, \
    AgentSimpleSerializer
from common.models import District, Agent


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


def get_provinces_1_2(request: HttpRequest) -> HttpResponse:
    queryset = District.objects.filter(parent__isnull=True)

    provinces = []
    for district in queryset:
        provinces.append({
            "distid": district.distid,
            "name": district.name,
        })

    return JsonResponse(provinces, safe=False)


def get_provinces_2_1(request: HttpRequest) -> HttpResponse:
    queryset = District.objects.filter(parent__isnull=True)
    serializer = DistrictSimpleSerializers(queryset, many=True).data

    return JsonResponse({
        'code': 10000,
        'message': '获取省级行政区域成功',
        'results': serializer
    })


@api_view(("GET",))
def get_provinces_2_2(request: HttpRequest) -> HttpResponse:
    queryset = District.objects.filter(parent__isnull=True).only('distid', 'name')
    serializer = DistrictSimpleSerializers(queryset, many=True).data

    return Response({
        'code': 10000,
        'message': '获取省级行政区域成功',
        'results': serializer
    })


@api_view(("GET",))
def get_provinces(request: HttpRequest, distid: int) -> HttpResponse:
    # 查询某个指定地区的详情
    district = District.objects.filter(distid=distid).defer('parent').first()
    serializer = DistrictDetailSerializers(district).data

    return Response(serializer)


@api_view(("GET",))
def get_provinced(request: HttpRequest, distid: int) -> HttpResponse:
    # 查询某个指定地区的详情，以及其下一级行政区域
    district = District.objects.filter(distid=distid).defer('parent').first()
    serializer = DistrictDetailSerializerd(district).data

    return Response(serializer)


# 类视图。继承父类实现列表对象查询
class AgentViews(ListAPIView):
    queryset = Agent.objects.all().only('name', 'tel', 'servstar')
    serializer_class = AgentSimpleSerializer

    def get(self, request, *args, **kwargs):
        resp = super(AgentViews, self).get(request, *args, **kwargs)
        return Response({
            'code': 10000,
            'message': '获取经理人成功',
            'results': resp.data
        })


# 类视图。继承父类实现单个对象查询
class AgentViewd(RetrieveAPIView):
    queryset = Agent.objects.all().only('name', 'tel', 'servstar')
    serializer_class = AgentSimpleSerializer


# 类视图。查询、更新
class AgentViewRU(RetrieveUpdateAPIView):
    queryset = Agent.objects.all().only('name', 'tel', 'servstar')
    serializer_class = AgentSimpleSerializer


# 类视图，查询列表+新增、查询单个+更新
class AgentView_LC_RU(ListCreateAPIView, RetrieveUpdateAPIView):
    queryset = Agent.objects.all().only('name', 'tel', 'servstar')
    serializer_class = AgentSimpleSerializer

    def get(self, request, *args, **kwargs):
        cls = RetrieveUpdateAPIView if 'pk' in kwargs else ListCreateAPIView
        return cls.get(self, request, *args, **kwargs)






