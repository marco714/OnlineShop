from flask import url_for, render_template, flash, redirect, request, jsonify,session
from flaskshop import app, db, bcrypt, mail
from flaskshop.forms import CustomerRegistrationForm, LoginForm, SellerRegistrationForm, ProductRegistrationForm, CheckOutForm
from flaskshop.models import Customer, Seller, CustomerBought, Product, Feature, Review, Size, Brand, Gender
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import secrets
import os

@app.template_filter()
def features(value):
    
    features = [feature.replace('\r', ' ') for feature in value.split('\n')]
    return features

@app.template_filter()
def size(size_name, size_number):

    size_shoes = []
    
    size_name_number = str(size_name) + " " + str(size_number)
    size_shoes.append(size_name_number)
    
    return size_shoes

@app.template_filter()
def calculate_purchase(req):
    total_price = 0


    for k, v in req.items():
        price = v['price'].split(" ")[-1]
        print(price)
        total_price += int(price)
    
    return total_price

app.jinja_env.filters['features'] = features
app.jinja_env.filters['size'] = size
app.jinja_env.filters['calculate_purchase'] = calculate_purchase



@app.route("/")
@app.route("/home")
def home():
    # del session['1#']
    # del session['5']
    # del session['7']
    # del session['10']

    print(session)
    page = request.args.get('page', 1, type=int)
    post_items = Product.query.paginate(page=page, per_page=5)
    return render_template('home.html', post_items=post_items, title="Items")

@app.route("/customer_register", methods=['GET', 'POST'])
def customer_register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = CustomerRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        if int(form.gender.data) == 1:
            male = Gender.query.get(1)
            customer = Customer(username=form.username.data, email=form.email.data, password=hashed_password, gender=male.id)

            db.session.add(customer)
            db.session.commit()
        
        elif int(form.gender.data) == 2:
            female = Gender.query.get(2)
            customer = Customer(username=form.username.data, email=form.email.data, password=hashed_password, gender=female.id)

            db.session.add(customer)
            db.session.commit()

        flash(f"Welcome, You've Created Your Account {form.username.data}! You are now able to log in", 'success')
        return redirect(url_for('login'))
    return render_template('customer_register.html', title='Customer Register', form=form)


@app.route("/seller_register", methods=['GET','POST'])
def seller_register():
    form = SellerRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        seller = Seller(username=form.username.data, email=form.email.data, password=hashed_password, address=form.address.data, phone=form.phone.data)

        db.session.add(seller)
        db.session.commit()

        flash(f"Welcome, You've Created Your Account {form.username.data}! You are now able to log in", 'success')
        return redirect(url_for('login_seller'))
  

    return render_template('seller_register.html', title='Seller Register', form=form)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _ , f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/img', picture_fn)

    form_picture.save(picture_path)

    return picture_fn

@app.route("/product_register", methods=['GET', 'POST'])
def product_register():
    form = ProductRegistrationForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
        
        brand = Brand.query.filter(Brand.brand_name == form.brand.data).first()
        gender = Gender.query.filter(Gender.id == int(form.gender.data)).first()

        if gender.id == 1:

            product = Product(name=form.name.data, price=form.price.data, quantity=form.quantity.data, image_product=picture_file)
            db.session.add(product)
            
            feature = Feature(feature=form.feature.data, product_features=product)
            db.session.add(feature)


            sizing = form.size.data
            sizing = sizing.splitlines()

            for i in range(len(sizing)):

                sizing_number, sizing_name = sizing[i].split()
                size = Size(size_number=sizing_number, size_name=sizing_name, product_size=product)
                db.session.add(size)
                db.session.commit()
     
            gender.product.append(product)
            brand.product.append(product)
            current_user.product.append(product)

            db.session.commit()
            flash(f"You've Registered A New Product {current_user.username}", "success")

        elif gender.id == 2:
        
            product = Product(name=form.name.data, price=form.price.data, quantity=form.quantity.data, image_product=picture_file)
            db.session.add(product)
            
            feature = Feature(feature=form.feature.data, product_features=product)
            db.session.add(feature)

            sizing = form.size.data
            sizing = sizing.splitlines()

            for i in range(len(sizing)):
                sizing_number, sizing_name = sizing[i].split()
                size = Size(size_number=sizing_number, size_name=sizing_name, product_size=product)
                db.session.add(size)
                db.session.commit()

            gender.product.append(product)
            brand.product.append(product)
            current_user.product.append(product)

            db.session.commit()
            flash(f"You've Registered A New Product {current_user.username}", "success")

    return render_template('product_register.html', form=form, title="Product Register")

@app.route("/product/<int:product_id>", methods=['GET', 'POST'])
def product(product_id):
    product = Product.query.get_or_404(product_id)

    features = product.feature[0]
    features = features.feature.splitlines()

    size_num = set()
    size_name = set()

    sizes = product.size
    
    for size in sizes:
        size_num.add(size.size_number)
        size_name.add(size.size_name)
    

    return render_template('customer_product.html', title=product.name, product=product, features=features, size_num=size_num, size_name=size_name)


@app.route("/login_seller", methods=['GET','POST'])
def login_seller():
    form = LoginForm()

    if form.validate_on_submit():
        
        seller = Seller.query.filter_by(email=form.email.data).first()
        if seller and bcrypt.check_password_hash(seller.password, form.password.data):   
            login_user(seller, remember=form.remember.data)
            flash('Login Successful Seller', 'success')
            return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful. Please Check Username and Password', 'danger')

    return render_template('login_seller.html', title='Seller Login', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()

    if form.validate_on_submit():

        customer = Customer.query.filter_by(email=form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please Check Email and Password', 'danger')

    return render_template('login.html', title='Customer Login', form=form)

@app.route("/seller_product/<int:seller_id>")
def seller_product(seller_id):
    
    seller = Seller.query.get(current_user.id)
    size_number = 14
    size_name = "UK"

    return render_template('seller_product.html', title="Seller Products", seller=seller, size_number=size_number, size_name=size_name)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/protected", methods=['POST'])
def protected():

    productDetail = dict()
    req = request.get_json()

    productDetail = {
        "brand": req['brand'],
        "name": req['name'],
        "price":req['price'],
        "size_num": req['size_num'],
        "size_name": req['size_name'],
        "image_name": req['img_id']
    }

    keys = list(productDetail.values())
    session.setdefault(keys[5], productDetail)


    productBought = dict()
    singleProduct = dict()

    for k, v in session.items():

        try:
            convert = int(k)
            
            products = Product.query.get(int(v['image_name']))
            singleProduct[convert] = v
            singleProduct[convert]['image_name'] = products.image_product

            productBought.update(singleProduct)
        except ValueError as e:
            continue

    return {"Message":"Received"}

@app.route("/checkout", methods=['GET', 'POST'])
@login_required
def checkout():
    
    if request.method == "POST":
        req = request.get_json()
        del session[str(req['deleteItem'])]


    product_bought = dict()

    for k, v in session.items():
        
        try:
            item = int(k)
            product_bought.setdefault(item, v)

        except ValueError as e:
            continue
    
    return render_template('postCheckout.html', title='Checkout Product', product=product_bought)


def send_reset_email(user,form):

    print(user)
    msg = Message('Your Order Now Has Been Processed', sender='narcamarco@gmail.com', recipients=[user.email])

    msg.body = f'''Your Following Order Information Is:
Region: {form.region}
City: {form.city}
Address: {form.address}
Contact Number: {form.phone_number}
'''
    mail.send(msg)


@app.route("/buy_checkout", methods=["POST", "GET"])
@login_required
def buy_checkout():

    if request.method == "POST":
                
        req = request.get_json()
        session.setdefault("Product", req)
        print(session["Product"])


    form = CheckOutForm()

    if form.validate_on_submit():

        send_reset_email(current_user, form)
        flash('An Email has been sent to confirm your purchase', 'info')
        return redirect(url_for('home'))

    # print(session['Product'])

    return render_template("checkout.html", title="CheckOut Product", form=form, req=session["Product"])