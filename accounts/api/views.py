from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.api.serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            saved_account = serializer.save()
            token, created = Token.objects.get_or_create(user=saved_account)
            data = {
                'token': token.key,
                'fullname': saved_account.fullname,
                'email': saved_account.email,
                'user_id': saved_account.id
            }

            return Response(data, status=201)
        else:
            data = serializer.errors

            return Response(data, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.validated_data['email'])
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": token.key,
                "fullname": user.username,
                "email": user.email,
                "user_id": user.id
            }
            return Response(data)
        else:
            return Response(serializer.errors, status=400)
