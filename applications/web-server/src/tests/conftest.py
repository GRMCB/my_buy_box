import os

os.environ['PYTHONPATH'] = '/var/www/webapp/applications/web-server/src/main/'

from main.app import app
import pytest
import json



@pytest.fixture
def app_test_client():

    with app.test_client() as test_client:
        yield test_client

@pytest.fixture
def load_valid_zipcodes():
    cur_path = os.path.dirname(os.path.abspath(__file__))
    test_data_path = os.path.join(cur_path, 'test_data/test_valid_zipcodes.json')

    with open(test_data_path) as zipcodes:
        valid_zipcodes = json.load(zipcodes)

    return valid_zipcodes