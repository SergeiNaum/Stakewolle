from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        task = register_user.delay(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        response_data = {
            "message": "Пользователь успешно зарегистрирован",
            "task_id": task.id
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)


@extend_schema(
    tags=['Registration'],
    summary='Registration new referer user by username, password, email, referral_code'
)
class RegisterWithReferralView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationWithReferralSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        task = register_user_referral.delay(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
            validated_data.get('referral_code')
        )

        response_data = {
            "message": "Регистрация пользователя по реферальной ссылке завершена",
            "task_id": task.id
        }
        return Response(response_data, status=status.HTTP_202_ACCEPTED)