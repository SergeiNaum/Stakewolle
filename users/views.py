from typing import Any

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from drf_spectacular.utils import extend_schema

from users.serializers import RegisterSerializer, RegistrationWithReferralSerializer
from api_refs.tasks import register_user, register_user_referral


@extend_schema(
    tags=['Registration'],
    summary='Registration new user by username, password, password2, email'
)
class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        task_create = register_user.delay(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        # enrich_user_data.delay(user.email)  # Hypothetical launch of email data enrichment

        response_data: dict = {
            "message": "Пользователь успешно зарегистрирован",
            "task_id": task_create.id
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)


@extend_schema(
    tags=['Registration'],
    summary='Registration new referer user by username, password, email, referral_code'
)
class RegisterWithReferralView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationWithReferralSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        task = register_user_referral.delay(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            validated_data.get('referral_code')
        )

        response_data: dict = {
            "message": "Регистрация пользователя по реферальной ссылке завершена",
            "task_id": task.id
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)
