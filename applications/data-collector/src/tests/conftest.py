import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../main")))
from main.app import app
import pytest
import json

os.environ['PYTHONPATH'] = '/var/www/webapp/applications/data-collector/src/main/'
TEST_DATA_PATH = "/applications/data-collector/src/tests/test_data/test_listing_criteria.json"

@pytest.fixture
def load_test_listing_criteria():
    cur_path = os.path.dirname("test_data/")
    test_data_path = os.path.relpath(cur_path,TEST_DATA_PATH )
    cwd = os.getcwd()  # Get the current working directory (cwd)
    path = cwd + TEST_DATA_PATH

    with open(path) as listing_criteria:
        test_search_criteria = json.load(listing_criteria)

        return test_search_criteria


@pytest.fixture
def app_test_client():
    with app.test_client() as test_client:
        yield test_client