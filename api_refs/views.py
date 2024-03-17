from typing import Optional

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request


from django.utils import timezone
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema


from api_refs.models import ReferralCode, Referral
from api_refs.serializers import ReferralCodeSerializer, EmailSerializer, ReferralSerializer, UserForRefsSerializer, \
    ReferrerWithReferralsSerializer
from api_refs.tasks import create_referral_code_task, delete_referral_code_task, get_referral_list


@extend_schema(
    tags=['Referral Codes'],
    summary='Create a new referral code for the user and show referal code'
)
class ReferralCodeCreateView(generics.CreateAPIView):
    serializer_class = ReferralCodeSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request: Request, *args, **kwargs) -> Response:
        user = request.user
        active_referral_code: Optional[ReferralCode] = ReferralCode.objects.filter(user=user, expiration_date__gt=timezone.now()).first()

        if active_referral_code:
            return Response({"detail": "У пользователя уже существует активный реферальный код."},
                            status=status.HTTP_400_BAD_REQUEST)

        task = create_referral_code_task.delay(user.id)
        return Response({"Создаём реф код task_id": task.id}, status=status.HTTP_202_ACCEPTED)


@extend_schema(
    tags=['Referral Codes'],
    summary='Destroy a user\'s referral code'
)
class ReferralCodeDestroyView(generics.DestroyAPIView):
    serializer_class = ReferralCodeSerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        user = request.user
        active_referral_code: Optional[ReferralCode] = ReferralCode.objects.filter(user=user, expiration_date__gt=timezone.now()).first()

        if active_referral_code:
            referral_code_id = active_referral_code.id
            task = delete_referral_code_task.delay(referral_code_id)
            return Response({"message": f"Задача Выполнена {task}, реф.код удалён"},
                            status=status.HTTP_205_RESET_CONTENT)
        return Response({"error": "Реферальный код не найден"},
                            status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    tags=['Referral Codes'],
    summary='Retrieve a referral code by email'
)
class ReferralCodeByEmailView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args, **kwargs) -> Response:

        user = get_user_model()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email: str = serializer.validated_data['email']

        try:
            referrer_user= user.objects.get(email=email)
        except user.DoesNotExist:
            return Response({"detail": "Пользователь с таким email не найден."},
                            status=status.HTTP_404_NOT_FOUND)

        referral_code: Optional[ReferralCode] = ReferralCode.objects.filter(user=referrer_user, expiration_date__gt=timezone.now()).first()

        if not referral_code:
            return Response({"detail": "У пользователя нет активного реферального кода."},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({"referral_code": referral_code.code})


@extend_schema(
    tags=['Referral Codes'],
    summary='Show referal code for authenticated user'
)
class ShowUserReferalCode(generics.ListAPIView):
    serializer_class = ReferralCodeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return ReferralCode.objects.filter(user=user)


@extend_schema(
    tags=['Referrals'],
    summary='Show all referrals for current is authenticated user '
)
class ReferralListView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

    def get(self, request):
        user = request.user
        referrer_id = user.id
        referral_list_task = get_referral_list.delay(referrer_id)

        serializer = ReferrerWithReferralsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
