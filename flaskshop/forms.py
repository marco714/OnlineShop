from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, RadioField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields import html5 as h5fields
from flaskshop.models import Customer, Seller

class CustomerRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = RadioField('Gender', choices=[(1, "Male"), (2, "Female")],default=1, coerce=int)
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        customer = Customer.query.filter_by(username=username.data).first()

        if customer:
            raise ValidationError('That Username is Taken. Please Choose A Different One')
    
    def validate_email(self, email):
        customer = Customer.query.filter_by(email=email.data).first()

        if customer:
            raise ValidationError('That Email is Taken. Please Choose A Different One')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign Up')

class SellerRegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    address = StringField('Address', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=11)])
    submit = SubmitField('Sign Up')

class ProductRegistrationForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    price = h5fields.IntegerField('Product Price', validators=[DataRequired()])
    quantity = h5fields.IntegerField('Product Quantity', validators=[DataRequired()])
    feature = TextAreaField('Product Features', validators=[DataRequired()])
    size = TextAreaField('Product Size', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[(1, "Male"), (2, "Female")],default=1, coerce=int)
    brand = StringField('Product Brand', validators=[DataRequired()])
    picture = FileField('Product Image', validators=[FileAllowed(['jpg','jfif', 'png'])])

    submit = SubmitField('Register Product')

class CheckOutForm(FlaskForm):

    region = StringField('Region', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    address = StringField('Complete Address', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Purchase Product')
