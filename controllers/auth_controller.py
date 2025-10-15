from flask import render_template , redirect, url_for ,flash
from forms import SigninForm ,LoginForm
from app import db
from werkzeug.security import generate_password_hash , check_password_hash
from models.models import Users

from flask_login import login_user , logout_user ,login_required

# admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = generate_password_hash('admin123')
ADMIN_EMAIL = 'admin@parkingapp.com'

# SignUp 

def signup():
    '''
    SignUp is function does user registration for web
    '''
    form = SigninForm()
    if form.validate_on_submit():
        fullname = form.fullname.data
        email = form.email.data
        phone = form.phone.data
        pincode = str(form.pincode.data)
        address = form.address.data
        password = form.password.data
        user = Users.query.filter_by(email=email).first()
        if user:
            flash("User already exists","danger")
        else:
            new_user = Users(fullname=fullname, email=email, phone=phone, pincode=pincode, address=address, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash("User created successfully","success")
            return redirect(url_for('login'))
    return render_template('signup.html', form=form)

# login func

def login():
    '''
    Login function Takes Email and password. And then login user if valid credentials 
    '''
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        if email == ADMIN_EMAIL and check_password_hash(ADMIN_PASSWORD, password):
            admin_user = Users.query.filter_by(email=ADMIN_EMAIL).first()
            if admin_user:
                login_user(admin_user)
                flash("Admin login successful","success")
                return redirect(url_for('home'))
            else:
                flash("Admin user not found in DB","danger")
        else:
            user = Users.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                flash("Login successful","success")
                return redirect(url_for('home'))
            else:
                flash("Invalid credentials","danger")
        form.email.data = ''
        form.password.data = ''
    return render_template('login.html', form=form)

# logout

@login_required
def logout():
    '''
    logout user only if user is logged in !
    '''
    logout_user()
    flash("User logged out successfully","success")
    return redirect(url_for('login'))