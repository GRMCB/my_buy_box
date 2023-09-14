from database.models import ListingRecord, db
import os
import logging
import atexit
import json
from apscheduler.schedulers.background import BackgroundScheduler
from redfin import Redfin
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask import Flask
from config import Config

logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    from database.models import db
    db.init_app(app)

    return app

def load_user_listing_criteria():
    cur_path = os.path.dirname("listing_criteria.json")
    user_data_path = os.path.relpath('user_data/listing_criteria.json', cur_path)

    with open(user_data_path) as listing_criteria:
        user_search_criteria = json.load(listing_criteria)
        return user_search_criteria

def get_all_listings_from_collector_database():
    with app.app_context():

        logger.info("Running get_all_listings_from_collector_database() function to get listings from Data Collector App");

        all_listings = []

        # Call Database Rest API to get Zip code listings
        records = requests.get(f"http://127.0.0.1:8081/api/listings")
        json_records = json.loads(records.text)

        for zipcode, search_params in user_search_criteria["zip_code"].items():
            zipcode_listings = client.search_all_by_zipcode(zipcode, search_params["REDFIN_SEARCH_PARAMETERS"])

            all_listings.extend(zipcode_listings)

        return all_listings

def get_rental_estimate(listing):
    base_url = "https://www.redfin.com/rental-estimate?propertyId="

    property_id = listing

    rental_estimate = requests.get(base_url + property_id)

    return rental_estimate 

def analyze_all_listings():

    user_listings = []

    all_listings = get_all_listings_from_collector_database()

    for listing in all_listings:
        rental_estimate = get_rental_estimate(listing)

        if ((rental_estimate/listing["Price"]) * 100) >= 0.60:
            user_listings.append(listing)

    save_listings_to_analyzer_database(user_listings)

def save_listings_to_analyzer_database(user_listings):
    for listing in user_listings:
        listing_record = ListingRecord(
            id=listing['MLS#'],
            sale_type=listing['SALE TYPE'],
            sold_date=listing['SOLD DATE'],
            property_type=listing['PROPERTY TYPE'],
            address=listing['ADDRESS'],
            city=listing['CITY'],
            state_or_province=listing['STATE OR PROVINCE'],
            zip_or_postal_code=listing['ZIP OR POSTAL CODE'],
            price=listing['PRICE'],
            beds=listing['BEDS'],
            baths=listing['BATHS'],
            location=listing['LOCATION'],
            square_feet=listing['SQUARE FEET'],
            lot_size=listing['LOT SIZE'],
            year_built=listing['YEAR BUILT'],
            days_on_market=listing['DAYS ON MARKET'],
            price_per_square_feet=listing['$/SQUARE FEET'],
            hoa_per_month=listing['HOA/MONTH'],
            status=listing['STATUS'],
            next_open_house_start_time=listing['NEXT OPEN HOUSE START TIME'],
            next_open_house_end_time=listing['NEXT OPEN HOUSE END TIME'],
            url=listing['URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)'],
            source=listing['SOURCE'],
            mls_number=listing['MLS#'],
            favorite=bool(listing['FAVORITE']),
            interested=bool(listing['INTERESTED']),
        )
        db.session.add(listing_record)
        db.session.commit()

db_path = os.path.join(os.path.dirname(__file__), 'database', 'analyzer_database.db')

app = create_app()
migrate = Migrate(app, db, directory=db_path)


scheduler = BackgroundScheduler()
scheduler.add_job(func=get_all_listings_from_collector_database, trigger="interval", seconds=10)
scheduler.start()

with app.app_context():

    logger.info("Running with app.app_context():")
    # db.create_all()

@app.route("/api/listings/<zip_code>", methods = ['GET'])
def get_listings(zip_code):
    """Get a list of listings objects sorted by MLS number"""
    listings = db.session.query(ListingRecord).filter(ListingRecord.zip_or_postal_code == zip_code).order_by(ListingRecord.mls_number).all()

    return ListingRecord.serialize_list(listings)

if __name__ == '__main__':
    load_dotenv()

    logger.info("Running if __name__ == '__main__'");

    app.run(debug=True, host='0.0.0.0')

    atexit.register(scheduler.shutdown)
