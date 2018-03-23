from rest_framework import viewsets, filters, renderers
from rest_framework.response import Response
from rest_framework.decorators import list_route
from openapi_codec import OpenAPICodec
from django_filters.rest_framework import DjangoFilterBackend
from django.db import connection
from django.db.models import Q
from .models import Tenant, Job
from .serializers import TenantSerializer, JobSerializer


class SwaggerRenderer(renderers.BaseRenderer):
    media_type = 'application/openapi+json'
    format = 'swagger'

    def render(self, data, media_type=None, renderer_context=None):
        codec = OpenAPICodec()
        return codec.dump(data)


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().select_related('tenant').prefetch_related('orders__items')
    serializer_class = JobSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter,)
    search_fields = ('job_name', 'job_number', 'tenant__tenant_name')
    ordering_fields = ('date_created',)

    def list(self, request, *args, **kwargs):
        response = super(JobViewSet, self).list(request, *args, **kwargs)
        return response

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


