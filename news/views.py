from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.utils import timezone
from .models import News, NewsCategory
from .serializers import (
    NewsPublicSerializer, NewsListPublicSerializer, NewsAdminSerializer,
    NewsCategoryPublicSerializer, NewsCategoryAdminSerializer,
)


class NewsCategoryListView(generics.ListAPIView):
    serializer_class   = NewsCategoryPublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return NewsCategory.objects.prefetch_related('translations').all()

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = self.request.query_params.get('lang', 'ru')
        return ctx


class NewsListView(generics.ListAPIView):
    serializer_class   = NewsListPublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = News.objects.filter(
            is_published=True,
            published_at__lte=timezone.now()
        ).select_related('category').prefetch_related(
            'translations', 'category__translations'
        )
        category_slug = self.request.query_params.get('category')
        if category_slug:
            qs = qs.filter(category__slug=category_slug)
        limit = self.request.query_params.get('limit')
        if limit:
            qs = qs[:int(limit)]
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = self.request.query_params.get('lang', 'ru')
        return ctx


class NewsDetailView(generics.RetrieveAPIView):
    serializer_class   = NewsPublicSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field       = 'slug'

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related(
            'category'
        ).prefetch_related('translations', 'category__translations')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = self.request.query_params.get('lang', 'ru')
        return ctx


class AdminNewsListCreateView(generics.ListCreateAPIView):
    serializer_class   = NewsAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]
    swagger_schema     = None

    def get_queryset(self):
        return News.objects.select_related('category').prefetch_related(
            'translations'
        ).order_by('-created_at')


class AdminNewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = NewsAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]
    swagger_schema     = None

    def get_queryset(self):
        return News.objects.prefetch_related('translations').all()

    def perform_destroy(self, instance):
        instance.is_published = False
        instance.save()


class AdminNewsCategoryListCreateView(generics.ListCreateAPIView):
    serializer_class   = NewsCategoryAdminSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return NewsCategory.objects.prefetch_related('translations').all()


class AdminNewsCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = NewsCategoryAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    queryset           = NewsCategory.objects.prefetch_related('translations').all()