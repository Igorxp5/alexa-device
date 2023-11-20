import json

import requests

from ..models.auth import CodePairRequest, AccessGrant
from ..exceptions.auth import CodePairError, AccessGrantError, MissingCodePair


class AlexaAuthentication:
    AUTH_BASE_URL = 'https://api.amazon.com'
    AUTH_CODE_PAIR_URL = AUTH_BASE_URL + '/auth/O2/create/codepair'
    AUTH_TOKEN_URL = AUTH_BASE_URL + '/auth/O2/token'

    def __init__(self, client_id: str, product_id: str, device_serial_number: str,
                 refresh_token: str = None):
        self._client_id = client_id
        self._product_id = product_id
        self._device_serial_number = device_serial_number

        self._code_pair: CodePairRequest | None = None

        self._access_grant: AccessGrant | None = None

        if refresh_token:
            self._access_grant = AccessGrant(refresh_token=refresh_token)

    @property
    def client_id(self) -> str:
        return self._client_id
    
    @property
    def product_id(self) -> str:
        return self._product_id
    
    @property
    def device_serial_number(self) -> str:
        return self._device_serial_number

    @property
    def authorization_header(self):
        return f'Bearer {self._access_grant.access_token}'

    def is_expired(self):
        return not self._access_grant or self._access_grant.is_expired()

    def request_code_pair(self) -> CodePairRequest:
        response = requests.post(self.AUTH_CODE_PAIR_URL, data=self.build_code_pair_payload())
        if response.status_code == 200:
            self._code_pair = CodePairRequest(**response.json())
            return self._code_pair
        raise CodePairError(response)
    
    def request_access_token(self) -> AccessGrant:
        response = requests.post(self.AUTH_TOKEN_URL, data=self.build_request_token_payload())
        if response.status_code == 200:
            self._access_grant = AccessGrant(**response.json())
            return self._access_grant
        raise AccessGrantError(response)

    def build_scope_data(self) -> dict:
        return {
            'alexa:all': {
                'productID': self.product_id, 
                'productInstanceAttributes':{
                    'deviceSerialNumber': self.device_serial_number
                }
            }
        }

    def build_code_pair_payload(self) -> dict:
        return {
            'response_type': 'device_code',
            'client_id': self.client_id,
            'scope': 'alexa:all',
            'scope_data': json.dumps(self.build_scope_data())
        }

    def build_request_token_payload(self) -> dict:
        if self._access_grant and self._access_grant.refresh_token:
            return {
                'grant_type': 'refresh_token',
                'refresh_token': self._access_grant.refresh_token,
                'client_id': self.client_id
            }

        if not self._code_pair:
            raise MissingCodePair

        return {
            'grant_type': 'device_code',
            'device_code': self._code_pair.device_code,
            'user_code': self._code_pair.user_code
        }
