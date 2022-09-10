import json
import logging
from django.urls import reverse
import pytest

from companies.models import Company

URL = reverse('companies-list')

pytestmark = pytest.mark.django_db


def test_zero_companies_should_return_empty_list(client):
    res = client.get(URL)
    assert res.status_code == 200
    assert json.loads(res.content) == []


def test_one_company_exists_should_succeed(client):
    company = Company.objects.create(name='Test company')
    res = client.get(URL)
    response_content = json.loads(res.content)[0]

    assert res.status_code == 200
    assert response_content.get('name') == company.name
    assert response_content.get('status') == company.status
    assert response_content.get('notes') == company.notes
    assert response_content.get('application_link') == company.application_link


def test_create_company_without_arguments_should_fail(client):
    res = client.post(URL)
    assert res.status_code == 400
    assert json.loads(res.content) == {'name': ['This field is required.']}


def test_create_existing_company_should_fail(client):
    company = Company.objects.create(name='Test company')
    res = client.post(URL, data={'name': company.name})
    assert res.status_code == 400
    assert json.loads(res.content) == {'name': ['company with this name already exists.']}


def test_create_company_with_only_name_all_fields_should_be_default(client):
    res = client.post(URL, {'name': 'Testing company'})
    res_content = json.loads(res.content)

    assert res.status_code == 201
    assert res_content['name'] == 'Testing company'
    assert res_content['status'] == 'Hiring'
    assert res_content['application_link'] == ''
    assert res_content['notes'] == ''


def test_create_company_with_layoffs_status_should_succeed(client):
    res = client.post(URL, {'name': 'New company', 'status': 'Layoffs'})
    res_content = json.loads(res.content)

    assert res.status_code == 201
    assert res_content.get('status') == 'Layoffs'


@pytest.fixture
def company(**kwargs):
    def _company_factory(**kwargs) -> Company:
        company_name = kwargs.pop('name', 'test company inc')
        return Company.objects.create(name=company_name, **kwargs)

    return _company_factory


def test_multiple_companies_exists_should_succeed(client, company):
    ticktock = company(name='ticktock')
    twitch = company(name='twitch')
    test_company = company()
    company_names = {ticktock.name, twitch.name, test_company.name}
    response_companies = client.get(URL).json()
    assert len(company_names) == len(response_companies)
    response_company_names = set(map(lambda company: company.get('name'), response_companies))
    assert company_names == response_company_names


def test_create_company_with_wrong_status_should_fail(client):
    res = client.post(URL, {'name': 'Test company', 'status': 'wrong status'})
    assert res.status_code == 400
    assert 'is not a valid choice' in str(res.content)


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


logger = logging.getLogger('CORONA_LOGS')


def function_that_logs_something():
    logger.warning('I am logging here!')


def test_logged_warning_level(caplog):
    function_that_logs_something()
    assert 'I am logging here!' in caplog.text
