from django.urls import path
from .views import (
    NewsCategoryListView,
    NewsListView,
    NewsDetailView,
    AdminNewsListCreateView,
    AdminNewsDetailView,
    AdminNewsCategoryListCreateView,
    AdminNewsCategoryDetailView,
)

urlpatterns = [
    path('news/categories/', NewsCategoryListView.as_view(), name='news-category-list'),
    path('news/', NewsListView.as_view(), name='news-list'),
    path('news/<slug:slug>/', NewsDetailView.as_view(), name='news-detail'),

    path('admin/news/categories/', AdminNewsCategoryListCreateView.as_view(), name='admin-news-category-list'),
    path('admin/news/categories/<int:pk>/', AdminNewsCategoryDetailView.as_view(), name='admin-news-category-detail'),

    path('admin/news/', AdminNewsListCreateView.as_view(), name='admin-news-list'),
    path('admin/news/<int:pk>/', AdminNewsDetailView.as_view(), name='admin-news-detail'),
]