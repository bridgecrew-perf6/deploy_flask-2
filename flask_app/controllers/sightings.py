from flask_app import app 
from flask import render_template, redirect, request, session, flash
from flask_app.models import sighting, user

@app.route('/show/<int:id>')
def show(id):
    data = {
        'id' : id
    }
    user_data = {
        'id' : session['user_id']
    }
    print(data)
    one_user = user.User.one_user_info(user_data)
    sighting_info = sighting.Sighting.get_one(data)
    number_skeptic = sighting.Sighting.number_skeptical(data)
    return render_template('sighting.html', sighting_info = sighting_info, one_user =one_user, number_skeptic = number_skeptic)

@app.route('/report_sighting')
def report():
    if not 'user_id' in session:
        return redirect('/')
    data = {
        'id' : session['user_id']
    }
    one_user = user.User.one_user_info(data)
    return render_template('add_sighting.html', one_user = one_user)


@app.route('/create', methods=['POST'])
def create_sighting():
    if not sighting.Sighting.validate_sighting(request.form):
        return redirect('/add_painting')
    data = {
        'location' : request.form['location'],
        'description' : request.form['description'],
        'date' : request.form['date'],
        'number' : request.form['number'],
        'reporter_id' : session['user_id'],
        'reporter_name' : request.form['reporter_name']
    }
    sighting.Sighting.save(data)
    return redirect(f"/dashboard/{session['user_id']}")


@app.route('/edit/<int:id>')
def edit(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id' : id
    }
    user_data = {
        'id' : session['user_id']
    }
    one_user = user.User.one_user_info(user_data)
    sighting_info = sighting.Sighting.get_one(data)
    return render_template('edit_sighting.html', sighting_info = sighting_info, one_user = one_user)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    if 'user_id' not in session:
        return redirect('/')
    if not sighting.Sighting.validate_sighting(request.form):
        return redirect(f"/edit/{id}")
    data = {
        'id' : id,
        'location' : request.form['location'],
        'description' : request.form['description'],
        'date' : request.form['date'],
        'number' : request.form['number'],
    }
    sighting.Sighting.update(data)
    return redirect(f"/dashboard/{session['user_id']}")

@app.route('/skeptical/<int:id>')
def skeptical(id):
    data = {
        'user_id' : session['user_id'],
        'sighting_id' : id
    }
    sighting.Sighting.skeptical(data)
    return redirect(f"/show/{id}")

@app.route('/believe/<int:id>')
def believe(id):
    data = {
        'user_id' : session['user_id'],
        'sighting_id' : id
    }
    sighting.Sighting.believe(data)
    return redirect(f"/show/{id}")
