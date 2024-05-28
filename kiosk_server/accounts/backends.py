from django.contrib.auth.backends import ModelBackend
from .models import CustomUser
from rest_framework.response import Response, status


class CustomUserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
            # IsDeleted가 True인 경우 None을 반환하여 로그인을 방지하도록 함
            if user.IsDeleted:
                Response({'message': '존재하지 않는 프로필입니다.'}, status=status.HTTP_400_BAD_REQUEST)
                return None
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        except CustomUser.DoesNotExist:
            CustomUser().set_password(password)
        return None
