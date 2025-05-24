from rest_framework import serializers
from .models import Section, Subsection, Test, AdditionalService


class AdditionalServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalService
        fields = ('id', 'name', 'price')


class SubsectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subsection
        fields = ('id', 'name', 'description', 'section')


class NestedSubsectionSerializer(serializers.ModelSerializer):
    """Упрощённый вариант (id + name) для вложенного списка в Section."""
    class Meta:
        model = Subsection
        fields = ('id', 'name')


class SectionSerializer(serializers.ModelSerializer):
    subsections = NestedSubsectionSerializer(many=True, read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'name', 'description', 'subsections')


class TestSerializer(serializers.ModelSerializer):
    additional_service = AdditionalServiceSerializer(read_only=True)

    class Meta:
        model = Test
        fields = (
            'id',
            'name',
            'biomaterial',
            'price',
            'section',
            'subsection',
            'additional_service',
        )
