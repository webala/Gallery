from app import db
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required
from .forms import LoginForm, RegistrationForm, ChangeProfilePictureForm
from .models import User
from .utils import save_picture

main = Blueprint('main', __name__)

@main.route('/')
def home():
    users = User.query.all()
    return render_template('home.html', users=users)

@main.route('/register',methods=['POST', 'GET'])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        
        user = User(
            username = form.username.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data,
            email = form.email.data
        )

        user.password = user.generate_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {user.username}. You can now log in.')

    return render_template('register.html', form=form)


@main.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password_hash(form.password.data):
            login_user(user)
            flash('Login Successfull')
            return redirect(url_for('main.home'))
        else:
            flash('Login Failed. Please check email or password.')
    

    return render_template('login.html', form=form)

@main.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    user = current_user
    profile_picture = url_for('static', filename='images/profile_pictures/{}'.format(user.profile_picture))

    form = ChangeProfilePictureForm()

    if form.validate_on_submit():
        if form.new_picture.data:
            new_picture = save_picture(form.new_picture.data)
            user.profile_picture = new_picture
        db.session.commit()
        flash('Profile picture updated succesfully')
        return redirect(url_for('main.dashboard'))

    return render_template('dashboard.html', user=user, profile_picture=profile_picture, form=form)