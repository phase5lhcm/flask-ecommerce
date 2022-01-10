from showroom import app
from flask import render_template
from showroom.models import Product

@app.route("/")
def hello_world():
    return render_template('homepage.html')

@app.route("/showroom")
def showroom():
    products = Product.query.all()
    return 'products page'

