import json
from django.test import TestCase
from django.urls import reverse
import pytest

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


class TestPostCompanies(TestCase):
    def test_create_company_without_arguments_should_fail(self):
        res = self.client.post(URL)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            json.loads(res.content), {'name': ['This field is required.']}
        )

    def test_create_existing_company_should_fail(self):
        company = Company.objects.create(name='Test company')
        res = self.client.post(URL, data={'name': company.name})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            json.loads(res.content),
            {'name': ['company with this name already exists.']},
        )

    def test_create_company_with_only_name_all_fields_should_be_default(self):
        res = self.client.post(URL, {'name': 'Testing company'})
        res_content = json.loads(res.content)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_content['name'], 'Testing company')
        self.assertEqual(res_content['status'], 'Hiring')
        self.assertEqual(res_content['application_link'], '')
        self.assertEqual(res_content['notes'], '')

    def test_create_company_with_layoffs_status_should_succeed(self):
        res = self.client.post(
            URL, {'name': 'New company', 'status': 'Layoffs'}
        )
        res_content = json.loads(res.content)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(res_content.get('status'), 'Layoffs')

    def test_create_company_with_wrong_status_should_fail(self):
        res = self.client.post(
            URL, {'name': 'Test company', 'status': 'wrong status'}
        )
        self.assertEqual(res.status_code, 400)
        self.assertIn('is not a valid choice', str(res.content))

    @pytest.mark.xfail
    def test_should_be_ok_to_fail(self):
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_be_skipped(self):
        self.assertEqual(1, 2)


def raise_covid19_exception():
    raise ValueError('CoronaVirus Exception')


def test_raise_covid19_exception_should_pass():
    with pytest.raises(ValueError) as e:
        raise_covid19_exception()
    assert 'CoronaVirus Exception' == str(e.value)
