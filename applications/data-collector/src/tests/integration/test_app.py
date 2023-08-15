import pytest
import app

def test_get_all_user_listings():
    user_search_criteria = load_user_listing_criteria()

    for zipcode, search_params in user_search_criteria["zip_code"].items():
        zipcode_listings = client.search_all_by_zipcode(zipcode, search_params["REDFIN_SEARCH_PARAMETERS"])

        all_listings.extend(zipcode_listings)

    print(all_listings)
    return all_listings