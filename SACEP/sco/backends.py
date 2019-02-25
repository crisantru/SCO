from sco.models import User
from django.contrib.auth.hashers import check_password

class CustomUserAuthentication(object):
    def authenticate(self, username=None, password=None):
        print("entro a backeds authenticate")
        try:
            user = User.objects.get(email=username)
            if(user.check_password(password)):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        print("entro a backeds get_user")
        try:
            user= User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None
