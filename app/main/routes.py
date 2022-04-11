from re import A
from app import db
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, login_required
from .forms import AddArtWork, LoginForm, RegistrationForm, ChangeProfilePictureForm
from .models import User, ArtWork
from .utils import save_picture
import json

main = Blueprint("main", __name__)


@main.route("/")
def home():
    user = current_user
    profile_picture = url_for(
        "static", filename="images/profile_pictures/{}".format(user.profile_picture)
    )
    artwork = list(ArtWork.query.all())
    print(artwork[1].orientation)
    return render_template("home.html", profile_picture=profile_picture, artwork=artwork, user=user)


@main.route("/register", methods=["POST", "GET"])
def register_user():
    form = RegistrationForm()
    if form.validate_on_submit():

        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
        )

        user.password = user.generate_password_hash(form.password.data)

        db.session.add(user)
        db.session.commit()
        flash(f"Account created for {user.username}. You can now log in.")
        return redirect(url_for('main.login'))

    return render_template("register.html", form=form)


@main.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password_hash(form.password.data):
            login_user(user)
            flash("Login Successfull")
            return redirect(url_for("main.home"))
        else:
            flash("Login Failed. Please check email or password.")

    return render_template("login.html", form=form)


@main.route("/dashboard", methods=["POST", "GET"])
def dashboard():
    user = current_user
    profile_picture = url_for(
        "static", filename="images/profile_pictures/{}".format(user.profile_picture)
    )

    profile_picture_form = ChangeProfilePictureForm()
    artwork_form = AddArtWork()

    if profile_picture_form.validate_on_submit():
        print('profile pic form validating')
        if profile_picture_form.new_picture.data:
            pic_data = save_picture(profile_picture_form.new_picture.data, 'profile_picture')
            user.profile_picture = pic_data['filename']
        db.session.commit()
        flash("Profile picture updated succesfully")
        return redirect(url_for("main.dashboard"))

    artwork = list(ArtWork.query.all())


    return render_template(
        "dashboard.html",
        user=user,
        profile_picture=profile_picture,
        profile_picture_form=profile_picture_form,
        artwork=artwork,
        artwork_form=artwork_form
    )


@main.route('/add_art', methods=['POST'])
def add_art():
    artwork_form = AddArtWork()
    if artwork_form.validate_on_submit():
        print('art form validating')
        if artwork_form.art_work.data:
            pic_data = save_picture(artwork_form.art_work.data, 'artwork')
        art_work = ArtWork(
            art_work = pic_data['filename'],
            name = artwork_form.name.data,
            description = artwork_form.description.data,
            orientation = pic_data['orientation']
        )
        db.session.add(art_work)
        db.session.commit()
        print(' filename: ', art_work.art_work, ' name:', art_work.name, ' desc:', art_work.description, ' orientation:', art_work.orientation)
        flash('Your art has been added succesfully')
        return redirect(url_for('main.dashboard'))
    else:
        return json.dumps({'message': 'Something went wrong. Please try again'}), 400

@main.route('/display/<art_id>', methods=['GET'])
def set_display(art_id):
    artwork = ArtWork.query.get(art_id)
    current_status = artwork.on_display
    artwork.on_display = not current_status

    db.session.commit()

    return json.dumps({'message': 'Display settings changed to {} for art {}'.format(artwork.on_display, artwork.id)})