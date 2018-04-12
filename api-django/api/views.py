from rest_framework import viewsets, filters, renderers
from rest_framework.response import Response
from rest_framework.decorators import list_route
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import FilterSet 
from django.db import connection
from django.db.models import Q
from .models import Tenant, Job, Client
from .serializers import TenantSerializer, JobSerializer, ClientSerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = (Client.objects.all()
        .select_related('primary_contact__contact_department')
        .select_related('primary_contact__contact_default_phone')
        .select_related('primary_contact__contact_default_address')
        .select_related('industry')
        .select_related('default_tax')
        .select_related('default_terms')
        .select_related('default_currency')
        .select_related('sales_rep__login')
        .select_related('account_status')
    )
    serializer_class = ClientSerializer


class JobFilter(FilterSet):
    class Meta:
        model = Job 
        # url: /jobs?job_name=hello&job_number__lt=9999&job_number__gt=5000&date_created__year__gt=2016
        fields = {
            'job_name': ['exact'],
            'job_number': ['lt', 'gt'],
            'date_created': ['year__gt'],
        }


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().select_related('tenant').prefetch_related('orders__items')
    serializer_class = JobSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter,)
    search_fields = ('job_name', 'job_number', 'tenant__tenant_name')
    ordering_fields = ('date_created',)
    filter_class = JobFilter

    @list_route(methods=['get'])
    def complex_example(self, request):
        qs = (
            self
            .get_queryset()
            .filter(tenant__tenant_name__icontains='vandelay')
            .filter(Q(orders__order_type='PRESENTATION') | Q(tenant__hidden=True))
        )[:20]
        serializer = self.get_serializer(qs, many=True)
        response = Response(serializer.data)
        print(connection.queries)
        return response


