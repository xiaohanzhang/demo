from rest_framework import serializers
from .models import Tenant, Job, Order, User, Item


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'login', )

    login = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='login_name'
     )


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('id', 'tenant_name')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'item_name')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'order_type', 'form_number', 'items')

    items = ItemSerializer(many=True, read_only=True)


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'job_name', 'job_number', 'tenant', 'orders', 'date_created')

    tenant = TenantSerializer(many=False, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

