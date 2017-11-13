from typing import Any

import pytest
from faker import Faker

from downloader.opencaching_request_maker import OpencachingRequestMaker, \
    RequestData, Cookies, IOpencachingRequestMaker
from downloader.shell_variables_configuration_getter import \
    IConfigurationGetter

faker = Faker()


class RequestResponse:
    def __init__(self, response: str, cookies: Cookies) -> None:
        self.text = response
        self.cookies = cookies


class MockedPostRequests:
    _called_num = 0
    _called_url = None
    _called_data = None
    _faked_response = None
    _faked_cookies = None

    def post(self, url: str, data: RequestData) -> Any:
        self._called_num += 1
        self._called_url = url
        self._called_data = data
        self._faked_response = faker.text()
        self._faked_cookies = {
            faker.text(max_nb_chars=20): faker.text(max_nb_chars=50),
            faker.text(max_nb_chars=20): faker.text(max_nb_chars=50),
        }

        return RequestResponse(self._faked_response, self._faked_cookies)

    def assert_once_called_post(self, url: str, data: RequestData) -> None:
        assert self._called_num == 1
        assert self._called_url == url
        assert self._called_data == data

    def get_mocked_response(self) -> str:
        return self._faked_response

    def get_mocked_cookies(self) -> Cookies:
        return self._faked_cookies


class MockedRequests(MockedPostRequests):
    pass


class MockedConfigurationGetter(IConfigurationGetter):
    login = ''
    password = ''
    base_url = 'https://oc.pl'

    def get_opencaching_base_url(self) -> str:
        return self.base_url


@pytest.mark.parametrize('opencaching_base_url,proper_url', [
    ('https://oc.pl/', 'https://oc.pl'),
    ('https://oc.pl', 'https://oc.pl'),
])
def test_save_opencaching_base_url_without_end_slash(
        opencaching_base_url, proper_url
):
    requests = MockedRequests()
    configuration_getter = MockedConfigurationGetter()
    configuration_getter.base_url = opencaching_base_url

    request_maker = OpencachingRequestMaker(requests, configuration_getter)
    assert proper_url == request_maker.get_opencaching_base_url()


def test_requests_called_properly_when_post_request_made():
    requests = MockedPostRequests()
    configuration_getter = MockedConfigurationGetter()

    request_maker = OpencachingRequestMaker(requests, configuration_getter)
    payload = {
        'some': 'data',
        'foo': 'bar',
    }
    request_maker.post('/some/url', data=payload)

    requests.assert_once_called_post('https://oc.pl/some/url', data=payload)


def test_return_response_text_from_post_request():
    requests = MockedPostRequests()
    configuration_getter = MockedConfigurationGetter()

    request_maker = OpencachingRequestMaker(requests, configuration_getter)
    payload = {
        'some': 'data',
        'foo': 'bar',
    }
    response = request_maker.post('/some/url', data=payload)

    assert requests.get_mocked_response() == response.text


def test_return_cookies_from_post_request():
    requests = MockedPostRequests()
    configuration_getter = MockedConfigurationGetter()

    request_maker = OpencachingRequestMaker(requests, configuration_getter)
    payload = {
        'some': 'data',
        'foo': 'bar',
    }
    response = request_maker.post('/some/url', data=payload)

    assert requests.get_mocked_cookies() == response.cookies


class TestIOpencachingRequestMaker:
    def test_raise_on_post(self):
        with pytest.raises(NotImplementedError):
            IOpencachingRequestMaker().post(url='ddd', data={'a': '123'})

    def test_raise_on_get_opencaching_base_url(self):
        with pytest.raises(NotImplementedError):
            IOpencachingRequestMaker().get_opencaching_base_url()
