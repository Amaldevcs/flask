from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Sessions
from flask_login import login_user, current_user, logout_user, login_required
import time




@app.route("/")
@app.route("/home")
def home():

    return render_template('home.html')
@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/back")
def back():
    return render_template('back.html', title='Back')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        user1 = Sessions.query.filter_by(user_id=user.id).first()
        if user1:
            timea=user1.times+600
            timeb=time.time()
            print timea
            print timeb
            if timeb >= timea:
                return redirect(url_for('logout'))
            else:
                return redirect(url_for('back'))
        

        




        if user and bcrypt.check_password_hash(user.password, form.password.data):

            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return render_template('logout.html', title='Logout')


@app.route("/session")
def session():
    ses=Sessions(author=current_user)
    db.session.add(ses)
    db.session.commit()
    print ses.times
    

    return render_template('account.html', title='Account')
