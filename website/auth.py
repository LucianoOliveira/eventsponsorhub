from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import os


auth =  Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = Users.query.filter_by(us_email=email).first()
        if user:
            print("User found")
            if check_password_hash(user.us_pwd, password):
                # flash('Logged in successfully!', category='success')
                print("Logged in successfully!")
                login_user(user, remember=True)
                return redirect(url_for('views.managementEvents'))
            else:
                flash('Incorrect password, try again.', category='error')
                print("Incorrect password, try again.")
        else:
            print("User Not found")

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # TODO - FIX THE SIGN UP PAGE
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Users.query.filter_by(us_email=email).first()
        if user:
            if len(email) < 4:
                flash('Email must be greater than 4 characters.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be greater than 6 characters.', category='error')
            else:
                user.pl_pwd = generate_password_hash(password1, method='sha256')
                db.session.commit()
                login_user(user, remember=True)
                # flash('User created successfully!', category='success')
                return redirect(url_for('views.home'))
        else:    
            # flash('Cannot create new user yet!', category='error')   
            if len(email) < 4:
                flash('Email must be greater than 4 characters.', category='error')
            if len(fullname) < 4:
                flash('Name must be greater than 4 characters.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be greater than 6 characters.', category='error')
            else:
                # create user (as buyer and as active)
                new_user = Users(us_name=fullname, us_email=email, us_is_buyer=1, us_is_active=1, us_pwd=generate_password_hash(password1, method='pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()
                # login user
                login_user(new_user, remember=True)
                flash('User created successfully!', category='success')
                return redirect(url_for('views.home'))
        
    return render_template("sign_up.html", user=current_user)