from flask_app import app
from flask import render_template, request, redirect, session, flash

from flask_app.models.recipe import Recipe
from flask_app.models.user import User




@app.route('/recipe/new')
def recipe():
    if 'user' not in session:
        return redirect('/')
    data = {
        'id': session['user']
    }
    logged = User.getUserById(data)
    return render_template("createRecipe.html", logged = logged)

@app.route('/recipe/create', methods = ['POST'])
def form_recipe():
    if 'user' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        flash("Something is wrong ninja", 'recipeCreate')
        return redirect(request.referrer)
    
    data = {
        'name' : request.form['name'],
        'description' : request.form['description'],
        'instruction' : request.form['instruction'],
        'dateMade' : request.form['dateMade'],
        'under30' : request.form['under30'],
        'user_id': request.form['user_id']
    }
    Recipe.createRecipe(data)
    return redirect('/dashboard')



@app.route('/recipe/view/<int:id>')
def viewRecipe(id):
    if 'user' not in session:
        return redirect('/')
    data = {
        'id': id,
        'user_id' : session['user']
    }
    dataInfo = {
        'id': session['user']
    }
    
    return render_template("viewRecipe.html", recipe = Recipe.getRecipeById(data), loggedUser = User.getUserById(dataInfo))



@app.route('/recipe/edit/<int:id>')
def editRecipe(id):
    if 'user' not in session:
        return redirect('/logout')
    data = {
        'id': id,
        'user_id': session['user']
    }

    currentRecipe = Recipe.getRecipeById(data)
    if not session['user'] == currentRecipe['user_id']:
        return redirect('/404Error')

    dataInfo = {
        'id': session['user']
    }
    return render_template("editRecipe.html", recipe = Recipe.getRecipeById(data), loggedUser = User.getUserById(dataInfo))

@app.route('/recipe/update/<int:id>', methods = ['POST'])
def updating(id):
    if 'user' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        flash("All fields must be complete", 'updateRecipe')
        return redirect(request.referrer)

    data = {
        'id': id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instruction': request.form['instruction'],
        'under30': request.form['under30'],
        'dateMade': request.form['dateMade'],
        'user_id': session['user']
    }

    Recipe.updateRecipe(data)
    return redirect('/dashboard')


@app.route('/recipe/delete/<int:id>')
def delete(id):
    data = {
        'id': id,
        'user_id' : session['user']
    }
    recipe = Recipe.getRecipeById(data)
    
    if not session['user'] == recipe['user_id']:
        return redirect('/404Error')

    Recipe.deleteRecipe(data)
    return redirect(request.referrer)



@app.route('/404Error')
def error():
    return render_template("404Error.html")








