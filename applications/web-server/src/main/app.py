#!/usr/bin/env python3

from flask import Flask, redirect, render_template, request
from prometheus_flask_exporter import PrometheusMetrics
from utils import valid_zipcode, load_valid_zipcodes
import requests
import json
import time


app = Flask(__name__)
app.config.from_pyfile("config.py")
metrics = PrometheusMetrics(app)

# static information as metric
metrics.info('app_info', 'Application info', version='1.0.3')

metrics.register_default(
    metrics.counter(
        'by_path_counter', 'Request count by request paths',
        labels={'path': lambda: request.path}
    )
)

valid_zipcodes_list = load_valid_zipcodes()

@app.route("/", methods = ['GET'])
def home_page():
    return render_template("index.html")

@app.route("/verify", methods = ['POST', 'GET'])
def verify():
    if request.method == "POST":
        zip_code = request.form["zip"]

        if valid_zipcode(valid_zipcodes_list, 0, len(valid_zipcodes_list) -1, zip_code):
            print("VALID ZIPCODE:{}".format(zip_code))
            zip_code_route = "/zipcode/" + str(zip_code)
            time.sleep(5)
            return redirect(zip_code_route)

        return render_template("invalid.html", zip_code=zip_code)

@app.route("/zipcode/<zip_code>", methods = ['POST', 'GET'])
def zip_code(zip_code):
    # Call Data Analyzer Rest API to get Zip code listings directly from database
    records = requests.get(f"http://127.0.0.1:8082/api/listings/{zip_code}")
    json_records = json.loads(records.text)

    return render_template('data.html', records=json_records)

@app.route('/health', methods = ['GET'])
def health():

    resp = "Web Server app is Healthy"

    return render_template('health.html', resp=resp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
