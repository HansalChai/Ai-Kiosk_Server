# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    
    def post(self, request):
        user = request.user
        user.IsDeleted = True
        user.save()
        return Response({'message': '사용자 프로필이 삭제되었습니다.'}, status=status.HTTP_200_OK)
