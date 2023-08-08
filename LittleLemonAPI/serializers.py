from rest_framework import serializers
from decimal import Decimal
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    tax_constant = serializers.SerializerMethodField(method_name='tax')
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'tax_constant', 'price_after_tax', 'category', 'category_id']

    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.5)

    def tax(self, tax:MenuItem):
        tax = 1.5
        return tax

class CartSerializer(serializers.ModelSerializer):
    class Meta():
        model = Cart
        fields = ['id', 'menuitem', 'quantity', 'price'] 

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta():
        model = OrderItem
        fields = ['id', 'order', 'menuitem', 'quantity', 'unit_price', 'price']