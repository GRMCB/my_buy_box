from database.models import ListingRecord, db
import os
from flask import Flask
import logging
import atexit
import json
from apscheduler.schedulers.background import BackgroundScheduler
from redfin import Redfin
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)

def load_user_listing_criteria():
    cur_path = os.path.dirname("listing_criteria.json")
    user_data_path = os.path.relpath('user_data/listing_criteria.json', cur_path)

    with open(user_data_path) as listing_criteria:
        user_search_criteria = json.load(listing_criteria)
        return user_search_criteria
def get_all_user_listings():
    with app.app_context():

        logger.info("Running get_all_user_listings() function to get listings from Redfin");
        user_search_criteria = load_user_listing_criteria()
        all_listings = []

        for zipcode, search_params in user_search_criteria["zip_code"].items():
            zipcode_listings = client.search_all_by_zipcode(zipcode, search_params["REDFIN_SEARCH_PARAMETERS"])

            all_listings.extend(zipcode_listings)

        print(all_listings)
        save_listings_to_database(all_listings)
        return all_listings

def save_listings_to_database(all_listings):
    for listing in all_listings:
        listing_record = ListingRecord(
            id=int(listing['MLS#']),
            sale_type=listing['SALE TYPE'],
            sold_date=listing['SOLD DATE'],
            property_type=listing['PROPERTY TYPE'],
            address=listing['ADDRESS'],
            city=listing['CITY'],
            state_or_province=listing['STATE OR PROVINCE'],
            zip_or_postal_code=listing['ZIP OR POSTAL CODE'],
            price=float(listing['PRICE']),
            beds=int(listing['BEDS']),
            baths=float(listing['BATHS']),
            location=listing['LOCATION'],
            square_feet=int(listing['SQUARE FEET']),
            lot_size=int(listing['LOT SIZE']),
            year_built=int(listing['YEAR BUILT']),
            days_on_market=int(listing['DAYS ON MARKET']),
            price_per_square_feet=float(listing['$/SQUARE FEET']),
            hoa_per_month=float(listing['HOA/MONTH']),
            status=listing['STATUS'],
            next_open_house_start_time=listing['NEXT OPEN HOUSE START TIME'],
            next_open_house_end_time=listing['NEXT OPEN HOUSE END TIME'],
            url=listing['URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)'],
            source=listing['SOURCE'],
            mls_number=int(listing['MLS#']),
            favorite=bool(listing['FAVORITE']),
            interested=bool(listing['INTERESTED']),
            latitude=float(listing['LATITUDE']),
            longitude=float(listing['LONGITUDE'])
        )
        db.session.add(listing_record)
        db.session.commit()

        print(get_listings(db.session))
        app.logger.warning(())

app = Flask(__name__)
client = Redfin()

scheduler = BackgroundScheduler()
scheduler.add_job(func=get_all_user_listings, trigger="interval", seconds=10)
scheduler.start()

db_path = os.path.join(os.path.dirname(__file__), 'database', 'database.db')

with app.app_context():

    logger.info("Running with app.app_context():");

    app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    db.create_all()

@app.route("/api/listings/<zip_code>", methods = ['GET'])
def get_listings(zip_code):
    """Get a list of listings objects sorted by MLS number"""
    listings = ListingRecord.query(ListingRecord).filter(ListingRecord.zip_or_postal_code == zip_code).order_by(ListingRecord.mls_number).all()
    return listings

if __name__ == '__main__':
    load_dotenv()

    logger.info("Running if __name__ == '__main__'");

    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

    app.run(debug=True, host='0.0.0.0')

    atexit.register(scheduler.shutdown)
