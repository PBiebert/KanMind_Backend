

from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token


class RegistrationView(APIView):
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
