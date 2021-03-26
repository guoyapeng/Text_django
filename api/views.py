import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import DistrictSimpleSerializers
from common.models import District


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
    queryset = District.objects.filter(parent__isnull=True)
    serializer = DistrictSimpleSerializers(queryset, many=True).data

    return Response({
        'code': 10000,
        'message': '获取省级行政区域成功',
        'results': serializer
    })