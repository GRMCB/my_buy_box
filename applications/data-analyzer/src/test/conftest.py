import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../main")))
from main.app import app
import pytest
import json

os.environ['PYTHONPATH'] = '/var/www/webapp/applications/data-analyzer/src/main/'

@pytest.fixture
def app_test_client():
    with app.test_client() as test_client:
        yield test_client