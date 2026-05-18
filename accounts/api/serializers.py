from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    Expects fullname, email, password, and repeated_password.
    Creates a new user after successful validation,
    using the email address as the username.
    """

    fullname = serializers.CharField(max_length=50)
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(write_only=True)
    repeated_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['fullname', 'email',
                  'password', 'repeated_password']

    def validate_email(self, value):
        """Checks if the email address already exists in the database."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists.")
        return value

    def validate(self, data):
        """Ensures that password and repeated_password match."""
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError("Password does not match.")
        return data

    def create(self, validated_data):
        """
        Creates a new user from the validated data.

        repeated_password is removed before creation,
        as it is only needed for validation.
        """
        repeated_password = validated_data.pop('repeated_password')
        username = validated_data['email']
        return User.objects.create_user(
            username=username,
            email=validated_data['email'],
            password=validated_data['password'],
            fullname=validated_data['fullname']
        )


class LoginSerializer(serializers.ModelSerializer):
    """
    Serializer for user login.

    Expects email and password, checks the credentials,
    and returns the validated data.
    """

    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        """
        Checks if a user with the given email exists
        and if the password is correct.
        """
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("User doesn't exist")

        if user.check_password(data['password']):
            return data
        else:
            raise serializers.ValidationError("password isn't right")
