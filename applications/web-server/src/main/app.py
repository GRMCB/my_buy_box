#!/usr/bin/env python3
import os
os.environ['PYTHONPATH'] = '/var/www/webapp/applications/web-server/src/main/'

from flask import Flask, redirect, render_template, request
from helpers import valid_zipcode, load_valid_zipcodes

app = Flask(__name__)
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

        return render_template("invalid.html")

@app.route("/zipcode/<zip_code>", methods = ['POST', 'GET'])
def zip_code(zip_code):
    return render_template('data.html', zip_code=zip_code)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
