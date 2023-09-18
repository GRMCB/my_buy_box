#!/usr/bin/env python3
from flask import Flask, redirect, render_template, request
import requests
import json

app = Flask(__name__)
app.config.from_pyfile("config.py")
from helpers import valid_zipcode, load_valid_zipcodes

valid_zipcodes_list = load_valid_zipcodes()

@app.route("/", methods = ['GET'])
def home_page():
    return render_template("index.html")

@app.route("/verify", methods = ['POST', 'GET'])
def verify():
    if request.method == "POST":
        zip_code = request.form["zip"]

        if valid_zipcode(valid_zipcodes_list, 0, len(valid_zipcodes_list) -1, zip_code):
            print("VALID ZIPCODE")
            zip_code_route = "/zipcode/" + str(zip_code)
            return redirect(zip_code_route)

        return render_template("invalid.html", zip_code=zip_code)

@app.route("/zipcode/<zip_code>", methods = ['POST', 'GET'])
def zip_code(zip_code):
    # Call Data Collector Rest API to get Zip code listings directly from database
    # This will change to Retrieving it from Data Analyzer database. 
    records = requests.get(f"http://127.0.0.1:8082/api/listings/{zip_code}")
    json_records = json.loads(records.text)

    return render_template('data.html', records=json_records)

@app.route('/health', methods = ['GET'])
def health():
    response = requests.get(f"http://127.0.0.1:8080/zipcode/12345")
    if response.status_code == 200:
        resp = "System is Healthy"

    else:
        resp = "System is Unhealthy"

    return render_template('health.html', resp=resp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
