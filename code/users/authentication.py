from django.contrib.auth.backends import ModelBackend
from users.models import User

class PhoneBackend(ModelBackend):
    def authenticate(self, request, phone=None, **kwargs):
        try:
            return User.objects.get(phone=phone)
        except User.DoesNotExist:
            return None
