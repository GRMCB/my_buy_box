from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ListingRecord(Base):
    __tablename__ = 'listing_records'
    id = Column(Integer, primary_key=True)
    sale_type = Column(String(50))
    sold_date = Column(String(50))
    property_type = Column(String(50))
    address = Column(String(100))
    city = Column(String(50))
    state_or_province = Column(String(50))
    zip_or_postal_code = Column(String(50))
    price = Column(Float)
    beds = Column(Integer)
    baths = Column(Float)
    location = Column(String(50))
    square_feet = Column(Integer)
    lot_size = Column(Integer)
    year_built = Column(Integer)
    days_on_market = Column(Integer)
    price_per_square_feet = Column(Float)
    hoa_per_month = Column(Float)
    status = Column(String(50))
    next_open_house_start_time = Column(String(50))
    next_open_house_end_time = Column(String(50))
    url = Column(String(200))
    source = Column(String(50))
    mls_number = Column(Integer)
    favorite = Column(String(1))
    interested = Column(String(1))
    latitude = Column(Float)
    longitude = Column(Float)

    def __repr__(self):
        return f'<ListingRecord {self.id}>'