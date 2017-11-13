import pytest
from faker import Faker

from downloader.opencaching_login_service import OpencachingLoginService, \
    IOpencachingLoginService
from downloader.opencaching_request_maker import (
    IOpencachingRequestMaker,
    RequestData,
    RequestMakerResponse,
)
from downloader.shell_variables_configuration_getter import \
    IConfigurationGetter

faker = Faker()


class MockedRequestMaker(IOpencachingRequestMaker):
    cookies = {
        faker.text(max_nb_chars=20): faker.text(max_nb_chars=200),
        faker.text(max_nb_chars=20): faker.text(max_nb_chars=200),
    }
    _calls_count = 0
    _called_url = None
    _called_data = None

    def get_opencaching_base_url(self) -> str:
        raise NotImplementedError

    def post(self, url: str, data: RequestData) -> RequestMakerResponse:
        self._calls_count += 1
        self._called_url = url
        self._called_data = data

        return RequestMakerResponse(text='gotham result', cookies=self.cookies)

    def assert_called_post_once_with(self, url, data):
        assert self._calls_count == 1
        assert self._called_url == url
        assert self._called_data == data


class MockedConfigurationGetter(IConfigurationGetter):
    def __init__(self):
        self._login = faker.text(max_nb_chars=20)
        self._password = faker.text(max_nb_chars=20)

    def get_login(self) -> str:
        return self._login

    def get_password(self) -> str:
        return self._password


def test_make_proper_request():
    request_maker = MockedRequestMaker()
    configuration = MockedConfigurationGetter()

    service = OpencachingLoginService(request_maker, configuration)
    service.login()

    request_maker.assert_called_post_once_with(
        '/login.php?action=login',
        data={
            'email': configuration.get_login(),
            'password': configuration.get_password(),
            'target': '/',
            'submit': 'Zaloguj się',
        }
    )


def test_return_cookies_from_request():
    request_maker = MockedRequestMaker()
    configuration = MockedConfigurationGetter()

    service = OpencachingLoginService(request_maker, configuration)
    cookies = service.login()

    assert cookies == request_maker.cookies


class TestIOpencachingLoginService:
    def test_raise_on_login(self):
        with pytest.raises(NotImplementedError):
            IOpencachingLoginService().login()
