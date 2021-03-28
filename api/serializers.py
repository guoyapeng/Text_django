from rest_framework import serializers
from common.models import District, Agent, Estate, HouseType


class DistrictSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('distid', 'name')


class DistrictDetailSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        exclude = ('parent',)


class DistrictDetailSerializerd(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField()

    @staticmethod
    def get_cities(district):
        quseryset = District.objects.filter(parent=district).only('name')
        return DistrictSimpleSerializers(quseryset, many=True).data

    class Meta:
        model = District
        exclude = ('parent',)


class AgentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('agentid', 'name', 'tel', 'servstar')


class AgentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        exclude = ('estates',)


class AgentDetailSerializer(serializers.ModelSerializer):
    estates = serializers.SerializerMethodField()

    @staticmethod
    def get_estates(agent):
        queryset = agent.estates.all()[:5]  # .only('name') 注意：解决1+N查询问题后，序列化器这里不能再做任何处理了
        return EstateSimpleSerializer(queryset, many=True).data

    class Meta:
        model = Agent
        fields = '__all__'


class EstateSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        fields = ('estateid', 'name')


class EstateDetailSerializer(serializers.ModelSerializer):
    district = DistrictSimpleSerializers()

    class Meta:
        model = Estate
        fields = '__all__'


class HouseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HouseType
        fields = '__all__'
