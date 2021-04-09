import datetime
import os
import uuid

import jwt
from django.core.cache import caches
from django.db.models import Prefetch, Q
from django.db.transaction import atomic
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api_app.consts import *
from api_app.helpers import EstateFilterSet, HouseInfoFilterSet, check_tel, DefaultResponse, \
    LoginRequiredAuthentication, RbacPermission
from api_app.serializers import *
from common.models import District, Agent, HouseType, Tag, User, LoginLog
from common.utils import gen_mobile_code, send_sms_by_luosimao, to_md5_hex, get_ip_address, upload_stream_to_qiniu
from izufang.settings import SECRET_KEY


# 前端没有实现，该接口未测试
@api_view(('POST',))
def upload_house_photo(request):
    file_obj = request.FILES.get(('mainphoto'))
    filename = f'{uuid.uuid4().hex}{os.path.splitext(file_obj.name)[1]}'
    upload_stream_to_qiniu.delay(file_obj.file, filename, len(file_obj))
    photo = HousePhoto()
    photo.path = f'http://q69nr46pe.bkt.clouddn.com/{filename}'
    photo.ismain = True  # 数据库中暂无该字段
    photo.save()
    return DefaultResponse(*FILE_UPLOAD_SUCCESS, data={
        'photoid': photo.photoid,
        'url': photo.path
    })


# 注册接口
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action == 'update':
            return UserUpdateSerializer
        return UserSimpleSerializer


# 登陆接口。
@api_view(('POST',))
def login(request):
    """登录（获取用户身份令牌）"""
    username = request.data.get('username')
    password = request.data.get('password')
    if username and password:
        password = to_md5_hex(password)
        user = User.objects.filter(
            Q(username=username, password=password) |
            Q(tel=username, password=password) |
            Q(email=username, password=password)
        ).first()
        if user:
            # roles = RoleSimpleSerializer(user.roles.all(), many=True).data
            # 用户登录成功通过JWT生成用户身份令牌
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'data': {'userid': user.userid, }
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode()
            with atomic():
                current_time = timezone.now()
                if not user.lastvisit or \
                        (current_time - user.lastvisit).days >= 1:
                    user.point += 2
                    user.lastvisit = current_time
                    user.save()
                loginlog = LoginLog()
                loginlog.user = user
                loginlog.logdate = current_time
                loginlog.ipaddr = get_ip_address(request)
                loginlog.save()
            resp = DefaultResponse(*USER_LOGIN_SUCCESS, data={'token': token})
        else:
            resp = DefaultResponse(*USER_LOGIN_FAILED)
    else:
        resp = DefaultResponse(*INVALID_LOGIN_INFO)
    return resp


@api_view(('GET',))
def get_code_by_sms(request, tel):
    """获取短信验证码"""
    if check_tel(tel):
        if caches['default'].get(f'{tel}:block'):
            resp = DefaultResponse(*CODE_TOO_FREQUENCY)
        else:
            code = gen_mobile_code()
            message = f'您的短信验证码是{code},【软件开发】'
            # 使用delay()方式去执行且参数是没有变化
            send_sms_by_luosimao.delay(tel, message=message)
            caches['default'].set(f'{tel}:block', code, timeout=120)   # 阻止一定时间内禁止重发
            caches['default'].set(f'{tel}:valid', code, timeout=1800)  # 设置验证码的有效时间段
            resp = DefaultResponse(*MOBILE_CODE_SUCCESS)
    else:
        resp = DefaultResponse(*INVALID_TEL_NUM)
    return resp


@api_view(('GET',))
def get_district(request, distid):
    """获取地区详情"""
    redis_cli = get_redis_connection()
    data = redis_cli.get(f'zufang:district:{distid}')
    if data:
        data = ujson.loads(data)
    else:
        district = District.objects.filter(distid=distid) \
            .defer('parent').first()
        data = DistrictDetailSerializer(district).data
        redis_cli.set(f'zufang:district:{distid}', ujson.dumps(data), ex=900)
    return Response(data)


@method_decorator(decorator=cache_page(timeout=86400), name='get')
class ProvincesView(ListAPIView):
    queryset = District.objects.filter(parent__isnull=True).only('name')
    serializer_class = DistrictSimpleSerializer(queryset, many=True)


@method_decorator(decorator=cache_page(timeout=86400), name='get')
class HotCityView(ListAPIView):
    """热门城市视图
    get:
        获取热门城市
    """
    queryset = District.objects.filter(ishot=True).only('name')
    serializer_class = DistrictSimpleSerializer
    pagination_class = None


@method_decorator(decorator=cache_page(timeout=120), name='list')
@method_decorator(decorator=cache_page(timeout=300), name='retrieve')
class AgentViewSet(ModelViewSet):
    """经理人视图
    list:
        获取经理人列表
    retrieve:
        获取经理人详情
    create:
        创建经理人
    update:
        更新经理人信息
    partial_update:
        更新经理人信息
    delete:
        删除经理人
    """
    queryset = Agent.objects.all()

    def get_queryset(self):
        name = self.request.GET.get('name')
        if name:
            self.queryset = self.queryset.filter(name__startswith=name)
        servstar = self.request.GET.get('servstar')
        if servstar:
            self.queryset = self.queryset.filter(servstar__gte=servstar)
        if self.action == 'list':
            self.queryset = self.queryset.only('name', 'tel', 'servstar')
        else:
            self.queryset = self.queryset.prefetch_related(
                Prefetch('estates',
                         queryset=Estate.objects.all().only('name').order_by('-hot'))
            )
        return self.queryset.order_by('-servstar')

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return AgentCreateSerializer
        return AgentDetailSerializer if self.action == 'retrieve' \
            else AgentSimpleSerializer


@method_decorator(decorator=cache_page(timeout=86400), name='list')
@method_decorator(decorator=cache_page(timeout=86400), name='retrieve')
class HouseTypeViewSet(ModelViewSet):
    """户型视图集"""
    queryset = HouseType.objects.all()
    serializer_class = HouseTypeSerializer
    pagination_class = None


@method_decorator(decorator=cache_page(timeout=3600), name='list')
class TagViewSet(ModelViewSet):
    """房源标签视图集"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


@method_decorator(decorator=cache_page(timeout=300), name='list')
@method_decorator(decorator=cache_page(timeout=300), name='retrieve')
class EstateViewSet(ModelViewSet):
    """楼盘视图集"""
    queryset = Estate.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = EstateFilterSet
    ordering = '-hot'
    ordering_fields = ('district', 'hot', 'name')

    # 为楼盘添加认证类。先认证用户是否登陆再做后续操作
    authentication_classes = (LoginRequiredAuthentication, )

    # 为楼盘添加授权类。只有被授权用户才可对该接口操作
    permission_classes = (RbacPermission, )


    def get_queryset(self):
        if self.action == 'list':
            queryset = self.queryset.only('name')
        else:
            queryset = self.queryset \
                .defer('district__parent', 'district__ishot', 'district__intro') \
                .select_related('district')
        return queryset

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return EstateCreateSerializer
        return EstateDetailSerializer if self.action == 'retrieve' \
            else EstateSimpleSerializer


@method_decorator(decorator=cache_page(timeout=120), name='list')
@method_decorator(decorator=cache_page(timeout=300), name='retrieve')
class HouseInfoViewSet(ModelViewSet):
    """房源视图集"""
    queryset = HouseInfo.objects.all()
    serializer_class = HouseInfoDetailSerializer

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = HouseInfoFilterSet
    ordering = ('-pubdate',)
    ordering_fields = ('pubdate', 'price')

    @action(methods=('GET',), detail=True)
    def photos(self, request, pk):
        queryset = HousePhoto.objects.filter(house=self.get_object())
        return Response(HousePhotoSerializer(queryset, many=True).data)

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset \
                .only('houseid', 'title', 'area', 'floor', 'totalfloor',
                      'price', 'mainphoto', 'priceunit', 'street', 'type',
                      'district_level3__distid', 'district_level3__name') \
                .select_related('district_level3', 'type') \
                .prefetch_related('tags')
        return self.queryset \
            .defer('user', 'district_level2', 'district_level3__parent',
                   'district_level3__ishot', 'district_level3__intro',
                   'estate__district', 'estate__hot', 'estate__intro',
                   'agent__realstar', 'agent__profstar', 'agent__certificated') \
            .select_related('district_level3', 'type', 'estate', 'agent') \
            .prefetch_related('tags')

    def get_serializer_class(self):
        if self.action in ('create', 'update'):
            return HouseInfoCreateSerializer
        return HouseInfoDetailSerializer if self.action == 'retrieve' \
            else HouseInfoSimpleSerializer
