from django.urls import path
from .views import (
    PartnerListView,
    AdminPartnerListCreateView,
    AdminPartnerDetailView,
    AdminPartnerReorderView,
)

urlpatterns = [
    path('partners/', PartnerListView.as_view(), name='partner-list'),

    path('admin/partners/', AdminPartnerListCreateView.as_view(), name='admin-partner-list'),

    path('admin/partners/reorder/', AdminPartnerReorderView.as_view(), name='admin-partner-reorder'),

    path('admin/partners/<int:pk>/', AdminPartnerDetailView.as_view(), name='admin-partner-detail'),
]