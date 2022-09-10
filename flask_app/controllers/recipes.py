from flask_app import app
from flask_app.models import user, recipe
from flask import Flask, render_template, redirect, session, request, flash

@app.route('/recipes')
def r_recipes():
    if 'user_id' not in session:
        flash(u'Sorry pal, you are not logged in!', 'login')
        return redirect('/login')

    session.pop('name', None)
    session.pop('description', None)
    session.pop('instructions', None)
    session.pop('cooked_date', None)

    print('rendering recipes page...')

    return render_template('recipes.html', recipes=recipe.Recipe.get_all_recipes_with_creator())

@app.route('/recipe/view/<int:id>')
def r_recipe_view(id): 
    if 'user_id' not in session:
        flash(u'Sorry pal, you are not logged in!', 'login')
        return redirect('/login')   

    data = {
        'id': id
    }

    return render_template('recipe_view.html', recipe=recipe.Recipe.get_one_recipe_with_creator(data))

@app.route('/recipe/create')
def r_recipe_create():
    if 'user_id' not in session:
        flash(u'Sorry pal, you are not logged in!', 'login')
        return redirect('/login')

    return render_template('recipe_create.html')

@app.route('/recipe/insert', methods=['POST'])
def f_recipe_insert():
    parsed = recipe.Recipe.parse_recipe_data(request.form)

    if not recipe.Recipe.validate_recipe_data(parsed):
        session['recipe_name'] = request.form.get('recipe_name')
        session['recipe_desc'] = request.form.get('recipe_description')
        session['recipe_inst'] = request.form.get('recipe_instructions')

        return redirect('/recipe/create')

    recipe.Recipe.add_recipe(parsed)

    return redirect('/recipes')

@app.route('/recipe/edit/<int:id>')
def r_recipe_update(id):
    if 'user_id' not in session:
        flash(u'Sorry pal, you are not logged in!', 'login')
        return redirect('/login')

    data = {
        'id':id
    }

    recipes = recipe.Recipe.get_one(data)

    if session['user_id'] != recipes.user_id:
        flash(u"Cheeky, aren't we?", 'recipes')
        return redirect('/recipes')

    return render_template('recipe_update.html', recipes=recipes)

@app.route('/recipe/update', methods=['POST'])
def f_recipe_update():
    parse = recipe.Recipe.parse_recipe_update(request.form)
    if not recipe.Recipe.validate_recipe_data(parse):
        session['name'] = request.form.get('recipe_name')
        session['description'] = request.form.get('recipe_description')
        session['instructions'] = request.form.get('recipe_instructions')
        session['cooked_date'] = request.form.get('recipe_cooked_on')
        print(session)
        return redirect(f"/recipe/edit/{parse['id']}")

    session.pop('name', None)
    session.pop('description', None)
    session.pop('instructions', None)
    session.pop('cooked_date', None)

    print(f"data validated: {parse}")

    recipe.Recipe.update(parse)

    return redirect('/recipes')

@app.route('/recipe/delete/<int:id>')
def d_recipe_delete(id):
    if 'user_id' not in session:
        flash(u'Sorry pal, you are not logged in!', 'login')
        return redirect('/login')

    data = {
        'id' : id
    }

    recipes = recipe.Recipe.get_one(data)

    if session['user_id'] != recipes.user_id:
        flash(u"Cheeky, aren't we?", 'recipes')
        return redirect('/recipes')

    recipe.Recipe.delete(data)

    return redirect('/recipes')
