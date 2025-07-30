from rest_framework import serializers
from .models import Gateway

class GateWaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ['id', 'title', 'is_enable']

