from rest_framework.views import APIView
from rest_framework import  viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from .models import Category, Options, OptionChoice, Menu, Order_amount, Order_menu, Order
from .serializers import CategorySerializer, MenuSerializer, OptionSerializer, OptionChoiceSerializer, OrderAmountSerializer, OrderSerializer
from rest_framework.exceptions import AuthenticationFailed

# 카테고리 관련 API
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(is_deleted=False, owner_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)

    @action(detail=True, methods=['post'], url_path='delete')
    def delete_category(self, request, pk=None):
        try:
            category = self.get_object()
            category.is_deleted = True
            category.save()
            return Response({"message": "Category deleted successfully."}, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)

# 옵션 관련 API
class OptionViewSet(viewsets.ModelViewSet):
    serializer_class = OptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Options.objects.filter(category_id=category_id, is_deleted=False)

    def perform_create(self, serializer):
        category_id = self.kwargs['category_id']
        try:
            category = Category.objects.get(id=category_id, is_deleted=False, owner_id=self.request.user)
            options_data = self.request.data.get('options', [])
            for option_data in options_data:
                option_data['category_id'] = category.id
                option = serializer.save(**option_data)
                for choice_data in option_data['choices']:
                    OptionChoice.objects.create(choice_name=choice_data['choice_name'], extra_cost=choice_data['extra_cost'], option_id=option)
            return Response({"message": "Option added successfully"}, status=status.HTTP_201_CREATED)
        except Category.DoesNotExist:
            return Response({"error": "CATEGORY_NOT_FOUND", "code": "CATEGORY-001", "message": "존재하지 않는 카테고리입니다."}, status=status.HTTP_404_NOT_FOUND)

    def perform_update(self, serializer):
        choices_data = self.request.data.pop('choices', [])
        option = serializer.save()

        for choice_data in choices_data:
            choice_id = choice_data.get('id')
            if choice_id:
                choice = OptionChoice.objects.get(id=choice_id, option_id=option)
                for attr, value in choice_data.items():
                    setattr(choice, attr, value)
                choice.save()
            else:
                OptionChoice.objects.create(option_id=option, **choice_data)

        existing_choice_ids = [choice['id'] for choice in choices_data if 'id' in choice]
        for choice in option.choices.exclude(id__in=existing_choice_ids):
            choice.delete()

    @action(detail=True, methods=['post'], url_path='delete')
    def delete_option(self, request, pk=None):
        try:
            option = self.get_object()
            option.is_deleted = True
            option.save()
            return Response({"message": "Option deleted successfully."}, status=status.HTTP_200_OK)
        except Options.DoesNotExist:
            return Response({"error": "Option not found."}, status=status.HTTP_404_NOT_FOUND)

# 메뉴 관련 API
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

# 주문 관련 API
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
    