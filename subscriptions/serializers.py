from rest_framework import serializers
from .models import Package, Subscription


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['title', 'sku', 'price', 'duration', 'created_time']


class SubscriptionSerializer(serializers.ModelSerializer):
    package = PackageSerializer()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ['package', 'user', 'created_time', 'expire_time']

    def get_user(self, obj):
        return obj.user.username