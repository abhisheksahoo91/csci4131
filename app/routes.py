from flask import render_template, url_for, flash, redirect, request
from app import app, db, bcrypt, logging
from app.dbclass import User
from app.form import RegistrationForm, LoginForm, UpdateProfileForm
from app.musiccloud import MusicCloud
from flask_login import login_user, current_user, logout_user, login_required
import requests, ast

DEEZER_BASE_URL = 'http://api.deezer.com/search?'

@app.route("/")
@app.route("/home")
def home():
    logging.info('app started')
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
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Email and password do not match. Please try again!', 'danger')
        else:
            flash(f'No record exists for email {form.email.data}.  Please verify the email!', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    flash('Goodbye {}! See you again soon'.format(current_user.firstname), 'success')
    logout_user()
    return redirect(url_for('home'))

@app.route('/searched', methods=['GET', 'POST'])
@login_required
def searched():
    search_type = request.args.get('search_type')
    search_text = request.args.get('search_text')
    musicCloud = MusicCloud()
    data = musicCloud.search_entity(search_type, search_text)
    # Format album data to group them based on genre
    if search_type == 'album':
        data = musicCloud.group_album_by_genre(data)
    if data == None or data == []:
        flash("No results for '{} - {}'. Please refine your search text.".format(search_type, search_text), 'danger')
    return render_template('searched.html', data=data, search_type=search_type, search_text=search_text)

@app.route('/selected/<search_type>/<id>', methods=['GET', 'POST'])
@login_required
def selected(search_type, id):
    musicCloud = MusicCloud()
    data = musicCloud.get_entity_byId(search_type, id)
    return render_template('selected.html', data=data)

@app.route('/update_favorite', methods=['GET', 'POST'])
@login_required
def update_favorite():
    target = request.args.get('target')
    target_param1 = request.args.get('target_param1')
    target_param2 = request.args.get('target_param2')
    search_type = request.args.get('search_type')
    entity_id = request.args.get('entity_id')

    musicCloud = MusicCloud()
    musicCloud.toggle_favorite(search_type, entity_id)
    if target == 'searched':
        return redirect(url_for('searched', search_type=target_param1, search_text=target_param2))
    elif target == 'selected':
        return redirect(url_for('selected', search_type=target_param1, id=target_param2))
    else:
        return redirect('home')

@app.route('/favorite', methods=['GET', 'POST'])
@login_required
def favorite():
    search_type = request.args.get('search_type')
    musicCloud = MusicCloud()
    data = musicCloud.get_favorite_by_type(search_type)
    if data == None or data == []:
        flash('You have not added any {}(s) to your favorite yet!'.format(search_type), 'danger')
    return render_template('favorite.html', data=data)


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
        
        return redirect(url_for('home'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname

    return render_template('profile.html', title='Profile', form=form)