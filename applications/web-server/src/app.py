#!/usr/bin/env python3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')