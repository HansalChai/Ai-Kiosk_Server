# kiosk_server/categories/serializers.py

from rest_framework import serializers
from rest_framework.response import Response
from .models import Category, Options, OptionChoice, Menu, Order_amount, Order, Order_menu, Order_choice_order_menu

class CategorySerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'owner_id']

    def create(self, validated_data):
        request = self.context.get('request')
        owner_id = request.user
        validated_data.pop('owner', None)  # 중복 전달 피하기 위해 owner 잠시 제거함
        return Category.objects.create(owner_id=owner_id, **validated_data)


class OptionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionChoice
        fields = ['choice_name', 'extra_cost']

class OptionSerializer(serializers.ModelSerializer):
    choices = OptionChoiceSerializer(many=True)
    # owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Options
        fields = ['id', 'option_name', 'choices']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        option = Options.objects.create(**validated_data)
        for choice_data in choices_data:
            OptionChoice.objects.create(option_id=option, **choice_data)
        return option


class MenuSerializer(serializers.ModelSerializer):
    category_id = serializers.ReadOnlyField(source='category_id.id')
    
    class Meta:
        model = Menu
        fields = ['id', 'category_id', 'name', 'image', 'price', 'is_deleted', 'created_at', 'updated_at']

class OrderAmountSerializer(serializers.ModelSerializer):
    teenager = serializers.IntegerField()
    adult = serializers.IntegerField()
    elder = serializers.IntegerField()
    aged = serializers.IntegerField()
    class Meta:
        model = Order_amount
        fields = '__all__'

class OptionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionChoice
        fields = ['id', 'choice_name', 'extra_cost']

class OrderChoiceOrderMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_choice_order_menu
        fields = ['option_choice_id']

class OrderMenuSerializer(serializers.ModelSerializer):
    options = OrderChoiceOrderMenuSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Order_menu
        fields = ['menu_id', 'count', 'options']

    def create(self, validated_data):
        options_data = validated_data.pop('options',[])
        order_menu = Order_menu.objects.create(**validated_data)
        for option_data in options_data:
            option_choice = OptionChoice.objects.get(id=option_data['option_choice_id'].id)
            Order_choice_order_menu.objects.create(order_menu_id=order_menu, option_choice_id=option_choice)
        return order_menu

class OrderSerializer(serializers.ModelSerializer):
    order_menus = OrderMenuSerializer(many=True)

    class Meta:
        model = Order
        fields = ['membership_id', 'order_num', 'order_age', 'package', 'order_menus']

    def create(self, validated_data):
        order_menus_data = validated_data.pop('order_menus')
        order = Order.objects.create(**validated_data)
        for order_menu_data in order_menus_data:
            options_data = order_menu_data.pop('options')
            order_menu = Order_menu.objects.create(order_id=order, **order_menu_data)
            for option_data in options_data:
                option_choice = OptionChoice.objects.get(id=option_data['option_choice_id'].id)
                Order_choice_order_menu.objects.create(order_menu_id=order_menu, option_choice_id=option_choice)
        return order