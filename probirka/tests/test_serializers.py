from django.test import TestCase

from catalog.models import Section, Subsection
from catalog.serializers import SectionSerializer


class SectionSerializerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.section = Section.objects.create(name="Гормоны", slug="gormony-serializer")
        Subsection.objects.create(name="Надпочечники", section=cls.section)

    def test_section_serializer_includes_nested_subsections(self):
        """Сериализатор отдаёт subsections как вложенный список id+name."""
        data = SectionSerializer(self.section).data
        self.assertIn("subsections", data)
        self.assertEqual(len(data["subsections"]), 1)
        self.assertEqual(data["subsections"][0]["name"], "Надпочечники")
