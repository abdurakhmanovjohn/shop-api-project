from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
  path('register/', RegisterView.as_view()),
  path('verify-email/', VerifyEmailView.as_view()),

  path('profile/', ProfileView.as_view()),
  path('profile-create/', ProfileCreateView.as_view()),
  path('profile-update/', ProfileUpdateView.as_view()),
  path('profile/reset-pass/', PasswordResetView.as_view()),

  path('login/', LoginView.as_view()),
  path('logout/', LogoutView.as_view()),
  path('token/refresh/', TokenRefreshView.as_view()),
]
