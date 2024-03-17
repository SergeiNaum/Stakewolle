from typing import Dict, Any

from rest_framework import serializers
from django.contrib.auth.models import User
from api_refs.tasks import create_referral_task
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
    referral_code = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'referral_code')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        referral_code = validated_data.pop('referral_code', None)

        if referral_code:
            user = User.objects.create_user(**validated_data)
            create_referral_task.delay(referral_code, user.id)
            return user
        else:
            raise serializers.ValidationError({"error": "Введите реферальный код"})
