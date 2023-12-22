from .services import StatusDataClass
from rest_framework import serializers
from src.apps.user.serializers import UserSerializer


class StatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()
    date_published = serializers.DateTimeField(read_only=True)
    user = UserSerializer(read_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        return StatusDataClass(**data)
