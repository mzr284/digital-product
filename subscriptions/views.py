from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils import timezone
from rest_framework.response import Response
from .serializers import PackageSerializer, SubscriptionSerializer
from .models import Package, Subscription


class PackageView(APIView):

    def get(self, request):
        packages = Package.objects.filter(is_enable=True)
        serial = PackageSerializer(packages, many=True)
        return Response(serial.data)


class SubscriptionView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        subscription = Subscription.objects.filter(user=request.user, expire_time__gt=timezone.now())
        serialize = SubscriptionSerializer(subscription, many=True)
        return Response(serialize.data)
