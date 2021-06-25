import json
from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite"
db = SQLAlchemy(app)


class database(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.email = email
        self.password = password
        self.username = username


@app.route('/')
def home():
    url = 'https://api.quotable.io/random'
    requesting = requests.get(url)
    res = json.loads(requesting.text)
    content = res["content"]
    author = res["author"]
    return render_template('index.html', contents=content, author=author)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form['email'] == database.query.filter_by(email=request.form['email']) and request.form[
            'password'] == database.query.filter_by(password=request.form['password']):
            username = request.form['username']
            session['username'] = username
            return redirect(url_for('user'))
    return render_template('login.html')


@app.route('/user')
def user():
    url = 'https://api.quotable.io/random'
    requesting = requests.get(url)
    res = json.loads(requesting.text)
    content = res["content"]
    author = res["author"]
    return render_template('user.html', contents=content, author=author)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        account = database(request.form['username'], request.form['email'], request.form['password'])
        if request.form['send_request'] == "send_post_request":
            db.session.add(account)
            db.session.commit()
            username = request.form['username']
            session['username'] = username
            return redirect(url_for('user'))
    return render_template('signup.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    flash("You are Logged Out", "Info")
    session.pop('username', None)
    return render_template('login.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_name = session['username']
    return render_template('profile.html', user_name=user_name)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
