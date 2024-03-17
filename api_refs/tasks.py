import string
import random
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.response import Response
from celery import shared_task


from api_refs.models import ReferralCode, Referral


def generate_referral_code(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


@shared_task
def create_referral_code_task(user_id):
    user = User.objects.get(id=user_id)
    code = generate_referral_code()
    expiration_date = timezone.now() + timezone.timedelta(days=30)

    referral_code = ReferralCode(user=user, code=code, expiration_date=expiration_date)
    referral_code.save()
    return referral_code.code


@shared_task
def delete_referral_code_task(referral_code_id):
    ReferralCode.objects.filter(id=referral_code_id).delete()


@shared_task
def register_user_referral(username, email, password, referral_code=None):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    if referral_code:
        try:
            referrer_code = ReferralCode.objects.get(code=referral_code, expiration_date__gt=timezone.now())
            Referral.objects.create(referrer=referrer_code.user, referral_user=user)
        except ReferralCode.DoesNotExist:
            pass

    return user.pk


@shared_task
def get_referral_list(referrer_id):

    referrer = User.objects.get(id=referrer_id)
    referrals = Referral.objects.filter(referral_user=referrer)
    if referrals:
        return [referral.referral_user.username for referral in referrals]


@shared_task
def register_user(username, email, password):
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    return user.pk
