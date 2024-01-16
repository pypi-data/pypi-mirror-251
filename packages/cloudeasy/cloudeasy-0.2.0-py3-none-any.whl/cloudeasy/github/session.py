import logging

import requests

logger = logging.getLogger(__name__)


class Session:
    def __init__(self, token, api="https://api.github.com"):
        """
        :param token: pat or access token
        :param api: GitHub API
        """
        self.api = api
        self._access_token = token
        self.session = requests.Session()

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value

    @property
    def headers(self):
        return {
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self.access_token
        }

    def _request(self, method, path, **kwargs):
        _req = self.session.request(method, f"{self.api}/{path}", **kwargs, headers=self.headers)
        match _req.status_code:
            case 200:
                return _req.json()
            case 204:
                return True
            case _:
                data = _req.json()
                logger.error(_req)
                raise Exception(f"failed to access \"{_req.url}\", {data['message']},see {data['documentation_url']}")

    def get(self, path, **kwargs):
        return self._request('GET', path, **kwargs)

    def post(self, path, **kwargs):
        return self._request('POST', path, **kwargs)

    def put(self, path, **kwargs):
        return self._request('PUT', path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request('DELETE', path, **kwargs)
