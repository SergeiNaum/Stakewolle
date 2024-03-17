from django.contrib.auth import get_user_model
from rest_framework import serializers
from api_refs.models import ReferralCode, Referral


class UserForRefsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'date_joined')


class ReferralCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralCode
        fields = ('id', 'user', 'code', 'expiration_date')
        read_only_fields = ('id', 'user', 'code', 'expiration_date')


class ReferralSerializer(serializers.ModelSerializer):
    referrer = UserForRefsSerializer(read_only=True)
    referral_user = UserForRefsSerializer(read_only=True)

    class Meta:
        model = Referral
        fields = ('referrer', 'referral_user')


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ReferrerWithReferralsSerializer(serializers.ModelSerializer):
    referrals = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'date_joined', 'referrals')

    def get_referrals(self, obj):
        referrals = Referral.objects.filter(referrer=obj)
        referral_users = [referral.referral_user for referral in referrals]
        return UserForRefsSerializer(referral_users, many=True).data