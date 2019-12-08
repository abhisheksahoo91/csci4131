from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt
from app.dbclass import User
from app.form import RegistrationForm, LoginForm, UpdateProfileForm
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data,
            username=form.username.data, email=form.email.data,
            password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created successfully. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                flash(f'Welcome {user.firstname}!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('user_home'))
            else:
                flash('Email and password do not match. Please try again!', 'danger')
        else:
            flash(f'No record exists for email {form.email.data}.  Please verify the email!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/user_home')
@login_required
def user_home():
    return render_template('user_home.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        any_field_update = False
        if form.email.data != current_user.email:
            current_user.email = form.email.data
            any_field_update = True
        if form.username.data != current_user.username:
            current_user.username = form.username.data
            any_field_update = True
        if form.firstname.data != current_user.firstname:
            current_user.firstname = form.firstname.data
            any_field_update = True
        if form.lastname.data != current_user.lastname:
            current_user.lastname = form.lastname.data
            any_field_update = True
        if form.new_password.data != '':
            hashed_pw = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password = hashed_pw
            any_field_update = True
        if any_field_update:
            db.session.commit()
            flash('Profile updated successfully.', 'success')
        else:
            flash('No fields updated.', 'success')
        
        return redirect(url_for('user_home'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname

    return render_template('profile.html', title='Profile', form=form)