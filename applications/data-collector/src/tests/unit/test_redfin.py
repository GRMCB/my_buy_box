import pytest
from main.redfin import Redfin

def test_search_all_by_zipcode(load_test_listing_criteria):
    """ This test validates the search_all_by_zipcode function in the Redfin API.
    It tests that the zipcode for the returned list of listings matches the test_listing_criteria.json file """

    # Create Redfin API Client used for testing listing criteria against
    client = Redfin()

    test_zipcode = list(load_test_listing_criteria['zip_code'].keys())[0]
    test_search_params = load_test_listing_criteria["zip_code"][test_zipcode]["REDFIN_SEARCH_PARAMETERS"]
    zipcode_listings = client.search_all_by_zipcode(test_zipcode, test_search_params)

    for listing in zipcode_listings:
        assert listing["ZIP OR POSTAL CODE"] == test_zipcode