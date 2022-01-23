from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import Length, Email, EqualTo, DataRequired, ValidationError
from showroom.models import User

class RegisterForm(FlaskForm):
    
    def validate_username(self, check_username):
        #query documents to see if user already exists in db with this username
        user = User.query.filter_by(username=check_username.data).first()
        if user:
            raise ValidationError('Username already exists.')
    def validate_email(self, check_email):
        email = User.query.filter_by(email=check_email.data).first()
        if email: 
            raise ValidationError('Email addrress already exists, please log in with your account.')
        
    username = StringField(label='Username', validators=[Length(min=2, max=20), DataRequired()])
    email = StringField(label='Email', validators=[Email(message="A legit email is required"), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password_confirmation = PasswordField(label='Confirm password', validators=[EqualTo('password1'), DataRequired()])
    submitBtn = SubmitField(label='Create Account')
    
class LoginForm(FlaskForm):
     #query documents to see if user already exists in db with username or email from user input
     # Login form can validate with username or email
    username = StringField(label='Username', validators=[DataRequired()])
    email = StringField(label='Email', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[ DataRequired()])
    loginBtn = SubmitField(label='Sign in')

class PurchaseForm(FlaskForm):
    purchaseBtn = SubmitField(label='Purchase')

class SellForm(FlaskForm):
    sellBtn = SubmitField(label='Sell')