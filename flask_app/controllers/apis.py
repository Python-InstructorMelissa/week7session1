from flask_app import app
from flask import Flask, render_template, redirect, session, request, flash
from flask_app.models.user import User

@app.route('/dashboard/')
def dashboard():
    if 'user_id' not in session:
        flash('Hey there log in first dude!!!')
        return redirect('/')
    userData = {
        'id': session['user_id']
    }
    theUser = User.getOne(userData)
    return render_template('dashboard.html', user=theUser)