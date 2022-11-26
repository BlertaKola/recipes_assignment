from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def loginPage():
    return render_template("loginRegister.html")

@app.route('/registerUser', methods = ['POST'])
def register():
    if not User.validate_user(request.form):
        flash("Something is wrong little ninja!", 'signUp')
        return redirect(request.referrer)
    
    if User.getUserByEmail(request.form):
        flash("This email already exists", 'emailRegister')
        return redirect(request.referrer)

    data = {
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    User.createUser(data)
    return redirect(request.referrer)

@app.route('/loginUser', methods = ['POST'])
def loginUser():
    data = {
        'email' : request.form['email'],
        'password': request.form['password']
    }
    if len(request.form['email'])< 1:
        flash("Email is required to log in mate", 'emailLogin')
        return redirect(request.referrer)
    if not User.getUserByEmail(data):
        flash("This email doesn't exits mate", 'emailLogin')
        return redirect(request.referrer)
    user = User.getUserByEmail(data)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash("Incorrect password", 'passwordLogin')
        return redirect(request.referrer)
    
    session['user'] = user['id']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/logout')

    data = {
        'id': session['user']
    }
    print(data)
    logged = User.getUserById(data)
    recipes = Recipe.allRecipes()

    return render_template("dashboard.html", logged = logged, recipes = recipes)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')