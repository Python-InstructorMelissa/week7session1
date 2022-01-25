from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.user import User

from  flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register/', methods=['POST'])
def register():
    isValid = User.validate(request.form)
    if not isValid:
        flash('Something went wrong')
        return redirect('/')
    data = {
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'username': request.form['username'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    if not id:
        flash("Something went wrong!")
        return redirect('/')
    if request.form['adminKey'] == 'CohortDecJan2021':
        data1 = {
            'id': id,
            'level': 1
        }
        User.update(data1)
        session['user_id'] = id
        flash(f'You are now logged in')
        return redirect('/dashboard/')
    else:
        data1 =  {
            'id': id,
            'level': 0
        }
        User.update(data1)
        session['user_id'] = id
        flash(f'You are now logged in')
        return redirect('/dashboard/')

@app.route('/login/', methods=['POST'])
def login():
    data = {
        'username': request.form['username']
    }
    user = User.getUsername(data)
    if not user:
        flash("Invalid Login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Wrong password")
        return redirect('/')
    session['user_id'] = user.id
    flash(f'You are now logged in {user.username}')
    return redirect('/dashboard/')


@app.route('/logout/')
def logout():
    session.clear()
    flash("You have been logged out")
    return redirect('/')

@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in')
        return redirect('/')
    else:
        data = {
            'id': session['user_id']
        }
        user = User.getOne(data)
        print('user.level: ', user.level)
        return render_template('dashboard.html', user=user)