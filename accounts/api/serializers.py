from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    # Feld 'fullname' wird im JSON erwartet und auf das Model-Feld 'username' gemappt
    fullname = serializers.CharField(max_length=50, source='username')
    # Feld 'email' wird im JSON erwartet und auf das Model-Feld 'email' gemappt
    email = serializers.EmailField(max_length=50)
    # Passwort-Felder werden nur zum Schreiben verwendet (nicht ausgegeben)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        # 'User' ist das Standard-Benutzermodell aus django.contrib.auth.models
        # 'fields' gibt an, welche Feldnamen im JSON vom Frontend erwartet werden und wie sie gemappt werden
        # (z.B. fullname -> username im Model, siehe source-Attribut im Serializer)
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']

    def validate_email(self, value):
        # Prüft, ob die E-Mail bereits existiert.
        # Wenn ja, wird eine Fehlermeldung ausgelöst (ValidationError).
        # Wenn nicht, wird der Wert zurückgegeben und die Validierung ist bestanden.
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value

    def validate_fullname(self, value):
        # Prüft, ob der Benutzername (fullname/username) bereits existiert.
        # Wenn ja, wird eine Fehlermeldung ausgelöst (ValidationError).
        # Wenn nicht, wird der Wert zurückgegeben und die Validierung ist bestanden.
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Fullname already exists.")
        return value

    def validate(self, data):
        # Diese Methode prüft, ob die beiden Passwörter übereinstimmen.
        # Wenn sie unterschiedlich sind, wird eine Fehlermeldung ausgelöst (ValidationError).
        # Wenn alles passt, werden die validierten Daten zurückgegeben, damit DRF weiterarbeiten kann.
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Password does not match.")
        return data

    def create(self, validated_data):
        # Hier werden nur die Felder übergeben, die das User-Modell wirklich erwartet.
        # 'repeated_password' wird ignoriert, da es nicht im User-Modell existiert.
        # Das Mapping von fullname -> username übernimmt DRF automatisch durch source='username'.
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
