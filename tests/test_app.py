import os

from injector import Injector

from downloader.app import get_injector
from downloader.opencaching_login_service import IOpencachingLoginService, \
    OpencachingLoginService
from downloader.shell_variables_configuration_getter import \
    IConfigurationGetter, ShellVariablesConfigurationGetter, SystemVariables


def test_injector_is_available():
    assert isinstance(get_injector(), Injector)


def test_environmental_variables_are_registered():
    injector = get_injector()

    assert injector.get(SystemVariables) == dict(os.environ)


def test_configuration_getter_is_registered():
    injector = get_injector()

    assert isinstance(
        injector.get(IConfigurationGetter),
        ShellVariablesConfigurationGetter
    )


def test_login_service_is_registered():
    injector = get_injector()

    assert isinstance(
        injector.get(IOpencachingLoginService),
        OpencachingLoginService
    )
