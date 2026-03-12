from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Program, ProgramGallery, ProgramTeam, ProgramAdvisor, ProgramTimeline
from .serializers import (
    ProgramListPublicSerializer, ProgramPublicSerializer, ProgramAdminSerializer,
    ProgramGallerySerializer, ProgramTeamSerializer,
    ProgramAdvisorSerializer, ProgramTimelineSerializer,
)


class ProgramListView(generics.ListAPIView):
    serializer_class   = ProgramListPublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Program.objects.filter(is_active=True).prefetch_related('translations')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = self.request.query_params.get('lang', 'ru')
        return ctx


class ProgramDetailView(generics.RetrieveAPIView):
    serializer_class   = ProgramPublicSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field       = 'slug'
    swagger_schema     = None

    def get_queryset(self):
        return Program.objects.filter(is_active=True).prefetch_related(
            'translations', 'gallery', 'teams', 'advisors', 'timeline__translations',
        )

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = self.request.query_params.get('lang', 'ru')
        return ctx


class AdminProgramListCreateView(generics.ListCreateAPIView):
    serializer_class   = ProgramAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]
    swagger_schema     = None

    def get_queryset(self):
        return Program.objects.prefetch_related(
            'translations', 'gallery', 'teams', 'advisors', 'timeline__translations',
        ).order_by('sort_order')


class AdminProgramDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = ProgramAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]
    swagger_schema     = None

    def get_queryset(self):
        return Program.objects.prefetch_related(
            'translations', 'gallery', 'teams', 'advisors', 'timeline__translations',
        )

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class AdminProgramGalleryListCreateView(generics.ListCreateAPIView):
    serializer_class   = ProgramGallerySerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProgramGallery.objects.filter(program_id=self.kwargs['program_id'])

    def perform_create(self, serializer):
        serializer.save(program_id=self.kwargs['program_id'])


class AdminProgramGalleryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = ProgramGallerySerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProgramGallery.objects.filter(program_id=self.kwargs['program_id'])


class AdminProgramTeamListCreateView(generics.ListCreateAPIView):
    serializer_class   = ProgramTeamSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProgramTeam.objects.filter(program_id=self.kwargs['program_id'])

    def perform_create(self, serializer):
        serializer.save(program_id=self.kwargs['program_id'])


class AdminProgramTeamDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = ProgramTeamSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProgramTeam.objects.filter(program_id=self.kwargs['program_id'])


class AdminProgramAdvisorListCreateView(generics.ListCreateAPIView):
    serializer_class   = ProgramAdvisorSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProgramAdvisor.objects.filter(program_id=self.kwargs['program_id'])

    def perform_create(self, serializer):
        serializer.save(program_id=self.kwargs['program_id'])


class AdminProgramAdvisorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = ProgramAdvisorSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]

    def get_queryset(self):
        return ProgramAdvisor.objects.filter(program_id=self.kwargs['program_id'])


class AdminProgramTimelineListCreateView(generics.ListCreateAPIView):
    serializer_class   = ProgramTimelineSerializer
    permission_classes = [permissions.IsAdminUser]
    swagger_schema     = None

    def get_queryset(self):
        return ProgramTimeline.objects.filter(
            program_id=self.kwargs['program_id']
        ).prefetch_related('translations')

    def perform_create(self, serializer):
        serializer.save(program_id=self.kwargs['program_id'])


class AdminProgramTimelineDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = ProgramTimelineSerializer
    permission_classes = [permissions.IsAdminUser]
    swagger_schema     = None

    def get_queryset(self):
        return ProgramTimeline.objects.filter(
            program_id=self.kwargs['program_id']
        ).prefetch_related('translations')