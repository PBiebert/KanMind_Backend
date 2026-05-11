from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from accounts.api.serializers import RegistrationSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Nimmt die vom Frontend gesendeten Registrierungsdaten entgegen und übergibt sie an den Serializer
        serializer = RegistrationSerializer(data=request.data)

        # Prüft, ob die Daten gültig sind (Feldregeln, eigene Validierung)
        if serializer.is_valid():
            # Legt den User an (ruft create() im Serializer auf)
            # Der Variablenname (z.B. saved_account) ist frei wählbar – z.B. auch banane = serializer.save()
            saved_account = serializer.save()
            # Erstellt ein Auth-Token für den neuen User
            token, created = Token.objects.get_or_create(user=saved_account)
            # Antwortdaten für das Frontend (Token und Userdaten)
            data = {
                'token': token.key,
                'fullname': saved_account.username,
                'email': saved_account.email,
                'user_id': saved_account.id
            }

            return Response(data, status=201)
        else:
            # Gibt die Validierungsfehler zurück, falls die Daten ungültig sind
            data = serializer.errors

        # Antwort an den Client (immer als JSON)
            return Response(data, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Nimmt die vom Frontend gesendeten Login-Daten entgegen und übergibt sie an den Serializer
        serializer = LoginSerializer(data=request.data)
        # Prüft, ob die Daten gültig sind (Feldregeln, eigene Validierung)
        if serializer.is_valid():
            # Holt den User anhand der validierten E-Mail
            user = User.objects.get(email=serializer.validated_data['email'])
            # Erstellt oder holt das Auth-Token für den User
            token, created = Token.objects.get_or_create(user=user)
            # Antwortdaten für das Frontend (Token und Userdaten)
            data = {
                "token": token.key,
                "fullname": user.username,
                "email": user.email,
                "user_id": user.id
            }
            # Gibt die Antwort mit Status 200 zurück
            return Response(data)
        else:
            # Gibt die Validierungsfehler zurück, falls die Daten ungültig sind
            return Response(serializer.errors, status=400)
