import pytest
from redfin import Redfin

# def test_valid_zipcode():

def test_search_all_by_zipcode():
    test_zipcode = load_test_listing_criteria["zip_code"]
    zipcode_listing = client.search_all_by_zipcode(test_zipcode, search_params["REDFIN_SEARCH_PARAMETERS"])

    assert zipcode_listing == test_zipcode