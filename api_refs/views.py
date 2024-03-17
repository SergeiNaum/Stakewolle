from typing import Optional, Any, List

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import serializers

from django.utils import timezone
from django.contrib.auth.models import User

from drf_spectacular.utils import extend_schema


from api_refs.models import ReferralCode, Referral
from api_refs.serializers import ReferralCodeSerializer, EmailSerializer, ReferralSerializer, ReferrerWithReferralsSerializer
from api_refs.tasks import create_referral_code_task, delete_referral_code_task, get_referral_list


@extend_schema(
    tags=['Referral Codes'],
    summary='Create a new referral code for the user and show referal code'
)
class ReferralCodeCreateView(generics.CreateAPIView):
    serializer_class = ReferralCodeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        user: User = request.user
        active_referral_code: Optional[ReferralCode] = ReferralCode.objects.filter(user=user, expiration_date__gt=timezone.now()).first()
        if active_referral_code:
            return Response({"detail": "У пользователя уже существует активный реферальный код."},
                            status=status.HTTP_400_BAD_REQUEST)

        task = create_referral_code_task.delay(user.id)

        response_data: dict = {
            "message": "Реферальный код создан",
            "task_id": task.id
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)


@extend_schema(
    tags=['Referral Codes'],
    summary='Destroy a user\'s referral code'
)
class ReferralCodeDestroyView(generics.DestroyAPIView):
    serializer_class = ReferralCodeSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        user: User = request.user
        active_referral_code: Optional[ReferralCode] = ReferralCode.objects.filter(user=user, expiration_date__gt=timezone.now()).first()

        if active_referral_code:
            task = delete_referral_code_task.delay(active_referral_code.id)
            response_data: dict = {
                "message": "Реферальный код удалён",
                "task_id": task.id
            }
            return Response(response_data, status=status.HTTP_202_ACCEPTED)
        return Response({"error": "Реферальный код не найден"}, status=status.HTTP_404_NOT_FOUND)


@extend_schema(
    tags=['Referral Codes'],
    summary='Retrieve a referral code by email'
)
class ReferralCodeByEmailView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            return Response(serializer.validated_data)
        except serializers.ValidationError as e:
            return Response({"errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
    tags=['Referral Codes'],
    summary='Show referal code for authenticated user'
)
class ShowUserReferalCode(generics.ListAPIView):
    serializer_class = ReferralCodeSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> List[ReferralCode]:
        user: User = self.request.user
        return ReferralCode.objects.filter(user=user)


@extend_schema(
    tags=['Referrals'],
    summary='Show all referrals for current is authenticated user '
)
class ReferralListView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer

    @staticmethod
    def get(request: Request, *args: Any, **kwargs: Any) -> Response:
        user: User = request.user
        referrer_id: int = user.id
        referral_list_task = get_referral_list.delay(referrer_id)

        serializer: ReferrerWithReferralsSerializer = ReferrerWithReferralsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
