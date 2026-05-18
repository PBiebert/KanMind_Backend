from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.api.serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.validators import validate_email

User = get_user_model()


class RegistrationView(APIView):
    """
    API view for user registration.

    Accessible without authentication (AllowAny).
    On success, returns a token along with the user's details.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests to register a new user.

        Validates the incoming data using RegistrationSerializer.
        On success (201): returns token, fullname, email, and user_id.
        On failure (400): returns validation errors.
        """
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
    """
    API view for user login.

    Accessible without authentication (AllowAny).
    Authenticates the user via email and password and returns a token.
    """

    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handles POST requests to log in a user.

        Validates credentials using LoginSerializer.
        On success (200): returns token, fullname, email, and user_id.
        On failure (400): returns validation errors.
        """
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


class FindUserView(APIView):
    """
    API view to look up a user by email address.

    Requires authentication. Accepts the email as a query parameter.
    """

    def get(self, request):
        """
        Handles GET requests to find a user by email.

        Query parameter: email
        On success (200): returns id, email, and fullname of the user.
        On not found (404): returns an error message.
        On invalid input (400): returns a format error.
        """
        email = request.query_params.get('email')
        try:
            validate_email(email)
            user = User.objects.filter(email=email).first()
            if user != None:
                data = {
                    'id': user.id,
                    "email": user.email,
                    "fullname": user.fullname,
                }
                return Response(data, status=200)
            else:
                return Response({'detail': 'E-mail not found'}, status=404)
        except:
            return Response({'detail': 'Invalid request. The email address is missing or has an incorrect format'}, status=400)
