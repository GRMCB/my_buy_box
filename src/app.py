#!/usr/bin/env python3
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def template():
    return '''
     <form action="/echo_user_input" method="POST">
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')