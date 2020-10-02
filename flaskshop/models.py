from datetime import datetime
from flaskshop import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):

    if Customer.query.get(int(user_id)):
        return Customer.query.get(int(user_id))
    else:
        return Seller.query.get(int(user_id))

class Customer(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_customer = db.Column(db.Boolean, server_default="1")

    customer_bought = db.relationship('CustomerBought', backref='customer_bought', lazy=True)

    #Changed
    gender = db.Column(db.Integer, db.ForeignKey('gender.id'))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Seller(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(12), nullable=False)
    is_customer = db.Column(db.Boolean, server_default="0")

    product = db.relationship('Product', backref='seller_item', lazy=True)

    def __repr__(self):
        return f"Seller('{self.username}', '{self.email}', '{self.address}', '{self.phone}')"

class CustomerBought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(60), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    date_bought = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    image_product = db.Column(db.String(60), nullable=False)

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    
    def __repr__(self):
        return f"CustomerBought('{self.name}', '{self.date_bought}', '{self.price}', '{self.quantity}')"

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_product = db.Column(db.String(60), nullable=False)

    feature = db.relationship('Feature', backref='product_features', lazy=True)
    size = db.relationship('Size', backref='product_size', lazy=True)
    review = db.relationship('Review', backref='product_review', lazy=True)

    #Changed
    gender = db.Column(db.Integer, db.ForeignKey('gender.id'))

    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'))
    seller_id = db.Column(db.Integer, db.ForeignKey('seller.id'))

    def __repr__(self):
        return f"Product('{self.name}', '{self.price}', '{self.quantity}')"

class Feature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feature = db.Column(db.Text, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return f"Feature('{self.feature}')"

class Review(db.Model):

    review_star = db.Column(db.Integer, primary_key=True)
    review_meaning = db.Column(db.String, nullable=False)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    def __repr__(self):
        return f"Review('{self.review_star}', '{self.review_meaning}')"

class Size(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    size_number = db.Column(db.Integer, nullable=False)
    size_name = db.Column(db.String(20), nullable=False)
    
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return f"Size('{self.size_number}', '{self.size_name}')"

#Look Up Table
class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String(25), nullable=False, unique=True)

    product = db.relationship('Product', backref='brand_product', lazy=True)

    def __repr__(self):
        return f"Brand('{self.brand_name}')"

#Look Up Table
class Gender(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(7), nullable=False)
    
    # Changed
    customer = db.relationship('Customer', backref='gender_customer', lazy=True)
    product = db.relationship('Product', backref='gender_product', lazy=True)

    def __repr__(self):
        return f"Gender('{self.gender}')"