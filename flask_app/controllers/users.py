from flask_app import app
from flask_app.models import user, recipe
from flask import Flask, render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/login')
def r_login():

    return render_template('login.html')

@app.route('/user/register', methods=['POST'])
def f_register_user():
    parsed_data = user.User.parse_registration_data(request.form)

    if not user.User.validate_registration(request.form):
        session['first_name'] = request.form.get('first_name')
        session['last_name'] = request.form.get('last_name')
        session['email'] = request.form.get('email')

        return redirect('/login')

    print(parsed_data)

    session.clear()

    user_id = user.User.save(parsed_data)

    session['user_id'] = user_id

    return redirect('/recipes')

@app.route('/user/login', methods=['POST'])
def f_user_login():
    print('Attempting to login...')

    data = {
        'email' : request.form.get('email')
    }

    user_match = user.User.get_user_email(data)

    if not user_match:
        flash(u'Invalid Email/Password', 'login')
        return redirect('/login')
    
    if not bcrypt.check_password_hash(user_match.password, request.form.get('password')):
        flash(u'Invalid Email/Password', 'login')
        return redirect('/login')

    session['user_id'] = user_match.id
    session['first_name'] = user_match.first_name.capitalize()
    session['last_name'] = user_match.last_name.capitalize()

    return redirect('/recipes')

@app.route('/logout')
def b_logout():
    print('clearing the session and logging out...')
    session.clear()
    return redirect('/login')
