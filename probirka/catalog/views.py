from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Section, Subsection, Test
from .serializers import (
    SectionSerializer,
    SubsectionSerializer,
    TestSerializer,
)


# ⚠️ каталог публично «только чтение», изменения — лишь для staff-пользователей.
class ReadOnlyIfAnonymousMixin:
    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            from rest_framework.permissions import AllowAny

            return [AllowAny()]
        from rest_framework.permissions import IsAdminUser

        return [IsAdminUser()]


class SectionViewSet(ReadOnlyIfAnonymousMixin, viewsets.ModelViewSet):
    queryset = Section.objects.prefetch_related("subsections").all()
    serializer_class = SectionSerializer
    http_method_names = ["get", "head", "options"]  # публично только чтение

    @action(detail=True, methods=["get"])
    def subsections(self, request, pk=None):
        """GET /api/sections/<id>/subsections/ — подразделы выбранного раздела."""
        subs = Subsection.objects.filter(section_id=pk)
        page = self.paginate_queryset(subs)
        ser = SubsectionSerializer(page or subs, many=True)
        return (
            self.get_paginated_response(ser.data)
            if page is not None
            else Response(ser.data)
        )


class SubsectionViewSet(ReadOnlyIfAnonymousMixin, viewsets.ModelViewSet):
    queryset = Subsection.objects.select_related("section").all()
    serializer_class = SubsectionSerializer
    http_method_names = ["get", "head", "options"]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["section"]  # ?section=<id>

    @action(detail=True, methods=["get"])
    def tests(self, request, pk=None):
        """GET /api/subsections/<id>/tests/ — анализы внутри подраздела."""
        tests = Test.objects.filter(subsection_id=pk).select_related(
            "section", "subsection", "additional_service"
        )
        page = self.paginate_queryset(tests)
        ser = TestSerializer(page or tests, many=True)
        return (
            self.get_paginated_response(ser.data)
            if page is not None
            else Response(ser.data)
        )


class TestViewSet(ReadOnlyIfAnonymousMixin, viewsets.ModelViewSet):
    queryset = Test.objects.select_related(
        "section", "subsection", "additional_service"
    ).all()
    serializer_class = TestSerializer
    http_method_names = ["get", "head", "options"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["section", "subsection"]  # ?section= или ?subsection=
    search_fields = [
        "name"
    ]  # ?search=<query> по названию ﻿:contentReference[oaicite:2]{index=2}
