from typing import Dict

from injector import inject

SystemVariables = Dict[str, str]


class IConfigurationGetter:
    def get_login(self) -> str:
        raise NotImplementedError

    def get_password(self) -> str:
        raise NotImplementedError

    def get_opencaching_base_url(self) -> str:
        raise NotImplementedError


class ShellVariablesConfigurationGetter(IConfigurationGetter):
    @inject
    def __init__(self, configuration: SystemVariables) -> None:
        self._configuration = configuration

    def get_login(self) -> str:
        return self._configuration['OC_LOGIN']

    def get_password(self) -> str:
        return self._configuration['OC_PASSWORD']

    def get_opencaching_base_url(self) -> str:
        return self._configuration['OC_BASE_URL']
