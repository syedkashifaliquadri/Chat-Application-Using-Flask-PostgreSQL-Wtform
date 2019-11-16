from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
# from wtform_fields import *
from wtform_fields import *
from models import *
# from passlib.hash import pbkdf2_sha256


app = Flask(__name__)
app.secret_key = 'replace later'

# configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wwawlrnmcezdmb:f230e2ab0aedcd4a2fca69cd00212304fa35905ee3eb5182be74f52a4cb14e13@ec2-107-21-104-31.compute-1.amazonaws.com:5432/dac02gvn88tl4a'
db = SQLAlchemy(app)

# configure flask login

login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/", methods=['GET' , 'POST'])
def index():
    reg_form = RegistrationForm()

    #Update database if validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        #Hash password
        hashed_pswd = pbkdf2_sha256.hash(password)

        # Add user into DB
        user = User(username=username, password=hashed_pswd)
        db.session.add(user)
        db.session.commit()

        flash('Register Successfully. Please Login.', 'success')

        return redirect(url_for('login'))

    return render_template('index.html', form=reg_form)


@app.route("/login", methods=['GET' , 'POST'])
def login():

    login_form = LoginForm()

    #Allow login if validation is success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(username= login_form.username.data).first()
        login_user(user_object)
        return redirect(url_for('chat'))

    return render_template("login.html", form= login_form)

@app.route("/chat", methods=['GET' , 'POST'])
def chat():
    if not current_user.is_authenticated:
        flash('Please Login.', 'danger')
        return redirect(url_for('login'))
    return "Chat with me"

@app.route("/logout", methods=['GET'])
def logout():

    logout_user()
    flash('You have logged out successfully', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)