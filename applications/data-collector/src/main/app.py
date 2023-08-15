from flask import Flask
import logging
import atexit
import time
import json
from apscheduler.schedulers.background import BackgroundScheduler
import os
from redfin import Redfin

logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)

all_listings = []
def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

def load_user_listing_criteria():
    cur_path = os.path.dirname("listing_criteria.json")
    user_data_path = os.path.relpath('user_data/listing_criteria.json', cur_path)

    with open(user_data_path) as listing_criteria:
        user_search_criteria = json.load(listing_criteria)
        return user_search_criteria
def get_all_user_listings():
    user_search_criteria = load_user_listing_criteria()

    for zipcode, search_params in user_search_criteria["zip_code"].items():
        zipcode_listings = client.search_all_by_zipcode(zipcode, search_params["REDFIN_SEARCH_PARAMETERS"])

        all_listings.extend(zipcode_listings)

    print(all_listings)
    return all_listings


app = Flask(__name__)
client = Redfin()

scheduler = BackgroundScheduler()
scheduler.add_job(func=get_all_user_listings, trigger="interval", seconds=5)
scheduler.start()

atexit.register(scheduler.shutdown)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')