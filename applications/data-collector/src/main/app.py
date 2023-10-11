#!/usr/bin/env python3

from database.models import ListingRecord, db, upsert
import os
import logging
import atexit
import json
from apscheduler.schedulers.background import BackgroundScheduler
from redfin import Redfin
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask import Flask, render_template
from config import Config
from sqlalchemy import text
import pika
from threading import Thread

logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)



def open_pika_connection():

    # Establish a connection to a RabbitMQ server (localhost)
    # url = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost/%2f')
    # params = pika.URLParameters(url)
    # params.socket_timeout = 5
    # connection = pika.BlockingConnection(params)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1', heartbeat=10))
    channel = connection.channel()
    channel.basic_qos(prefetch_count=1)

    # Create queue for analyzing zipcode
    channel.queue_declare(queue="analyze")

    return channel

def publish_message_to_queue(channel):
    # Publish message to queue to analyze data
    # Message will contain more data once more filters are added to search.
    # Right now it analyzes only on zip code and rent_price_ratio
    logger.info("Publishing message to 'analyze' queue");
    channel.basic_publish(exchange="", routing_key="analyze",
                body=json.dumps({
                    "zip_code": "TEST",
                    "rent_price_ratio": 0.6
                }))

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
    
def get_all_user_listings_from_api(channel):
    with app.app_context():

        logger.info("Running get_all_user_listings_from_api() function to get listings from Redfin");
        user_search_criteria = load_user_listing_criteria()
        all_listings = []

        for zipcode, search_params in user_search_criteria["zip_code"].items():
            zipcode_listings = client.search_all_by_zipcode(zipcode, search_params["REDFIN_SEARCH_PARAMETERS"])

            all_listings.extend(zipcode_listings)

        save_listings_to_collector_database(all_listings)

        publish_message_to_queue(channel)

        return all_listings

def save_listings_to_collector_database(all_listings):
    for listing in all_listings:
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
        upsert(db.session, ListingRecord, listing_record)
        db.session.commit()

db_path = os.path.join(os.path.dirname(__file__), 'database', 'database.db')

app = create_app()
migrate = Migrate(app, db, directory=db_path)

client = Redfin()


def scheduler():
    channel = open_pika_connection()
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=get_all_user_listings_from_api(channel), trigger="interval", seconds=10)
    scheduler.start()

with app.app_context():

    logger.info("Running with app.app_context():")
    Thread(target=scheduler).start()
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
    try:
        db.session.query("1").from_statement(text("SELECT 1")).all() 
        return render_template("health.html", resp="Data Collector app is Healthy")
    except:
        return "Data Collector app is Unhealthy", 503

if __name__ == '__main__':
    load_dotenv()

    logger.info("Running if __name__ == '__main__'");

    DATABASE_URL = os.getenv('DATABASE_URL')
    DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')

    app.run(debug=True, host='0.0.0.0')

    atexit.register(scheduler.shutdown)