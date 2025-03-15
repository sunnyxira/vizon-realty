from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class PhonePinAuthBackend(ModelBackend):
    def authenticate(self, request, phone=None, pin=None, **kwargs):
        try:
            user = User.objects.get(phone=phone, pin=pin)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
