import uuid
import requests
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from rest_framework.views import APIView
from .serializers import GateWaySerializer
from .models import Gateway, Payment
from subscriptions.models import Package, Subscription
from rest_framework import status


class GatewayView(APIView):

    def get(self, request):
        gateways = Gateway.objects.filter(is_enable=True)
        serial = GateWaySerializer(gateways, many=True, context={'request': request})
        return Response(serial.data)


class PaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        package_id = request.query_params.get("package")
        gateway_id = request.query_params.get("gateway")

        try:
            package = Package.objects.get(pk=package_id, is_enable=True)
            gateway = Gateway.objects.get(pk=gateway_id, is_enable=True)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        payment = Payment.objects.create(
            user=request.user,
            package=package,
            gateway=gateway,
            price=package.price,
            phone_number=request.user.phone_number,
            token=str(uuid.uuid4())
        )

        return Response({'token': payment.token, 'callback_url': 'https://my-site.com/payments/pay/'})


    def post(self, request):
        token = request.data.get('token')
        stat = request.data.get('status')

        try:
            payment = Payment.objects.get(token=token)
        except Payment.DoesNotExist:
            return Response({'error': 'payment with this token not exists'}, status=status.HTTP_404_NOT_FOUND)

        if stat != 10:
            payment.status = payment.STATUS_CANCELED
            payment.save()
            return Response({'message': 'your payment canceled'}, status=status.HTTP_400_BAD_REQUEST)

        r = requests.post('bank_varify_url', data={})
        if r.status_code // 100 != 2:
            payment.status = payment.STATUS_ERROR
            payment.save()
            return Response({'message': "your payment don't successfully paid"},
                            status=status.HTTP_417_EXPECTATION_FAILED)

        payment.status = payment.STATUS_PAID
        payment.save()

        subscription = Subscription.objects.create(user=request.user, package=payment.package,
                                     expire_time=timezone.now() + timezone.timedelta(days=payment.package.duration.day))

        return Response(status=status.HTTP_200_OK)