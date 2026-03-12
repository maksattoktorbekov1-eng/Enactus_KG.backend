from django.urls import path
from .views import (
    ProgramListView, ProgramDetailView,
    AdminProgramListCreateView, AdminProgramDetailView,
    AdminProgramGalleryListCreateView, AdminProgramGalleryDetailView,
    AdminProgramTeamListCreateView, AdminProgramTeamDetailView,
    AdminProgramAdvisorListCreateView, AdminProgramAdvisorDetailView,
    AdminProgramTimelineListCreateView, AdminProgramTimelineDetailView,
)

urlpatterns = [
    path('programs/', ProgramListView.as_view(), name='program-list'),
    path('programs/<slug:slug>/', ProgramDetailView.as_view(), name='program-detail'),
    path('admin/programs/', AdminProgramListCreateView.as_view(), name='admin-program-list'),
    path('admin/programs/<int:pk>/', AdminProgramDetailView.as_view(), name='admin-program-detail'),
    path('admin/programs/<int:program_id>/gallery/', AdminProgramGalleryListCreateView.as_view(), name='program-gallery-list'),
    path('admin/programs/<int:program_id>/gallery/<int:pk>/', AdminProgramGalleryDetailView.as_view(), name='program-gallery-detail'),
    path('admin/programs/<int:program_id>/teams/', AdminProgramTeamListCreateView.as_view(), name='program-team-list'),
    path('admin/programs/<int:program_id>/teams/<int:pk>/', AdminProgramTeamDetailView.as_view(), name='program-team-detail'),
    path('admin/programs/<int:program_id>/advisors/', AdminProgramAdvisorListCreateView.as_view(), name='program-advisor-list'),
    path('admin/programs/<int:program_id>/advisors/<int:pk>/', AdminProgramAdvisorDetailView.as_view(), name='program-advisor-detail'),
    path('admin/programs/<int:program_id>/timeline/', AdminProgramTimelineListCreateView.as_view(), name='program-timeline-list'),
    path('admin/programs/<int:program_id>/timeline/<int:pk>/', AdminProgramTimelineDetailView.as_view(), name='program-timeline-detail'),
]