from django.urls import path, include
from rest_framework import routers, documentation, schemas
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import TenantViewSet, JobViewSet, ClientViewSet

router = routers.DefaultRouter()
# router.register(r'tenants', TenantViewSet)
router.register(r'jobs', JobViewSet)
router.register(r'clients', ClientViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='commonsku API',
        default_version='v2',
        description='Test description',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@commonsku.com"),
        license=openapi.License(name="BSD License"),
    ),
    validators=['flex', 'ssv'],
    public=True,
    # permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
    path('doc', documentation.include_docs_urls(title='Hello SKUBot')),
    path('swagger<format>', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]


