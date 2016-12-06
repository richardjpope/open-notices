from django.contrib.auth.backends import ModelBackend
from core.models import User

class UserBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username.lower())
            if user.check_password(password):
                return user
            else:
                return None
        except User.DoesNotExist:
            return None