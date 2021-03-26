import json

from django.http import HttpRequest, HttpResponse, JsonResponse
from common.models import District


# Create your views here.
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
