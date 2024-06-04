from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, Options, OptionChoice, Menu, Order_amount, Order_menu, Order
from .serializers import CategorySerializer, MenuSerializer, OptionSerializer, OptionChoiceSerializer, OrderAmountSerializer, OrderSerializer
from rest_framework.exceptions import AuthenticationFailed

# 카테고리 불러오기, 추가 API
class CategoryListAddView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        categories = Category.objects.filter(is_deleted=False, owner_id=request.user.id)
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
            category = Category.objects.get(id=category_id, owner_id=request.user)
            category.is_deleted = True
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
            category = Category.objects.get(id=category_id, owner_id=request.user)
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
        options = Options.objects.filter(category_id=category_id, is_deleted=False)
        serializer = OptionSerializer(options, many=True, context={'view': self})
        return Response({"options": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, category_id):
        try:
            category = Category.objects.get(id=category_id, is_deleted=False, owner_id=request.user)
            options_data = request.data.get('options', [])
            for option_data in options_data:
                option = Options(
                    id = option_data.get('id'),
                    options_name=option_data['options_name'], 
                    category_id=category,
                    # order_menu_ID=None if request.user.is_owner else option_data.get('order_menu_ID')
                    # order_menu_id=option_data.get('order_menu_id') # 관리자 페이지에서 order_menu_ID 값 null 허용
                )
                option.save()
                for choice_data in option_data['choices']:
                    choice = OptionChoice(choice_name=choice_data['choice_name'], extra_cost=choice_data['extra_cost'], options_id=option)
                    choice.save()
            return Response({"message": "Option added successfully"}, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({"error": "CATEGORY_NOT_FOUND", "code": "CATEGORY-001", "message": "존재하지 않는 카테고리입니다."}, status=status.HTTP_404_NOT_FOUND)

# 옵션 수정 API
class OptionUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, category_id, option_id):
        try:
            option = Options.objects.get(id=option_id, category_id=category_id, is_deleted=False)
            option.options_name = request.data.get('options_name', option.options_name)
            option.save()

            existing_choices = {choice.id: choice for choice in option.choices.all()}
            new_choices = request.data.get('choices', [])

            for choice_data in new_choices:
                choice_id = choice_data.get('id')
                if choice_id and choice_id in existing_choices:
                    choice = existing_choices.pop(choice_id)
                    choice.choice_name = choice_data['choice_name']
                    choice.extra_cost = choice_data['extra_cost']
                    choice.save()
                else:
                    OptionChoice.objects.create(
                        choice_name=choice_data['choice_name'],
                        extra_cost=choice_data['extra_cost'],
                        options_id=option 
                    )

            for choice in existing_choices.values():
                choice.delete()

            return Response({"message": "Option updated successfully", "option_id": option.id}, status=status.HTTP_200_OK)
        except Options.DoesNotExist:
            return Response({"error": "OPTION_NOT_FOUND", "code": "OPTION-001", "message": "존재하지 않는 옵션입니다."}, status=status.HTTP_404_NOT_FOUND)
# 옵션 삭제 API
class OptionDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, category_id, option_id):
        try:
            option = Options.objects.get(id=option_id, category_id=category_id, is_deleted=False)
            option.is_deleted = True
            option.save()
            return Response({"message": "Option deleted successfully"}, status=status.HTTP_200_OK)
        except Options.DoesNotExist:
            return Response({"error": "OPTION_NOT_FOUND", "code": "OPTION-001", "message": "존재하지 않는 옵션입니다."}, status=status.HTTP_404_NOT_FOUND)



class MenuListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MenuSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Menu.objects.filter(category_id=category_id, is_deleted=False)

    def perform_create(self, serializer):
        category_id = self.kwargs['category_id']
        category = Category.objects.get(pk=category_id)
        serializer.save(category_id=category)
 
class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Menu.objects.filter(category_id=category_id)
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

class OrderAmountView(APIView):

    def post(self, request, *args, **kwargs):
        menu_id = request.data.get('menu_id')
        age_range = request.data.get('age_range')
        
        order_menus = Order_menu.objects.filter(menu_id=menu_id)
        
        if not order_menus.exists():
            return Response({"detail": "Order_menu가 비어있습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        order_amount, created = Order_amount.objects.get_or_create(menu_id=menu_id)
        
        for order_menu in order_menus:
            count = order_menu.count

            if age_range in ['0-2', '4-6', '8-12']:
                order_amount.teenager += count
            elif age_range in ['15-20', '25-32']:
                order_amount.adult += count
            elif age_range in ['38-43', '48-53']:
                order_amount.elder += count
            elif age_range == '60-100':
                order_amount.aged += count

        order_amount.save()
        
        serializer = OrderAmountSerializer(order_amount)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get(self, request, *args, **kwargs):
        menu_id = request.query_params.get('menu_id')
        order_amount = Order_amount.objects.get(menu_id=menu_id)
        serializer = OrderAmountSerializer(order_amount)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    