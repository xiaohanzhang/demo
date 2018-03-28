from rest_framework import serializers
from .models import (
    Tenant, Job, Order, User, Item, Client, Industry, Contact, Phone, Tax, Terms, Currency, Status,
    CommissionClientRate, Department
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('id', 'active', 'created_by', 'login')

    user_id = serializers.UUIDField(read_only=True, source='pk')
    login_name = serializers.SerializerMethodField()

    def get_login_name(self, obj):
        login = obj.login
        return login.login_name if login else ''


class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('tenant_id', 'tenant_name', 'tenant_status', 'date_created')

    tenant_id = serializers.UUIDField(read_only=True, source='pk')


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


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        exclude = ('id', 'active', 'tenant', 'created_by', 'date_created')

    industry_id = serializers.UUIDField(read_only=True, source='pk')
    # tenant = TenantSerializer(many=False, read_only=True)
    # created_by = UserSerializer(many=False, read_only=True)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        exclude = ('id', 'active', 'parent_type', 'created_by', 'date_created', 'ordering')

    department_id = serializers.UUIDField(read_only=True, source='pk')


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phone
        exclude = ('id', 'active', 'parent_id',)

    phone_id = serializers.UUIDField(read_only=True, source='pk')
    created_by = UserSerializer(many=False, read_only=True)


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        exclude = ('id', 'active', 'tenant', 'date_created', 'created_by')

    tax_id = serializers.UUIDField(read_only=True, source='pk')
    # tenant = TenantSerializer(many=False, read_only=True)
    # created_by = UserSerializer(many=False, read_only=True)


class TermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        exclude = ('id', 'active', 'created_by', 'days_to_add', 'display_order', 'date_created')

    terms_id = serializers.UUIDField(read_only=True, source='pk')
    # created_by = UserSerializer(many=False, read_only=True)


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        exclude = ('id', 'parent_type', 'flow_order')

    status_id = serializers.UUIDField(read_only=True, source='pk')
    # created_by = UserSerializer(many=False, read_only=True)


class CommissionClientRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionClientRate
        exclude = ('id', )

    commission_client_rate_id = serializers.UUIDField(read_only=True, source='pk')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        exclude = ('id', )

    currency_id = serializers.UUIDField(read_only=True, source='pk')
    # created_by = UserSerializer(many=False, read_only=True)


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        exclude = ('id', 'active', 'parent_contact', 'created_by')

    contact_id = serializers.UUIDField(read_only=True, source='pk')
    contact_default_phone = PhoneSerializer(many=False, read_only=True)
    # created_by = UserSerializer(many=False, read_only=True)
    contact_department = DepartmentSerializer(many=False, read_only=True)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        exclude = (
            'id', 'active', 'parent', 'parent_client', 'date_merged', 'qbo_customer_ref',
            'xero_contact_id', 'latest_use', 'date_quickbooks', 'quickbooks_id', 'priority',
            'prospect', 'tenant', 'secondary_contact', 'tertiary_contact', 'merged_by', 'created_by'
        )
        read_only_fields = ('client_id', 'date_created')
        # depth = 1
        # extra_kwargs
        # validators

    client_id = serializers.UUIDField(read_only=True, source='pk')
    # tenant = TenantSerializer(many=False, read_only=True)
    primary_contact = ContactSerializer(many=False, read_only=True)
    # secondary_contact = ContactSerializer(many=False, read_only=True)
    # tertiary_contact = ContactSerializer(many=False, read_only=True)
    industry = IndustrySerializer(many=False, read_only=True)
    default_tax = TaxSerializer(many=False, read_only=True)
    default_terms = TermsSerializer(many=False, read_only=True)
    default_currency = CurrencySerializer(many=False, read_only=True)
    sales_rep = UserSerializer(many=False, read_only=True)
    account_status = StatusSerializer(many=False, read_only=True)
    commission_client_rate = CommissionClientRateSerializer(many=False, read_only=True)
    # created_by = UserSerializer(many=False, read_only=True)
    # merged_by = UserSerializer(many=False, read_only=True)
