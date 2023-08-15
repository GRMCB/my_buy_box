import pytest
import app
TEST_DATA_PATH = "test_data/listing_criteria.json"

@pytest.fixture
def load_test_listing_criteria():
    cur_path = os.path.dirname("listing_criteria.json")
    test_data_path = os.path.relpath(TEST_DATA_PATH, cur_path)

    with open(test_data_path) as listing_criteria:
        test_search_criteria = json.load(listing_criteria)

    return test_search_criteria

@pytest.fixture
def load_valid_zipcodes():
    cur_path = os.path.dirname("valid_zipcodes.json")
    test_data_path = os.path.relpath(TEST_DATA_PATH, cur_path)

    with open(test_data_path) as zipcodes:
        valid_zipcodes = json.load(zipcodes)

    return valid_zipcodes

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
