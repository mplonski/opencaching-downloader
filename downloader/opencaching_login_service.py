from injector import inject

from downloader.opencaching_request_maker import (
    Cookies,
    IOpencachingRequestMaker,
)
from downloader.shell_variables_configuration_getter import \
    IConfigurationGetter


class IOpencachingLoginService:
    def login(self) -> Cookies:
        raise NotImplementedError


class OpencachingLoginService(IOpencachingLoginService):
    @inject
    def __init__(
            self,
            request_maker: IOpencachingRequestMaker,
            configuration: IConfigurationGetter,
    ):
        self._request_maker = request_maker
        self._configuration = configuration

    def login(self) -> Cookies:
        login_data = {
            'email': self._configuration.get_login(),
            'password': self._configuration.get_password(),
            'target': '/',
            'submit': 'Zaloguj się',
        }
        response = self._request_maker.post(
            url='/login.php?action=login',
            data=login_data,
        )

        return response.cookies
