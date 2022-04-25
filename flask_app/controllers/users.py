from flask_app import app 
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, sighting
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if not user.User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data ={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    user_id = user.User.save(data)
    session['user_id'] = user_id
    return redirect(f"/dashboard/{session['user_id']}")

@app.route('/login', methods=['POST'])
def login():
    data = {'email': request.form['email']}
    user_in_db = user.User.get_by_email(data)
    if not user_in_db:
        flash("*Invalid Email/Password", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("*Invalid Email/Password", 'login')
        return redirect('/')
    print(user_in_db)
    session['user_id'] = user_in_db.id
    return redirect(f'/dashboard/{user_in_db.id}')

@app.route('/dashboard/<int:id>')
def dashboard(id):
    if 'user_id' not in session:
        flash("*Please Log In", 'login')
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    one_user = user.User.one_user_info(data)
    all_sightings = sighting.Sighting.get_all()
    return render_template('dashboard.html', one_user = one_user, all_sightings = all_sightings)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')