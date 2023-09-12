from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.inspection import inspect

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../main")))

Base = declarative_base()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ListingRecord(db.Model):
    __tablename__ = 'listing_records'
    id = Column(String(50), primary_key=True)
    sale_type = Column(String(50))
    sold_date = Column(String(50))
    property_type = Column(String(50))
    address = Column(String(100))
    city = Column(String(50))
    state_or_province = Column(String(50))
    zip_or_postal_code = Column(String(50))
    price = Column(String(50))
    beds = Column(String(50))
    baths = Column(String(50))
    location = Column(String(50))
    square_feet = Column(String(50))
    lot_size = Column(String(50))
    year_built = Column(String(50))
    days_on_market = Column(String(50))
    price_per_square_feet = Column(String(50))
    hoa_per_month = Column(String(50))
    status = Column(String(50))
    next_open_house_start_time = Column(String(50))
    next_open_house_end_time = Column(String(50))
    url = Column(String(200))
    source = Column(String(50))
    mls_number = Column(String(50))
    favorite = Column(String(1))
    interested = Column(String(1))
    latitude = Column(String(50))
    longitude = Column(String(50))

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
    def __repr__(self):
        return f'<ListingRecord {self.id}>'
