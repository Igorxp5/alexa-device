import os

import dotenv
import pytest


@pytest.fixture(scope='session', autouse=True)
def load_env():
    env_file = dotenv.find_dotenv('.test.env')
    dotenv.load_dotenv(env_file)


@pytest.fixture
def avs_client_id():
    return os.environ['AVS_CLIENT_ID']


@pytest.fixture
def avs_product_id():
    return os.environ['AVS_PRODUCT_ID']


@pytest.fixture
def avs_device_serial_number():
    return os.environ['AVS_DEVICE_SERIAL_NUMBER']


@pytest.fixture
def avs_refresh_token():
    return os.environ['AVS_REFRESH_TOKEN']
