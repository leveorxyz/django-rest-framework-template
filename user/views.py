from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter
from django.contrib.auth import authenticate, logout
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes

from core.views import (
    CustomListAPIView,
    CustomRetrieveAPIView,
    CustomCreateAPIView,
    CustomAPIView,
)
from core.utils import set_user_ip
from .models import User
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserSignUpSerializer,
    VerifyEmailSerializer,
    PasswordResetEmailSerializer,
    PasswordResetSerializer,
)


class UserRetrieveAPIView(CustomRetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        # Extracting data from request and validating it
        user = None
        fields = ["email", "password"]
        for field in fields:
            if field not in request.data:
                raise ValidationError(f"{field} is required")
        try:
            user: User = User.objects.get(email=request.data["email"])
            if user.check_password(request.data["password"]):
                user.is_active = True
                user.save()
        except User.DoesNotExist:
            raise ValidationError("Invalid credentials")
        serializer = UserLoginSerializer(user)

        # Checking if user is already logged in
        result = None
        if request.user.is_authenticated:
            set_user_ip(request)
            result = UserLoginSerializer(request.user).data

        # Authenticating user
        else:
            user = authenticate(
                email=request.data["email"],
                password=request.data["password"],
            )
            if not user:
                raise AuthenticationFailed()
            result = serializer.data

        # Returning token
        return Response(
            {
                "status_code": 200,
                "message": "Login successful.",
                "result": result,
            }
        )


class UserSignUpView(CustomCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny]


class LogoutView(CustomAPIView):
    http_method_names = ["post", "options"]

    def post(self, request):
        # Flushing current request session
        logout(request)
        return super().post(request=request)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        serializer = VerifyEmailSerializer(data={"token": kwargs["token"]})
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        return Response(
            {
                "status_code": 200,
                "message": "Email verified successfully.",
                "result": UserLoginSerializer(instance=validated_data["user"]).data,
            }
        )


class PasswordResetEmailView(CustomAPIView):
    permission_classes = [AllowAny]
    http_method_names = ["post", "options"]

    @extend_schema(
        request=PasswordResetEmailSerializer,
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[OpenApiExample(name="example 1", value={})],
                response=[],
            )
        },
    )
    def post(self, request):
        # Extracting data from request and validating it
        data = request.data
        serializer = PasswordResetEmailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user: User = serializer.validated_data["user"]
        user.send_password_reset_mail()
        return super().post(request=request)


class PasswordResetView(CustomAPIView):
    permission_classes = [AllowAny]
    http_method_names = ["post", "options"]

    @extend_schema(
        request=PasswordResetSerializer,
        responses={
            200: OpenApiResponse(
                description="Success.",
                examples=[OpenApiExample(name="example 1", value={})],
                response=[],
            )
        },
    )
    def post(self, request):
        # Extracting data from request and validating it
        data = request.data
        serializer = PasswordResetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        User.verify_password_reset(**validated_data)
        return super().post(request=request)
