from flask import render_template
from . import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/clients')
def clients():
    return render_template('clients.html')

@app.route('/properties')
def properties():
    return render_template('properties.html')

@app.route('/visuals')
def visuals():
    return render_template('visuals.html')

