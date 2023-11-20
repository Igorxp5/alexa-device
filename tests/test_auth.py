from alexa_device.client.auth import AlexaAuthentication

def test_request_access_token(avs_client_id, avs_product_id, avs_device_serial_number):
    auth = AlexaAuthentication(avs_client_id, avs_product_id, avs_device_serial_number)
    access_grant = auth.request_access_token()

    assert access_grant.access_token
    assert access_grant.refresh_token
    assert access_grant.expires_in == 3600
    assert access_grant.token_type == 'bearer'
    assert not access_grant.is_expired()


def test_refresh_token(avs_client_id, avs_product_id, avs_device_serial_number,
                                  avs_refresh_token):
    auth = AlexaAuthentication(avs_client_id, avs_product_id, avs_device_serial_number,
                               refresh_token=avs_refresh_token)
    access_grant = auth.request_access_token()

    assert access_grant.access_token
    assert access_grant.refresh_token == avs_refresh_token
    assert access_grant.expires_in == 3600
    assert access_grant.token_type == 'bearer'
    assert not access_grant.is_expired()
