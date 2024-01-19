import re
import time

import jwt
import requests
from terevintosoftware.pkce_client import PkceClient, PkceLoginConfig
from terevintosoftware.pkce_client.token_config_map import TokenConfigMap
import socket


def _is_token_expired(token: str) -> bool:
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        if 'exp' in decoded:
            exp_time = decoded['exp']
            current_time = time.time()
            # time in seconds
            return current_time - 30 > exp_time
        return False
    except jwt.DecodeError:
        raise
    except jwt.ExpiredSignatureError:
        return True


def _get_azure_storage_url(account: str, container: str) -> str:
    """Generates an Azure blob storage url.

    Parameters:
        account (str): the Azure storage account name
        container (str): the Azure storage container name

    Returns:
        str: Azure blob storage url
    """

    return f'https://{account}.blob.core.windows.net/{container}'


def _sanitize_url(url: str) -> str:
    """
    handles multiple slashes in url by replacing them with a single slash, while keeping the double slashes after protocol scheme
    :param url:
    :return:
        sanitized url
    """
    parts = url.split('://')
    result = parts[0] + '://' + re.sub('//+', '/', parts[1])
    return result


def _find_free_port():
    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Bind the socket to a random port
            s.bind(('', 0))

            # Get the port number
            _, port = s.getsockname()

            return port
        except OSError as e:
            raise EnvironmentError(f"Unable to lookup free port: {e}")
        finally:
            # Close the socket
            s.close()


class TokenHolder:
    def __init__(self, **kwargs: str) -> None:
        self.domain = kwargs['domain']
        self.realm = kwargs['realm']
        self.client_id = kwargs['client_id']
        self.access_token = kwargs.get('access_token', '')
        self.refresh_token = kwargs.get('refresh_token', '')

    def get_tokens_with_credentials(self, username, password) -> None:
        data = {
            "grant_type": "password",
            "client_id": self.client_id,
            "username": username,
            "password": password
        }
        response = requests.post(f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token', data=data)
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        self.refresh_token = response.json()["refresh_token"]

    def get_tokens_by_authflow(self) -> None:

        config = PkceLoginConfig(
            authorization_uri=f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/auth',
            token_uri=f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token',
            scopes=["openid"],
            client_id=self.client_id,
            internal_port=_find_free_port(),
            add_random_state=True,
            random_state_length=32,
            verify_authorization_server_https=False,
            token_config_map=TokenConfigMap(scopes='scope'))

        login_client = PkceClient(config)
        pkce_token = login_client.login()
        self.access_token = pkce_token.access_token
        self.refresh_token = pkce_token.refresh_token

    def _refresh_tokens(self):
        payload = f'grant_type=refresh_token&refresh_token={self.refresh_token}&client_id={self.client_id}'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(f'https://{self.domain}/auth/realms/{self.realm}/protocol/openid-connect/token', headers=headers, data=payload)
        response.raise_for_status()
        self.access_token = response.json()["access_token"]
        self.refresh_token = response.json()["refresh_token"]

    def get_token(self) -> str:
        if _is_token_expired(self.access_token):
            self._refresh_tokens()
        return self.access_token
