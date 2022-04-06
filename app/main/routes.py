from flask import Blueprint, render_template
from .forms import RegistrationForm

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register',methods=['POST', 'GET'])
def requster_user():
    form = RegistrationForm()
    if form.validate_on_submit():
        print('form validated')
    return render_template('register.html', form=form)