import os
from flask import Flask
import logging
import atexit
import time
import json
from apscheduler.schedulers.background import BackgroundScheduler
from redfin import Redfin
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
# from components.listings.src.main.listing_record import ListingRecord
from components.listings.src.main.listing_db import Database

logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)

class ListingRecord(db.Model):
    __tablename__ = 'listing_records'
    id = db.Column(db.Integer, primary_key=True)
    sale_type = db.Column(db.String(50))
    sold_date = db.Column(db.String(50))
    property_type = db.Column(db.String(50))
    address = db.Column(db.String(100))
    city = db.Column(db.String(50))
    state_or_province = db.Column(db.String(50))
    zip_or_postal_code = db.Column(db.String(50))
    price = db.Column(db.Float)
    beds = db.Column(db.Integer)
    baths = db.Column(db.Float)
    location = db.Column(db.String(50))
    square_feet = db.Column(db.Integer)
    lot_size = db.Column(db.Integer)
    year_built = db.Column(db.Integer)
    days_on_market = db.Column(db.Integer)
    price_per_square_feet = db.Column(db.Float)
    hoa_per_month = db.Column(db.Float)
    status = db.Column(db.String(50))
    next_open_house_start_time = db.Column(db.String(50))
    next_open_house_end_time = db.Column(db.String(50))
    url = db.Column(db.String(200))
    source = db.Column(db.String(50))
    mls_number = db.Column(db.Integer)
    favorite = db.Column(db.String(1))
    interested = db.Column(db.String(1))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return f'<Student {self.id}>'
def load_user_listing_criteria():
    cur_path = os.path.dirname("listing_criteria.json")
    user_data_path = os.path.relpath('user_data/listing_criteria.json', cur_path)

    with open(user_data_path) as listing_criteria:
        user_search_criteria = json.load(listing_criteria)
        return user_search_criteria
def get_all_user_listings():
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

        print(listing_record.id)

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
client = Redfin()

app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = Database(app)
db.create_all()

if __name__ == '__main__':
    load_dotenv()

    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

    scheduler = BackgroundScheduler()
    scheduler.add_job(func=get_all_user_listings, trigger="interval", seconds=5)
    scheduler.start()

    app.run(debug=True, host='0.0.0.0')

    atexit.register(scheduler.shutdown)
