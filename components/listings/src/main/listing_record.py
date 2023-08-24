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

