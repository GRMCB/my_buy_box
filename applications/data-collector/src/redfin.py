import requests
import json
import csv
import io
import urllib

class Redfin:
    # api/gis-search/ endpoint no longer exists - Must use gis-csv
    SEARCH_URL = 'api/gis-csv'
    REGION_URL = 'api/region'
    INITIAL_INFO_URL = "api/home/details/initialInfo"

    # https://github.com/alientechsw/RedfinPlus/blob/master/docs/REDFIN.md
    SEARCH_PARAMS = {
        "al":1,
        "status":1,
        "region_id":29439,
        "uipt":1,
        "sp":True,
        "region_type":2,
        "page_number":1,
        "v":8,
        "min_parcel_size":5000,
        "num_homes":500,
        "min_price":500000,
        "max_price":1500000,
        "min_num_beds":3,
        "min_num_baths":2,
        "gar":True,
        "min_num_park":2
    }



    def __init__(self):
        self.base = 'https://www.redfin.com/stingray/'
        self.user_agent_header = {
            'user-agent': 'redfin'
        }


    def meta_property(self, url, kwargs, page=False):
        if page:
            kwargs['pageType'] = 3
        return self.meta_request('api/home/details/' + url, {
            'accessLevel': 1,
            **kwargs
        })

    def meta_request(self, url, kwargs):
        print(self.base + url)
        response = requests.get(
            self.base + url, params=kwargs, headers=self.user_agent_header)
        response.raise_for_status()
        return json.loads(response.text[4:])

    def raw_request(self, url, kwargs):
        print(self.base + url)

        response = requests.get(
            self.base + url, params=kwargs, headers=self.user_agent_header)
        response.raise_for_status()
        json_response = self.csv_to_json_dict(response.text)

        return json_response

    # Url Requests

    def initial_info(self, url, **kwargs):
        return self.meta_request('api/home/details/initialInfo', {'path': url, **kwargs})

    def page_tags(self, url, **kwargs):
        return self.meta_request('api/home/details/v1/pagetagsinfo', {'path': url, **kwargs})

    def primary_region(self, url, **kwargs):
        return self.meta_request('api/home/details/primaryRegionInfo', {'path': url, **kwargs})

    # Search
    def search(self, query, **kwargs):
        return self.meta_request('do/location-autocomplete', {'location': query, 'v': 2, **kwargs})

    # Convert Zip Code to Region ID
    def zipcode_to_regionid(self, zip_code, **kwargs):
        params = {
            "region_id": zip_code,
            "region_type": 2,
            "tz": True,
            "v": 8
        }
        response = self.meta_request(Redfin.REGION_URL, params)
        region_id = response["payload"]["rootDefaults"]["region_id"]

        return region_id

    # Search All
    def search_all_by_zipcode(self, zip_code, search_params, **kwargs):
        region_id = self.zipcode_to_regionid(zip_code)
        search_json = {}
        # Replace Zipcode with Region ID in region_id field
        search_json["region_id"] = [region_id]
        params = dict(search_params, **search_json)
        SEARCH_URL = self.createURL(Redfin.SEARCH_URL, params)

        return self.raw_request(SEARCH_URL, params)

    # Property ID Requests
    def below_the_fold(self, property_id, **kwargs):
        return self.meta_property('belowTheFold', {'propertyId': property_id, **kwargs}, page=True)

    def hood_photos(self, property_id, **kwargs):
        return self.meta_request('api/home/details/hood-photos', {'propertyId': property_id, **kwargs})

    def more_resources(self, property_id, **kwargs):
        return self.meta_request('api/home/details/moreResourcesInfo', {'propertyId': property_id, **kwargs})

    def page_header(self, property_id, **kwargs):
        return self.meta_request('api/home/details/homeDetailsPageHeaderInfo', {'propertyId': property_id, **kwargs})

    def property_comments(self, property_id, **kwargs):
        return self.meta_request('api/v1/home/details/propertyCommentsInfo', {'propertyId': property_id, **kwargs})

    def building_details_page(self, property_id, **kwargs):
        return self.meta_request('api/building/details-page/v1', {'propertyId': property_id, **kwargs})

    def owner_estimate(self, property_id, **kwargs):
        return self.meta_request('api/home/details/owner-estimate', {'propertyId': property_id, **kwargs})

    def claimed_home_seller_data(self, property_id, **kwargs):
        return self.meta_request('api/home/details/claimedHomeSellerData', {'propertyId': property_id, **kwargs})

    def cost_of_home_ownership(self, property_id, **kwargs):
        return self.meta_request('do/api/costOfHomeOwnershipDetails', {'propertyId': property_id, **kwargs})

    # Listing ID Requests
    def floor_plans(self, listing_id, **kwargs):
        return self.meta_request('api/home/details/listing/floorplans', {'listingId': listing_id, **kwargs})

    def tour_list_date_picker(self, listing_id, **kwargs):
        return self.meta_request('do/tourlist/getDatePickerData', {'listingId': listing_id, **kwargs})

    # Table ID Requests

    def shared_region(self, table_id, **kwargs):
        return self.meta_request('api/region/shared-region-info', {'tableId': table_id, 'regionTypeId': 2, 'mapPageTypeId': 1, **kwargs})

    # Property Requests

    def similar_listings(self, property_id, listing_id, **kwargs):
        return self.meta_property('similars/listings', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def similar_sold(self, property_id, listing_id, **kwargs):
        return self.meta_property('similars/solds', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def nearby_homes(self, property_id, listing_id, **kwargs):
        return self.meta_property('nearbyhomes', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def above_the_fold(self, property_id, listing_id, **kwargs):
        return self.meta_property('aboveTheFold', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def property_parcel(self, property_id, listing_id, **kwargs):
        return self.meta_property('propertyParcelInfo', {'propertyId': property_id, 'listingId': listing_id, **kwargs}, page=True)

    def activity(self, property_id, listing_id, **kwargs):
        return self.meta_property('activityInfo', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def customer_conversion_info_off_market(self, property_id, listing_id, **kwargs):
        return self.meta_property('customerConversionInfo/offMarket', {'propertyId': property_id, 'listingId': listing_id, **kwargs}, page=True)

    def rental_estimate(self, property_id, listing_id, **kwargs):
        return self.meta_property('rental-estimate', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def avm_historical(self, property_id, listing_id, **kwargs):
        return self.meta_property('avmHistoricalData', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def info_panel(self, property_id, listing_id, **kwargs):
        return self.meta_property('mainHouseInfoPanelInfo', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def descriptive_paragraph(self, property_id, listing_id, **kwargs):
        return self.meta_property('descriptiveParagraph', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def avm_details(self, property_id, listing_id, **kwargs):
        return self.meta_property('avm', {'propertyId': property_id, 'listingId': listing_id, **kwargs})

    def tour_insights(self, property_id, listing_id, **kwargs):
        return self.meta_property('tourInsights', {'propertyId': property_id, 'listingId': listing_id, **kwargs}, page=True)

    def stats(self, property_id, listing_id, region_id, **kwargs):
        return self.meta_property('stats', {'regionId': region_id, 'propertyId': property_id, 'listingId': listing_id, 'regionTypeId': 2, **kwargs})

    @staticmethod
    def createURL(url, params={}):
        url_params = urllib.parse.urlencode(params, doseq=True)
        url = "%s?%s" % (url, url_params)

        return url

    @staticmethod
    def csv_to_json_dict(csv_string):
        reader = csv.DictReader(io.StringIO(csv_string))
        json_data = json.dumps(list(reader))
        json_dict = json.loads(json_data)

        return json_dict

