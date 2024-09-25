from flask import render_template
from . import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
