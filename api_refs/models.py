import datetime

from django.contrib.auth.models import User
from django.db import models


class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(max_length=10, unique=True)
    expiration_date = models.DateTimeField()


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referral_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')


