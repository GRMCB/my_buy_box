from database.models import ListingRecord, db
import os
import re
import logging
import atexit
import json
from apscheduler.schedulers.background import BackgroundScheduler
from redfin import Redfin
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask import Flask, render_template
from config import Config
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    from database.models import db
    db.init_app(app)

    return app

def get_all_listings_from_collector_database():

    logger.info("Running get_all_listings_from_collector_database() function to get listings from Data Collector App");

    all_listings = []

    # Call Database Rest API to get Zip code listings
    records = requests.get(f"http://127.0.0.1:8081/api/listings")
    print(records)
    json_records = json.loads(records.text)

    for listing in json_records:
        print(listing)
        all_listings.append(listing)

    return all_listings

def get_rental_estimate(listing):
    pattern = r"([^/]+)$"
    base_url = "https://www.redfin.com/rental-estimate?propertyId="

    property_id = re.search(pattern, listing["url"]).group(1)

    # Get the Redfin Rental Estimate from the HTML response
    response = requests.get(base_url + property_id)
    # soup = BeautifulSoup(response, 'html.parser')
    pattern = r'"rentalEstimateInfo\\":{[^}]*"predictedValue\\":(\d+)'
    rental_estimate = re.findall(pattern, response.text)

    if rental_estimate:
        return rental_estimate[0]
    else:
        return None 

def analyze_all_listings():
    with app.app_context():
        user_listings = []

        all_listings = get_all_listings_from_collector_database()
        print(all_listings)
        for listing in all_listings:
            rental_estimate = get_rental_estimate(listing)
            print("RENTAL ESTIMATE:{}".format(rental_estimate))

            if rental_estimate:

                if ((int(rental_estimate)/int(listing["price"])) * 100) >= 0.60:
                    user_listings.append(listing)

        save_listings_to_analyzer_database(user_listings)

def save_listings_to_analyzer_database(user_listings):
    for listing in user_listings:
        listing_record = ListingRecord(
            id=listing["mls_number"],
            sale_type=listing["sale_type"],
            sold_date=listing["sold_date"],
            property_type=listing["property_type"],
            address=listing["address"],
            city=listing["city"],
            state_or_province=listing["state_or_province"],
            zip_or_postal_code=listing["zip_or_postal_code"],
            price=listing["price"],
            beds=listing["beds"],
            baths=listing["baths"],
            location=listing["location"],
            square_feet=listing["square_feet"],
            lot_size=listing["lot_size"],
            year_built=listing["year_built"],
            days_on_market=listing["days_on_market"],
            price_per_square_feet=listing["price_per_square_feet"],
            hoa_per_month=listing["hoa_per_month"],
            status=listing["status"],
            next_open_house_start_time=listing["next_open_house_start_time"],
            next_open_house_end_time=listing["next_open_house_end_time"],
            url=listing["url"],
            source=listing["source"],
            mls_number=listing["mls_number"],
            favorite=bool(listing["favorite"]),
            interested=bool(listing["interested"]),
        )
        db.session.add(listing_record)
        db.session.commit()

db_path = os.path.join(os.path.dirname(__file__), 'database', 'analyzer_database.db')

app = create_app()
migrate = Migrate(app, db, directory=db_path)


scheduler = BackgroundScheduler()
scheduler.add_job(func=analyze_all_listings, trigger="interval", seconds=10)
scheduler.start()

with app.app_context():

    logger.info("Running with app.app_context():")
    db.create_all()

@app.route("/api/listings/<zip_code>", methods = ['GET'])
def get_listings_by_zipcode(zip_code):
    """ Get a list of listings objects sorted by MLS number """
    listings = db.session.query(ListingRecord).filter(ListingRecord.zip_or_postal_code == zip_code).order_by(ListingRecord.mls_number).all()

    return ListingRecord.serialize_list(listings)

@app.route("/api/listings", methods = ['GET'])
def get_all_listings():
    """ Get all listings from the collector database """
    listings = db.session.query(ListingRecord).all()

    return ListingRecord.serialize_list(listings)

@app.route('/health', methods = ['GET'])
def health():

    resp = "Data Analyzer app is Healthy"

    return render_template('health.html', resp=resp)

if __name__ == '__main__':
    load_dotenv()

    logger.info("Running if __name__ == '__main__'");

    app.run(debug=True, host='0.0.0.0')

    atexit.register(scheduler.shutdown)
