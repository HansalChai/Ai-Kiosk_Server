from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, Options, OptionChoice, Menu
from .serializers import CategorySerializer, MenuSerializer, OptionSerializer, OptionChoiceSerializer
from rest_framework.exceptions import AuthenticationFailed

# 카테고리 불러오기, 추가 API
class CategoryListAddView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(IsDeleted=False, owner=request.user)
        serializer = CategorySerializer(categories, many=True)
        return Response({"categories": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            raise AuthenticationFailed({"error": "INVALID_ACCESSTOKEN", "code": "AUTH-003", "message": "AccessToken이 유효하지 않습니다."})

        data = request.data.copy()
        serializer = CategorySerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Category added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 카테고리 삭제 API
class CategoryDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, category_id):
        if not request.user.is_authenticated:
            raise AuthenticationFailed({"error": "INVALID_ACCESSTOKEN", "code": "AUTH-003", "message": "AccessToken이 유효하지 않습니다."})

        try:
            category = Category.objects.get(category_id=category_id, owner=request.user)
            category.IsDeleted = True
            category.save()
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({"error": "CATEGORY_NOT_FOUND", "code": "CATEGORY-001", "message": "존재하지 않는 카테고리입니다."}, status=status.HTTP_404_NOT_FOUND)

# 카테고리 수정 API
class CategoryUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, category_id):
        if not request.user.is_authenticated:
            return Response({"error": "INVALID_ACCESSTOKEN", "code": "AUTH-003", "message": "AccessToken이 유효하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            category = Category.objects.get(category_id=category_id, owner=request.user)
            data = request.data
            serializer = CategorySerializer(category, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({"error": "CATEGORY_NOT_FOUND", "code": "CATEGORY-001", "message": "존재하지 않는 카테고리입니다."}, status=status.HTTP_404_NOT_FOUND)

# 옵션 불러오기, 추가 API
class OptionsListAddView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, category_id):
        options = Options.objects.filter(category_ID=category_id, IsDeleted=False, owner=request.user)
        serializer = OptionSerializer(options, many=True, context={'view': self})
        return Response({"options": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, category_id):
        try:
            category = Category.objects.get(category_id=category_id, IsDeleted=False, owner=request.user)
            options_data = request.data.get('options', [])
            for option_data in options_data:
                option = Options(
                    option_name=option_data['option_name'], 
                    category_ID=category,
                    owner=request.user,
                    # order_menu_ID=None if request.user.is_owner else option_data.get('order_menu_ID')
                    order_menu_ID=option_data.get('order_menu_ID') # 관리자 페이지에서 order_menu_ID 값 null 허용
                )
                option.save()
                for choice_data in option_data['choices']:
                    choice = OptionChoice(choice_name=choice_data['choice_name'], extra_cost=choice_data['extra_cost'], option=option)
                    choice.save()
            return Response({"message": "Option added successfully", "option_id": option.option_ID}, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({"error": "CATEGORY_NOT_FOUND", "code": "CATEGORY-001", "message": "존재하지 않는 카테고리입니다."}, status=status.HTTP_404_NOT_FOUND)

# 옵션 수정 API
class OptionUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, category_id, option_id):
        try:
            option = Options.objects.get(option_ID=option_id, category_ID=category_id, IsDeleted=False, owner=request.user)
            option.option_name = request.data.get('option_name', option.option_name)
            option.save()

            OptionChoice.objects.filter(option=option).delete()
            for choice_data in request.data.get('choices', []):
                choice = OptionChoice(choice_name=choice_data['choice_name'], extra_cost=choice_data['extra_cost'], option=option)
                choice.save()

            return Response({"message": "Option updated successfully", "option_id": option.option_ID}, status=status.HTTP_200_OK)
        except Options.DoesNotExist:
            return Response({"error": "OPTION_NOT_FOUND", "code": "OPTION-001", "message": "존재하지 않는 옵션입니다."}, status=status.HTTP_404_NOT_FOUND)

# 옵션 삭제 API
class OptionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, category_id, option_id):
        try:
            option = Options.objects.get(option_ID=option_id, category_ID=category_id, IsDeleted=False, owner=request.user)
            option.IsDeleted = True
            option.save()
            return Response({"message": "Option deleted successfully"}, status=status.HTTP_200_OK)
        except Options.DoesNotExist:
            return Response({"error": "OPTION_NOT_FOUND", "code": "OPTION-001", "message": "존재하지 않는 옵션입니다."}, status=status.HTTP_404_NOT_FOUND)



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