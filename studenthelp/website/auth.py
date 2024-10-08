from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Volunteering, Honors, Credit
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            print('a')
            email = request.form.get('email')
            password = request.form.get('password')
            print(email)
            print(password)
            user = User.query.filter_by(email=email).first()
            print('1')
            if user:
                print('2')
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    print('3')
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again.', category='error')
            else:
                flash('Email does not exist.', category='error')

        return render_template("login.html", user=current_user)
    except:
        flash("An error has occured", category="error")


@auth.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('auth.login'))
    except:
        flash("An error has occured", category="error")

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    print("sign up")
    try:
        if request.method == 'POST':
            email = request.form.get('email')
            first_name = request.form.get('firstName')
            last_name = request.form.get('lastName')
            password1 = request.form.get('password1')
            password2 = request.form.get('password2')
            print(email)
            user = User.query.filter_by(email=email).first()
            print('1b')
            if user:
                flash('Email already exists.', category='error')
            elif len(email) < 4:
                flash('Email must be greater than 3 characters.', category='error')
            elif len(first_name) < 2:
                flash('First name must be greater than 1 character.', category='error')
            elif password1 != password2:
                flash('Passwords don\'t match.', category='error')
            elif len(password1) < 7:
                flash('Password must be at least 7 characters.', category='error')
            else:
                print('new 1')
                print(first_name)
                print(email)
                print(last_name)
                print(generate_password_hash(password1, method='scrypt'))
                new_user = User(email=email, first_name=first_name,last_name=last_name, password=generate_password_hash(
                    password1, method='scrypt'))
                print('new 2')
                db.session.add(new_user)
                db.session.commit()
                print('new 3')
                
                login_user(new_user, remember=True)
                flash('Account created!', category='success')
                print('new 4')
                
                return redirect(url_for('views.home'))

        return render_template("sign-up.html", user=current_user)
    except:
        flash("An error has occured", category="error")
