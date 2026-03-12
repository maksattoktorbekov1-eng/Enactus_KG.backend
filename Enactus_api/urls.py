from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title='Enactus KG API',
        default_version='v1',
        description='API для сайта Enactus Кыргызстан',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

admin.site.site_header = 'Enactus KG — Панель управления'
admin.site.site_title  = 'Enactus KG Admin'
admin.site.index_title = 'Добро пожаловать в административную панель'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('programs.urls')),
    path('api/', include('partners.urls')),
    path('api/', include('news.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
