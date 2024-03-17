from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils import timezone

from api_refs.models import ReferralCode
from api_refs.utils import check_email


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', "email"]


class RegisterSerializer(serializers.ModelSerializer):

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
    def validate_email(email):

        if not check_email(email):
            raise serializers.ValidationError('Не рабочий email')

        return email

    def create(self, validated_data):
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        password2 = validated_data["password2"]
        if password != password2:
            raise serializers.ValidationError({"password": "Пароли не совпадают"})
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


class RegistrationWithReferralSerializer(serializers.ModelSerializer):
    referral_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'referral_code')
        extra_kwargs = {'password': {'write_only': True}}

    @staticmethod
    def validate_referral_code(value):
        if value:
            try:
                referral_code = ReferralCode.objects.get(code=value, expiration_date__gt=timezone.now())
            except ReferralCode.DoesNotExist:
                raise serializers.ValidationError("Неправильный реферальный код")
        else:
            raise serializers.ValidationError("Введите реферальный код")
        return value
