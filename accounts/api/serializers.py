from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email',
                  'password', 'repeated_password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Password does not match.")
        return data

    def create(self, validated_data):
        repeated_password = validated_data.pop('repeated_password')
        username = validated_data['email']
        return User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname']
        )


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

        if user.check_password(data['password']):
            return data
        else:
            raise serializers.ValidationError("password isn't right")
