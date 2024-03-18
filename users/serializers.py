from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from api_refs.models import ReferralCode
from api_refs.utils import check_email


class UserSerializer(serializers.ModelSerializer):
    id: int
    user: User
    code: str
    email: str

    class Meta:
        model = User
        fields = ['id', 'username', "email"]


class RegisterSerializer(serializers.ModelSerializer):
    username: str
    password: str
    password2: str
    email: str

    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "password2",
            "email",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    @staticmethod
    def validate_email(email: str) -> str:

        if not check_email(email):
            raise serializers.ValidationError('Не рабочий email')
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Пользователь с таким email уже существует"})

        return email

    def validate(self, attrs: dict):
        password = attrs['password']
        password2 = attrs['password2']

        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})

        return attrs

    def create(self, validated_data: dict) -> User:
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


class RegistrationWithReferralSerializer(serializers.ModelSerializer):
    username: str
    email: str
    password: str
    referral_code: str = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'referral_code')
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_referral_code(value: str) -> str:
        if value:
            try:
                referral_code = ReferralCode.objects.get(code=value, expiration_date__gt=timezone.now())
            except ReferralCode.DoesNotExist:
                raise serializers.ValidationError("Неправильный реферальный код")
        else:
            raise serializers.ValidationError("Введите реферальный код")
        return value
