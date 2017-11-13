from typing import Dict

from downloader.shell_variables_configuration_getter import \
    IConfigurationGetter

RequestData = Dict[str, str]
Cookies = Dict[str, str]


class RequestMakerResponse:
    def __init__(self, text: str, cookies: Cookies):
        self.text = text
        self.cookies = cookies


class IOpencachingRequestMaker:
    def post(self, url: str, data: RequestData) -> RequestMakerResponse:
        raise NotImplementedError

    def get_opencaching_base_url(self) -> str:
        raise NotImplementedError


class OpencachingRequestMaker(IOpencachingRequestMaker):
    def __init__(
            self, requests, configuration_getter: IConfigurationGetter
    ) -> None:
        self._requests = requests
        self._opencaching_base_url = self._remove_last_slash_from_url(
            configuration_getter.get_opencaching_base_url()
        )

    @staticmethod
    def _remove_last_slash_from_url(url: str) -> str:
        if url[-1] == '/':
            return url[:-1]

        return url

    def post(self, url: str, data: RequestData) -> RequestMakerResponse:
        response = self._requests.post(
            f'{self._opencaching_base_url}{url}',
            data=data
        )

        return RequestMakerResponse(
            text=response.text,
            cookies=response.cookies,
        )

    def get_opencaching_base_url(self) -> str:
        return self._opencaching_base_url
