#!/usr/bin/env python3.5
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!" #return string

@app.route("/welcome")
def welcome():
    return render_template('welcome.html') #render a template

if __name__ == "__main__":
    app.run(port=2300) #run server/app
