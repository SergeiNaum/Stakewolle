from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from users.serializers import UserSerializer, RegisterSerializer, RegistrationWithReferralSerializer


@extend_schema(
    tags=['Registration'],
    summary='Registration new user by username, password, password2, email'
)
class RegisterView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })


@extend_schema(
    tags=['Registration'],
    summary='Registration new referer user by username, password, email, referral_code'
)
class RegisterWithReferralView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationWithReferralSerializer

