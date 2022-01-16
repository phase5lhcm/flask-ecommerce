from urllib import request
from showroom import app
from flask_wtf import Form
from flask import render_template, redirect, flash,url_for
from showroom.models import Product, User
from showroom.forms import RegisterForm, LoginForm
from showroom import db
from flask_login import login_user, logout_user, login_required
import sys
import logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home_page():
    return render_template('homepage.html')

@app.route('/showroom')
# @login_required
def showroom():
    #let's return all Products in db
    products = Product.query.all()
   # print('products', products)
    return render_template('showroom.html', products=products)

@app.route("/register", methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        create_user = User(username=form.username.data, 
                           email=form.email.data, 
                           password=form.password1.data)
        db.session.add(create_user)
        db.session.commit()
        # print(f"user: create_user")
        # app.logger.info(f'Hello - app.logger.info')
        login_user(create_user)
        flash(f"Welcome! You are now logged in as {create_user.username}", category="success")
        return redirect(url_for('showroom'))
    #Let's check if there are form errors per the validators
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error creating user: {err_msg}', category='danger')
    return render_template('registerPage.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    # user = User.query.filter_by(username=form.username.data).first()
    # print(f'user: ', user) - prints None
    # if form.is_submitted:
    #     userFound = User.query.filter_by(email=form.email.data).first()
    #     print(f"user",userFound)
    # if form.validate():
    #     print('True')
    # form is not validating so I used not logic instead
    if not form.validate_on_submit():
        # print("form is not submitting")
        user = User.query.filter_by(email=form.email.data).first()
        print(f"user", form.email.data)
        if user and user.verify_password(
            check_pwrd = form.password.data
        ):
            login_user(user)
            app.logger.info(f'user login attempt:', user)
            print("user logged in")
            flash(f"{user.username}, you have successfully logged in.")
            return redirect(url_for('showroom'))
        else:
            flash('Incorrect email and password combination. Please try again, or register for an account', category="danger")
    print(form.errors)
    return render_template('loginPage.html', form=form)
    
# @app.route("/logout", methods=['POST'])
# def logout_page():
#     logout_user()
#     flash("Logout successful", category="info")
#     return redirect(url_for("home_page"))