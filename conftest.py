from companies.models import Company

import pytest


@pytest.fixture
def company(**kwargs):
    def _company_factory(**kwargs) -> Company:
        company_name = kwargs.pop('name', 'test company inc')
        return Company.objects.create(name=company_name, **kwargs)

    return _company_factory
