from flask import  render_template, request, redirect, session, url_for, flash
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from user_agent import generate_user_agent
from datetime import datetime
import os, logging
from app.form import ContactForm, LoginForm, RegistrationForm
from app.models import Contacts, User

app.config['SECRET_KEY'] = 'super_secret_key'

user = generate_user_agent()
now = datetime.now()

time = now.strftime("%H:%M")

os = os.name

menu = ["Flask", "Is", "Great"]
text = 'Some quick example text to build on the card title and make up the bulk of the card`s content.'

@app.route('/')
def index():
	return render_template("index.html", title = "Flask",text = text, time = time,os=os) 

@app.route('/home')
def home():
	return render_template("index.html", title = "Flask",text = text, time = time,os=os) 

@app.route('/about')   
def about():
	return render_template('about.html',menu = menu,user = user,time = time,os=os)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    main = logging.getLogger('main')
    main.setLevel(logging.DEBUG)
    handler = logging.FileHandler('log')
    format = logging.Formatter('%(asctime)s  %(name)s %(levelname)s: %(message)s')
    handler.setFormatter(format)
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        save_to_db(form)
        flash("Data sent successfully: " + session.get('username') + ' ' + session.get('email'), category = 'success')
        return redirect(url_for("contact"))

    elif request.method == 'POST':
        flash("Validation failed", category = 'warning')
        main.addHandler(handler)
        main.error(form.name.data + " " + form.email.data + " " + form.phone.data + " " + form.subject.data + " " + form.message.data)

    if(session.get('username') == None):
        return render_template('contact.html', form=form, username="Guest")
    else :
        form.name.data = session.get('username')
        form.email.data = session.get('email')
        return render_template('contact.html', form=form, username=session.get('username'))


@app.route('/database')
def database() :
    contacts = Contacts.query.all()
    return render_template('database.html', contacts=contacts)

@app.route('/database/delete/<id>')
def delete_by_id(id):
    data = Contacts.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("database"))

@app.context_processor
def inject_user():
    date = time
    return dict(user_info=request.headers.get('User-Agent'), date=date)

def save_to_db(form) :
    contact = Contacts(
        name = form.name.data,
        email = form.email.data,
        phone = form.phone.data,
        subject = form.subject.data,
        message = form.message.data
    )
    try:
        db.session.add(contact)
        db.session.commit()
    except:
        db.session.flush()
        db.session.rollback()

@app.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User(
			name = form.name.data, 
			email = form.email.data,
			password = form.password.data
			)
		try:
			db.session.add(user)
			db.session.commit()
		except:
			db.session.flush()
			db.session.rollback()
		flash('Thanks for registering')
		return redirect(url_for('index'))	
	return render_template('registration.html', form=form)

@app.route('/users')
@login_required
def users():
    all_users = User.query.all()
    return render_template('users_data.html', all_users=all_users)

@app.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user:
			if user.password == form.password.data:
				login_user(user,remember=form.remember.data)
				flash('You have been logged in!', category='success')
				return redirect(url_for('index'))
			else:
				flash('Password is incorrect', category='warning')
				return redirect(url_for('login'))
		else:
			flash('Email is incorrect', category='warning') 
	return render_template('login.html', form=form)

@app.route('/user/delete/<id>')
def delete_user_by_id(id):
    data = User.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for("users"))

@app.route('/logout')
def logout():
	logout_user()
	flash('You have been logged out')
	return redirect(url_for('index'))

@app.route('/account')
def account():
	return render_template('account.html')