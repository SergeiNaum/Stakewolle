import datetime
import string
import random

# import clearbit
from typing import List

from django.utils import timezone
from django.contrib.auth.models import User
from celery import shared_task


from api_refs.models import ReferralCode, Referral


def generate_referral_code(
    size: int = 8, chars: str = string.ascii_uppercase + string.digits
) -> str:
    return "".join(random.choice(chars) for _ in range(size))


@shared_task
def create_referral_code_task(user_id: int) -> str:
    user: User = User.objects.get(id=user_id)
    code: str = generate_referral_code()
    expiration_date: datetime = timezone.now() + timezone.timedelta(days=30)

    referral_code: ReferralCode = ReferralCode(
        user=user, code=code, expiration_date=expiration_date
    )
    referral_code.save()
    return referral_code.code


@shared_task
def delete_referral_code_task(referral_code_id: int) -> dict:
    try:
        referral_code: ReferralCode = ReferralCode.objects.get(id=referral_code_id)
        referral_code.delete()
        return {"message": "Реферальный код успешно удален"}
    except ReferralCode.DoesNotExist:
        return {"error": "Реферальный код не найден"}


@shared_task
def register_user_referral(
    username: str, email: str, password: str, referral_code: str = None
) -> int:
    user: User = User.objects.create_user(
        username=username, email=email, password=password
    )

    if referral_code:
        try:
            referrer_code: List[ReferralCode] | None = ReferralCode.objects.get(
                code=referral_code, expiration_date__gt=timezone.now()
            )
            Referral.objects.create(referrer=referrer_code.user, referral_user=user)
        except ReferralCode.DoesNotExist:
            pass

    return user.pk


@shared_task
def get_referral_list(referrer_id: int) -> list:

    referrer: User = User.objects.get(id=referrer_id)
    referrals: List[Referral] = Referral.objects.filter(referral_user=referrer)
    if referrals:
        return [referral.referral_user.username for referral in referrals]


@shared_task
def register_user(username: str, email: str, password: str) -> int:
    user = User.objects.create_user(username=username, email=email, password=password)
    return user.pk


# @shared_task(bind=True)
# def enrich_user_data(email: str) -> dict:
# """
# Версия пакета clearbit несовместима современными версиями языка python поэтому я ее не установил
# Понижать версию языка я не стал, ввиду возможных проблем совместимости в других сторонних пакетах
# Это пример кода который мог бы быть исполнен если бы пакет clearbit поддерживал python 3.10 и выше
# во views код вызывающий отложенную задачу celery так же закомментирован
# """
#     clearbit.key: str = 'sk_1f8d2e16fffd45e6c29d20b2b5e9003f'
#     try:
#         clearbit_data = clearbit.Enrichment.find(email=email, stream=True)
#         if clearbit_data and 'company' in clearbit_data:
#             user: User = User.objects.get(email=email)
#             user.company_name = clearbit_data['company'].get('name', '')
#             user.company_domain = clearbit_data['company'].get('domain', '')
#             user.save()
#             return clearbit_data
#         else:
#             return {"error": "No company data available for this user."}
#     except (ObjectDoesNotExist, KeyError) as e:
#         return {"error": str(e)}clearbit
