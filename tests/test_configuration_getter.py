import pytest
from faker import Faker

from downloader.shell_variables_configuration_getter import (
    ShellVariablesConfigurationGetter,
    IConfigurationGetter)

faker = Faker()


def test_return_opencaching_login_from_configuration():
    configuration = {
        'OC_LOGIN': faker.name(),
    }
    getter = ShellVariablesConfigurationGetter(configuration)
    assert configuration['OC_LOGIN'] == getter.get_login()


def test_return_opencaching_password_from_configuration():
    configuration = {
        'OC_PASSWORD': faker.name(),
    }
    getter = ShellVariablesConfigurationGetter(configuration)
    assert configuration['OC_PASSWORD'] == getter.get_password()


def test_return_opencaching_base_url_from_configuration():
    configuration = {
        'OC_BASE_URL': 'http://oc.pl/',
    }
    getter = ShellVariablesConfigurationGetter(configuration)
    assert configuration['OC_BASE_URL'] == getter.get_opencaching_base_url()


class TestIConfigurationGetter:
    def test_raise_on_get_login(self):
        with pytest.raises(NotImplementedError):
            IConfigurationGetter().get_login()

    def test_raise_on_get_password(self):
        with pytest.raises(NotImplementedError):
            IConfigurationGetter().get_password()

    def test_raise_on_get_opencaching_base_url(self):
        with pytest.raises(NotImplementedError):
            IConfigurationGetter().get_opencaching_base_url()
