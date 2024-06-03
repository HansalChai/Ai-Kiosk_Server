from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, Menu
from .serializers import CategorySerializer, MenuSerializer
from rest_framework.exceptions import AuthenticationFailed

class CategoryListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(is_deleted=False)
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed({"error": "INVALID_ACCESSTOKEN", "code": "AUTH-003", "message": "AccessToken이 유효하지 않습니다."})

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, category_id):
        if not request.user.is_authenticated:
            raise AuthenticationFailed({"error": "INVALID_ACCESSTOKEN", "code": "AUTH-003", "message": "AccessToken이 유효하지 않습니다."})

        try:
            category = Category.objects.get(category_id=category_id)
            category.is_deleted = True
            category.save()
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "CATEGORY_NOT_FOUND", "code": "CATEGORY-001", "message": "존재하지 않는 카테고리입니다."}, status=status.HTTP_404_NOT_FOUND)


class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, category_id):
        if not request.user.is_authenticated:
            return Response({"error": "INVALID_ACCESSTOKEN", "code": "AUTH-003", "message": "AccessToken이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(category_id=category_id)
            data = request.data
            serializer = CategorySerializer(category, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "CATEGORY_NOT_FOUND", "code": "CATEGORY-001", "message": "존재하지 않는 카테고리입니다."}, status=status.HTTP_404_NOT_FOUND)
        
class MenuListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Menu.objects.filter(category_ID=category_id, IsDeleted=False)

    def perform_create(self, serializer):
        category_id = self.kwargs['category_id']
        category = Category.objects.get(pk=category_id)
        serializer.save(category_ID=category)

class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Menu.objects.filter(category_ID=category_id)
    
    def perform_destroy(self, instance):
        instance.IsDeleted = True
        instance.save()