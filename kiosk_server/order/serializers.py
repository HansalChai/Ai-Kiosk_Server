# kiosk_server/categories/serializers.py

from rest_framework import serializers
from .models import Category, Options, OptionChoice, Menu, Order_amount

class CategorySerializer(serializers.ModelSerializer):
    owner_id = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Category
        fields = ['id', 'category_name', 'owner_id', 'is_deleted']

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
        fields = ['id', 'category_id', 'options_name', 'is_deleted', 'choices']

    #context를 활용한 조건부 처리
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if not self.context.get('view').request.user.is_authenticated and self.context.get('view').request.user.is_owner:
    #         representation.pop('order_menu_ID', None)
    #     return representation

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        option = Options.objects.create(**validated_data)
        for choice_data in choices_data:
            OptionChoice.objects.create(options_id=option, **choice_data)
        return option

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'

class OrderAmountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_amount
        fields = '__all__'