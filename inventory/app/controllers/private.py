from app import app
from flask import Flask, render_template, redirect, session, request, flash
import re
from  flask_bcrypt import Bcrypt
from app.models.user import User
from app.models.inventory import Inventory


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('dashboard.html', user=User.getOne(data), items=Inventory.getAll())

@app.route('/addInventory')
def addInventory():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    return render_template('addInventory.html', user=User.getOne(data))

@app.route('/createInventory', methods=['POST'])
def createInventory():
    data = {
        'iName': request.form['iName'],
        'iImage': request.form['iImage'],
        'user_id': request.form['user_id']
    }
    Inventory.save(data)
    return redirect('/dashboard')

@app.route('/updateUser/<int:id>')
def updateUser(id):
    data = {
        'id': id
    }
    return render_template('updateUser.html', user=User.getOne(data))

@app.route('/editUser/<int:id>', methods=['POST'])
def editUser(id):
    data = {
        'id': id,
        'firstName': request.form['firstName'],
        'lastName': request.form['lastName'],
        'uImg': request.form['uImg']
    }
    User.update(data)
    return redirect('/dashboard')

@app.route('/item/<int:id>')
def viewItem(id):
    data = {
        'id': id
    }
    print(Inventory.getOne(data))
    return render_template('viewItem.html', item=Inventory.getOneWithUser(data))