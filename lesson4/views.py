from datetime import datetime, timedelta
from random import randint

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lesson4.models import ConfirmationCode


class RegisterApiView(APIView):
    def post(self, request):
        username = request.data.get('username')  # +996700012122
        password = request.data.get('password')  # random
        user = User.objects.create_user(username=username,
                                        password=password,
                                        is_active=False)
        user.save()
        code = randint(100000, 999999)  # 1111
        confirmation_code = ConfirmationCode()
        confirmation_code.code = str(code)
        confirmation_code.user = user
        confirmation_code.valid_until = datetime.now() + timedelta(minutes=20)
        confirmation_code.save()
        send_mail(subject='Code confirmation',
                  message=f'http://127.0.0.1:8000/confirm/{code}',
                  from_email=settings.EMAIL_HOST,
                  recipient_list=[username])
        # sms_send()
        return Response(status=status.HTTP_200_OK)


class ConfirmApiView(APIView):
    def post(self, request):
        code = request.data.get('code')
        codes = ConfirmationCode.objects.get(code=code,
                                             valid_until__gte=datetime.now())
        user = codes.user
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK)


class LoginApiView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'],
                            password=request.data.get('password', 'admin123'))
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={'message': 'User not found'})
        else:
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)


class ReAuth(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response(status=status.HTTP_200_OK,
                        data={
                            'username': user.username,
                            'is_active': user.is_active,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                        })
