from flask import Flask, render_template, request
# from wtform_fields import *
from wtform_fields import *
from models import *


app = Flask(__name__)
app.secret_key = 'replace later'

# configure Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wwawlrnmcezdmb:f230e2ab0aedcd4a2fca69cd00212304fa35905ee3eb5182be74f52a4cb14e13@ec2-107-21-104-31.compute-1.amazonaws.com:5432/dac02gvn88tl4a'
db = SQLAlchemy(app)

@app.route("/", methods=['GET' , 'POST'])
def index():
    reg_form = RegistrationForm()
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        # Check username exists
        user_object = User.query.filter_by(username=username).first()
        if user_object:
            return "Someone else taken this username"
        
        # Add user into DB
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return "Inserted into DB"


    return render_template('index.html', form=reg_form)



if __name__ == "__main__":
    app.run(debug=True)