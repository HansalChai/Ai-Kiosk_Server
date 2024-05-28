# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import CustomUser
from .serializers import CustomUserSerializer

class CustomUserDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
