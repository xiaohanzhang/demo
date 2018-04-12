from django.contrib import admin
from .models import Job, Tenant, Order, Client

class OrderAdmin(admin.ModelAdmin):
    raw_id_fields = ('job', 'tenant', 'created_by')


class TenantAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'tenant_default_address', 'created_by', 'tenant_default_job_template',
        'primary_contact'
    )
    list_display = ('tenant_name',)
    list_filter = ('active', 'hidden')
    search_fields = ('tenant_name',)


class JobAdmin(admin.ModelAdmin):
    raw_id_fields = ('tenant', 'created_by', 'client_rep')


class ClientAdmin(admin.ModelAdmin):
    raw_id_fields = (
        'primary_contact', 'industry', 'default_tax', 'created_by',
        'sales_rep', 'tenant', 'parent', 'secondary_contact', 
        'tertiary_contact', 'parent_client'
    )
    list_select_related = ('tenant',)
    list_display = ('client_name', 'get_tenant_name')
    list_filter = ('active',)
    search_fields = ('client_name', 'tenant__tenant_name',)

    def get_tenant_name(self, obj):
        return obj.tenant.tenant_name

admin.site.register(Order, OrderAdmin)
admin.site.register(Job, JobAdmin)
admin.site.register(Tenant, TenantAdmin)
admin.site.register(Client, ClientAdmin)