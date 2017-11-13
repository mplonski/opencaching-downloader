import os

from injector import Injector

from downloader.opencaching_login_service import (
    IOpencachingLoginService,
    OpencachingLoginService,
)
from downloader.shell_variables_configuration_getter import (
    ShellVariablesConfigurationGetter,
    IConfigurationGetter,
    SystemVariables,
)


def get_injector():
    injector = Injector()

    injector.binder.bind(SystemVariables, to=lambda: dict(os.environ))
    injector.binder.bind(IConfigurationGetter,
                         to=ShellVariablesConfigurationGetter)
    injector.binder.bind(IOpencachingLoginService,
                         to=OpencachingLoginService)

    return injector
