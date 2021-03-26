from rest_framework import serializers
from common.models import District


class DistrictSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = ('distid', 'name')
