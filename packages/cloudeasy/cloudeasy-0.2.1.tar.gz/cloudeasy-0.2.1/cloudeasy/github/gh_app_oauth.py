from typing import TypedDict
from urllib.parse import urlencode

import requests


class AccessToken(TypedDict):
    access_token: str
    expires_in: int
    refresh_token: str
    token_type: str
    refresh_token_expires_in: int
    scope: str


class GithubAppOAuth:
    def __init__(self, client_id, client_secret, web='https://github.com', api='https://api.github.com'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.api = api
        self.gh_headers = {
            "Accept": "application/vnd.github+json",
            "Content-Type": "application/json",
        }
        self.authorization_base_url = f'{web}/login/oauth/authorize'
        self.token_url = f'{web}/login/oauth/access_token'

    def build_auth_url(self, redirect_uri=None, state=None) -> str:
        url_params = {
            "client_id": self.client_id
        }
        if redirect_uri:
            url_params['redirect_uri'] = redirect_uri
        if state:
            url_params['state'] = state

        return f"{self.authorization_base_url}?{urlencode(url_params)}"

    def get_access_token(self, code: str) -> AccessToken:
        access_response = requests.post(self.token_url, params={
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code
        }, headers=self.gh_headers)
        return access_response.json()

        return token
