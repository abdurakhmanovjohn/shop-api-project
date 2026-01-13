from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('email',)

  def create(self, validated_data):
    return User.objects.create(email=validated_data['email'])


class VerifyEmailSerializer(serializers.Serializer):
  email = serializers.EmailField()
  code = serializers.CharField(max_length=6)


class ProfileCreateSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True)

  class Meta:
    model = User
    fields = ('full_name', 'username', 'password', 'avatar')

  def validate_password(self, value):
    validate_password(value)
    return value

  def update(self, instance, validated_data):
    instance.full_name = validated_data['full_name']
    instance.username = validated_data['username']
    instance.avatar = validated_data.get('avatar')
    instance.set_password(validated_data['password'])
    instance.save()
    return instance


class ProfileUpdateSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=False)

  class Meta:
    model = User
    fields = ('full_name', 'username', 'password', 'avatar')

  def update(self, instance, validated_data):
    if 'full_name' in validated_data:
      instance.full_name = validated_data['full_name']

    if 'username' in validated_data:
      instance.username = validated_data['username']

    if 'avatar' in validated_data:
      instance.avatar = validated_data['avatar']

    if 'password' in validated_data:
      validate_password(validated_data['password'])
      instance.set_password(validated_data['password'])

    instance.save()
    return instance


class ProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'email', 'username', 'full_name', 'avatar')


# class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
#   username_field = 'email'

#   def validate(self, attrs):
#     data = super().validate(attrs)

#     if not self.user.is_email_verified:
#       raise serializers.ValidationError("Email not verified")

#     if not self.user.has_usable_password():
#       raise serializers.ValidationError("Profile not completed")

#     return data

class EmailOrUsernameTokenObtainPairSerializer(TokenObtainPairSerializer):
  username_field = "email"

  def validate(self, attrs):
    identifier = attrs.get("email")
    password = attrs.get("password")

    if not identifier or not password:
      raise serializers.ValidationError(
        "Email or username and password are required"
      )

    try:
      user = User.objects.get(email=identifier)
    except User.DoesNotExist:
      try:
        user = User.objects.get(username=identifier)
      except User.DoesNotExist:
        raise serializers.ValidationError("Invalid credentials")

    if not user.check_password(password):
      raise serializers.ValidationError("Invalid credentials")

    if not user.is_email_verified:
      raise serializers.ValidationError("Email not verified")

    refresh = self.get_token(user)

    return {
      "refresh": str(refresh),
      "access": str(refresh.access_token),
    }
