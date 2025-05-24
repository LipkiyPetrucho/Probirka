from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from catalog.models import Section, Subsection, Test
from feedback.models import ContactMessage


class CatalogAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.sec = Section.objects.create(name='Аллергия', slug='allergy')
        cls.sub = Subsection.objects.create(name='ИммуноCAP', section=cls.sec)
        cls.test = Test.objects.create(
            name='Глютен, IgE',
            biomaterial='кровь',
            price='600.00',
            section=cls.sec,
            subsection=cls.sub,
        )

    # ─────────────────── list & detail ───────────────────
    def test_sections_list(self):
        url = reverse('section-list')  # router генерирует имя <basename>-list
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['results'][0]['name'], 'Аллергия')

    def test_tests_detail(self):
        url = reverse('test-detail', args=[self.test.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['name'], 'Глютен, IgE')

    # ─────────────────── фильтр ───────────────────
    def test_tests_filter_by_section(self):
        url = reverse('test-list') + f'?section={self.sec.id}'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['count'], 1)

    # ─────────────────── поиск ───────────────────
    def test_tests_search(self):
        url = reverse('test-list') + '?search=IgE'  # вместо 'глютен'
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(resp.data['count'], 1)


class FeedbackAPITests(APITestCase):
    def test_contact_post_creates_message(self):
        url = reverse('contact-message')  # зададим имя в urls.py
        payload = {'name': 'Alice', 'email': 'a@ex.com', 'message': 'Hi!'}
        self.assertEqual(ContactMessage.objects.count(), 0)

        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ContactMessage.objects.count(), 1)
