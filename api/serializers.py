from rest_framework import serializers
from common.models import District


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