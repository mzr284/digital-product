import uuid
import random
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User, Device
from django.core.cache import cache



class RegisterView(APIView):

    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
            return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            pass

        code = random.randint(10000, 99999)
        cache.set(str(phone_number), code, 2 * 60)
        return Response({"code": code})


class GetTokenView(APIView):

    def post(self, request):
        phone_number = request.data.get("phone_number")
        code = request.data.get("code")
        cached_code = cache.get(str(phone_number))
        if code != cached_code or cached_code is None:
            return Response({"Error": "Your code is wrong!"}, status=status.HTTP_403_FORBIDDEN)

        user = User.objects.create_user(phone_number=phone_number)
        device = Device.objects.create(user=user)

        token = str(uuid.uuid4())
        return Response({"detail": "registering is successfully, next you must log in with this token", "token": token})
