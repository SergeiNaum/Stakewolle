import datetime
from typing import Union, Dict, Optional, List

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import serializers
from api_refs.models import ReferralCode, Referral

UserModel = get_user_model()


class UserForRefsSerializer(serializers.ModelSerializer):
    username: str
    email: str
    date_joined: datetime

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "date_joined")


class ReferralCodeSerializer(serializers.ModelSerializer):
    id: int
    user: UserModel
    code: str
    expiration_date: datetime

    class Meta:
        model = ReferralCode
        fields = ("id", "user", "code", "expiration_date")
        read_only_fields = ("id", "user", "code", "expiration_date")


class ReferralSerializer(serializers.ModelSerializer):
    referrer: Referral = UserForRefsSerializer(read_only=True)
    referral_user: Referral = UserForRefsSerializer(read_only=True)

    class Meta:
        model = Referral
        fields = ("referrer", "referral_user")


class EmailSerializer(serializers.Serializer):
    email: str = serializers.EmailField()

    @staticmethod
    def validate_email(value: str) -> Union[Dict[str, str], None]:
        try:
            user: UserModel = get_user_model()
            user: UserModel = user.objects.get(email=value)
        except user.DoesNotExist:
            raise serializers.ValidationError(
                {"errors": "Пользователь с таким email не найден."}
            )

        referral_code: Optional[ReferralCode] = ReferralCode.objects.filter(
            user=user, expiration_date__gt=timezone.now()
        ).first()
        if referral_code:
            return {"referral_code": referral_code.code}
        else:
            raise serializers.ValidationError(
                {"errors": "У пользователя нет активного реферального кода."}
            )


class ReferrerWithReferralsSerializer(serializers.ModelSerializer):
    referrals: List[UserForRefsSerializer] = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "date_joined", "referrals")

    @staticmethod
    def get_referrals(obj) -> List[UserForRefsSerializer]:
        referrals: Optional[Referral] = Referral.objects.filter(referrer=obj)
        referral_users: List[Referral] = [
            referral.referral_user for referral in referrals
        ]
        return UserForRefsSerializer(referral_users, many=True).data
