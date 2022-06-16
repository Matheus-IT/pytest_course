import json
from django.test import TestCase
from django.urls import reverse

from companies.models import Company

URL = reverse('companies-list')


class TestGetCompanies(TestCase):
    def test_zero_companies_should_return_empty_list(self):
        res = self.client.get(URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json.loads(res.content), [])

    def test_one_company_exists_should_succeed(self):
        company = Company.objects.create(name='Test company')
        res = self.client.get(URL)
        response_content = json.loads(res.content)[0]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(response_content.get('name'), company.name)
        self.assertEqual(response_content.get('status'), company.status)
        self.assertEqual(response_content.get('notes'), company.notes)
        self.assertEqual(
            response_content.get('application_link'), company.application_link
        )
