# kiosk_server/categories/serializers.py

from rest_framework import serializers
from .models import Category, Options, OptionChoice, Menu

class CategorySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Category
        fields = ['category_id', 'category_name', 'owner',]

    def create(self, validated_data):
        request = self.context.get('request')
        owner = request.user
        validated_data.pop('owner', None)  # 중복 전달 피하기 위해 owner 잠시 제거함
        return Category.objects.create(owner=owner, **validated_data)


class OptionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OptionChoice
        fields = ['choice_name', 'extra_cost']

class OptionSerializer(serializers.ModelSerializer):
    choices = OptionChoiceSerializer(many=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Options
        fields = ['option_ID', 'category_ID', 'owner', 'option_name', 'choices']

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
            OptionChoice.objects.create(option=option, **choice_data)
        return option

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'