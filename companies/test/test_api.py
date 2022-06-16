import json
from django.test import TestCase
from django.urls import reverse


class TestGetCompanies(TestCase):
    def test_zero_companies_should_return_empty_list(self):
        URL = reverse('companies-list')
        res = self.client.get(URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.content), [])
