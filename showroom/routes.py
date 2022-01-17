from urllib import request
from showroom import app
from flask import render_template, redirect, flash,url_for, request
from showroom.models import Product, User
from showroom.forms import RegisterForm, LoginForm, PurchaseForm
from showroom import db
from flask_login import login_user, logout_user, login_required, current_user

#TODO - add logging info to file when used in production
import logging
logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def home_page():
    return render_template('homepage.html')

@app.route('/showroom', methods=['GET','POST'])
@login_required
def showroom():
    purchase_form = PurchaseForm()
    if purchase_form.is_submitted():
        print("form submitted")
    # request method checks removes resumbit 
    # form question when refreshing page
    # if purchase_form.validate_on_submit():
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        app.logger.info(f'purchase form selected', request.form.get('purchased_item'))
        print(f"form: ", request.form.get('purchased_item'))
        p_item_obj = Product.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.confirm_purchase(current_user)
                app.logger.info(f'purchase form selected by: {current_user.username} for {p_item_obj.name} at ${p_item_obj.price} dollars')
                flash(f"Purchase successful for {p_item_obj.name} at {p_item_obj.price} dollars", category="success")
            else:
                flash("Your budget is too low for this item", category="danger")
        return redirect(url_for('showroom'))
    #let's return all Products in db
    # passing owner_id=None ensures that only items that
    # have not been purchased yet are displayed
    # in the PRODUCTS AVAILABLE section
    products = Product.query.filter_by(owner=None)
    # print(f"user {current_user.id}")
    owned_products = Product.query.filter_by(owner=current_user.id)
    print('products', owned_products)
    return render_template('showroom.html', products=products, purchase_form=purchase_form, owned_products=owned_products)

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
        # app.logger.info(f'user', create_user)
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
    
@app.route("/logout")
def logout_page():
    logout_user()
    flash("Logout successful", category="info")
    return redirect(url_for("home_page"))

