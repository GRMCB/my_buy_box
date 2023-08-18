from main.helpers import valid_zipcode
import pytest
import os

os.environ['PYTHONPATH'] = '/var/www/webapp/applications/web-server/src/main/'

def test_invalid_zipcode(load_valid_zipcodes):
    zip_code = "00000"

    assert (valid_zipcode(load_valid_zipcodes, 0, len(load_valid_zipcodes)-1, zip_code)) == False

def test_valid_zipcode(load_valid_zipcodes):
    zip_code = "98034"

    assert (valid_zipcode(load_valid_zipcodes, 0, len(load_valid_zipcodes)-1, zip_code)) == True
