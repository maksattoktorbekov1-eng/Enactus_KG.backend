from rest_framework import generics, permissions, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Partner
from .serializers import PartnerPublicSerializer, PartnerAdminSerializer, PartnerReorderSerializer


class PartnerListView(generics.ListAPIView):
    serializer_class   = PartnerPublicSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Partner.objects.filter(is_active=True).prefetch_related('translations')

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['lang'] = self.request.query_params.get('lang', 'ru')
        return ctx


class AdminPartnerListCreateView(generics.ListCreateAPIView):
    serializer_class   = PartnerAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]
    swagger_schema     = None

    def get_queryset(self):
        return Partner.objects.prefetch_related('translations').order_by('sort_order')


class AdminPartnerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = PartnerAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes     = [MultiPartParser, FormParser]
    swagger_schema     = None

    def get_queryset(self):
        return Partner.objects.prefetch_related('translations').all()


class AdminPartnerReorderView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ids': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_INTEGER),
                    description='Список ID партнёров в нужном порядке'
                )
            }
        )
    )
    def patch(self, request):
        serializer = PartnerReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ids = serializer.validated_data['ids']
        for index, partner_id in enumerate(ids):
            Partner.objects.filter(id=partner_id).update(sort_order=index)
        return Response({'detail': 'Порядок обновлён.'}, status=status.HTTP_200_OK)