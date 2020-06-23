from flask import Flask, render_template
from flask_mongoengine import MongoEngine
from flask_user import login_required, UserManager, UserMixin


class ConfigClass(object):
    SECRET_KEY = 'this is a totally secret key'
    MONGODB_SETTINGS = {
        'db': 'tst_app',
        'host': 'mongodb://localhost:27017/tst_app'
    }

    USER_APP_NAME = 'Flask-User MongoDB App'
    USER_ENABLE_EMAIL = False
    USER_ENABLE_USERNAME = True
    USER_REQUIRE_RETYPE_PASSWORD = False


app = Flask(__name__)
app.config.from_object(ConfigClass)

# app = Flask(__name__)
# app.config.from_object(__name__ + '.ConfigClass')

db = MongoEngine(app)


class User(db.Document, UserMixin):
    active = db.BooleanField(default=True)

    username = db.StringField(default='')
    password = db.StringField()

    first_name = db.StringField(default='')
    last_name = db.StringField(default='')

    roles = db.ListField(db.StringField, default=[])


user_manager = UserManager(app, db, User)

def headerinfo():
    return {'Home': "/", 'Lights': "/lights", 'Special Functions': "/special", 'Rooms': "/rooms", 'Login': '/login'}


@app.route('/login')
def login():
    return render_template("login.html", header=headerinfo(), active="Login")


@app.route('/members')
@login_required
def members_page():
    return render_template('member.html')



