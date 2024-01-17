import functools
from base64 import b64encode
from typing import TypedDict

from nacl import encoding, public

from cloudeasy.github.session import Session


class RepoPublicKey(TypedDict):
    key_id: str
    key: str


def secret_encrypt(public_key: str, secret_value: str) -> str:
    """
    https://docs.github.com/en/rest/actions/secrets?apiVersion=2022-11-28#create-or-update-a-repository-secret
    :param public_key:
    :param secret_value:
    :return:
    """
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder)
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


class RepoSecret(Session):

    def list_repo_secrets(self, owner, repo_name):
        return self.get(f"repos/{owner}/{repo_name}/actions/secrets")

    @functools.lru_cache(maxsize=256)
    def get_repo_public_key(self, owner, repo_name) -> RepoPublicKey:
        return self.get(f"repos/{owner}/{repo_name}/actions/secrets/public-key")

    def get_repo_secret(self, owner, repo_name, secret_name):
        return self.get(f"repos/{owner}/{repo_name}/actions/secrets/{secret_name}")

    def delete_repo_secrets(self, owner, repo_name, secret_name):
        return self.delete(f"repos/{owner}/{repo_name}/actions/{secret_name}")

    def put_repo_secrets(self, owner, repo_name, secret_name, data, encrypted_key_id, public_key) -> bool:
        encrypted_value = secret_encrypt(public_key, data)
        return self.put(f"repos/{owner}/{repo_name}/actions/secrets/{secret_name}", json={
            "encrypted_value": encrypted_value,
            "key_id": encrypted_key_id
        })

    def set_repo_secret(self, owner, repo_name, secret_name, secret_value) -> bool:
        public_key = self.get_repo_public_key(owner, repo_name)
        return self.put_repo_secrets(owner, repo_name, secret_name, secret_value, public_key['key_id'], public_key['key'])


class OrgSecret(Session):
    def list_organization_secrets(self, org_name):
        return self.get(f"orgs/{org_name}/actions/secrets")
