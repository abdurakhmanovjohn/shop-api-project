from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser, EmailVerification
from .serializers import (
  RegisterSerializer,
  VerifyEmailSerializer,
  ProfileCreateSerializer,
  ProfileUpdateSerializer,
  ProfileSerializer,
  # EmailTokenObtainPairSerializer,
  EmailOrUsernameTokenObtainPairSerializer,
)


class RegisterView(APIView):
  permission_classes = [AllowAny]

  def post(self, request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()

    verification, _ = EmailVerification.objects.get_or_create(user=user)

    send_mail(
      subject="Your verification code",
      message=f"Your verification code is: {verification.code}",
      from_email=settings.EMAIL_HOST_USER,
      recipient_list=[user.email],
    )

    return Response(
      {"detail": "Verification code sent to email"},
      status=status.HTTP_201_CREATED
    )


class VerifyEmailView(APIView):
  permission_classes = [AllowAny]

  def post(self, request):
    serializer = VerifyEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    email = serializer.validated_data['email']
    code = serializer.validated_data['code']

    try:
      verification = EmailVerification.objects.get(
        user__email=email,
        code=code
      )
    except EmailVerification.DoesNotExist:
      return Response({"error": "Invalid code"}, status=400)

    user = verification.user
    user.is_email_verified = True
    user.save()
    verification.delete()

    return Response({"detail": "Email verified"})


class ProfileCreateView(APIView):
  permission_classes = [AllowAny]

  def patch(self, request):
    email = request.data.get("email")

    if not email:
      return Response({"error": "Email required"}, status=400)

    try:
      user = CustomUser.objects.get(email=email, is_email_verified=True)
    except CustomUser.DoesNotExist:
      return Response({"error": "Email not verified"}, status=403)

    serializer = ProfileCreateSerializer(user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return Response({"detail": "Profile created successfully"})


class ProfileUpdateView(APIView):
  permission_classes = [IsAuthenticated]

  def patch(self, request):
    serializer = ProfileUpdateSerializer(
      request.user,
      data=request.data,
      partial=True
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    print("VALIDATED DATA:", serializer.validated_data)

    return Response({"detail": "Profile updated"})


class ProfileView(RetrieveAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = ProfileSerializer

  def get_object(self):
    return self.request.user


class LoginView(TokenObtainPairView):
  serializer_class = EmailOrUsernameTokenObtainPairSerializer


class LogoutView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    token = RefreshToken(request.data.get("refresh"))
    token.blacklist()
    return Response({"detail": "Logged out"})


class PasswordResetView(APIView):
  permission_classes = [IsAuthenticated]

  def patch(self, request):
    user = request.user
    if not user.check_password(request.data.get("old_password")):
      return Response({"error": "Wrong password"}, status=400)

    validate_password(request.data.get("new_password"))
    user.set_password(request.data.get("new_password"))
    user.save()
    return Response({"detail": "Password changed"})
