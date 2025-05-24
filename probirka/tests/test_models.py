from django.test import TestCase

from django.core.exceptions import ValidationError

from catalog.models import Section, Subsection, AdditionalService, Test


class TestModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.section = Section.objects.create(
            name="Гормоны", slug="gormony-model"
        )  # уникально
        cls.subsection = Subsection.objects.create(
            name="Щитовидка", section=cls.section
        )
        cls.service = AdditionalService.objects.create(
            name="Взятие крови", price="130.00"
        )

    # ─────────────────── positive ───────────────────
    def test_test_can_be_linked_directly_to_section(self):
        """Модель допускает отсутствие subsection."""
        t = Test.objects.create(
            name="T4 свободный",
            biomaterial="кровь",
            price="450.00",
            section=self.section,
            additional_service=self.service,
        )
        self.assertEqual(t.subsection, None)
        self.assertEqual(t.section, self.section)

    def test_test_can_be_linked_via_subsection(self):
        """При указании subsection clean() не падает, если принадлежит тому же section."""
        t = Test.objects.create(
            name="Тест",
            biomaterial="кровь",
            price="1.00",
            section=self.section,
            subsection=self.subsection,
        )
        t.full_clean()  # не должно вызвать ValidationError

    # ─────────────────── negative ───────────────────
    def test_subsection_must_belong_to_same_section(self):
        """subsection от другого раздела → ValidationError."""
        other = Section.objects.create(name="Аллергия", slug="allergy")
        wrong_sub = Subsection.objects.create(name="Пыльца", section=other)

        test = Test(
            name="IgE",
            biomaterial="кровь",
            price="600.00",
            section=self.section,
            subsection=wrong_sub,
        )
        with self.assertRaises(ValidationError):
            test.full_clean()
