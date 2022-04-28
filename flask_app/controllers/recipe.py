from flask_app import app

from flask import render_template, redirect, session, request, flash

from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.route('/dashboard')
def home():
    if 'user.id' not in session: #this was in his success page not mine
        flash ("Please log in to see this page")
        return redirect('/')

    recipes = Recipe.recipes_show_all()
    print (recipes)
    return render_template('/dashboard.html', recipes = recipes)



@app.route('/recipes/new')
def recipes_new():
    if 'user.id' not in session:
        flash ("Please log in to see this page")
        return redirect('/')

    return render_template ('/recipes_new.html')



@app.route('/recipes/new/results', methods = ['POST'])
def recipes_new_results():
    if 'user.id' not in session:
        flash ("Please log in to see this page")
        return redirect('/')
    #need validations here before we insert into db
    # print (request.form)
    # print (Recipe.validate_recipe(request.form)
    if Recipe.validate_recipe(request.form):
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_made': request.form['date_made'],
            'under_30_minutes': request.form['under_30_minutes'],
            'user_id': session['user.id']
        }
        Recipe.recipe_new(data)
        return redirect('/dashboard')

    return redirect('/recipes/new')



@app.route('/recipes/<int:recipes_id>')
def recipes_show(recipes_id):
    if 'user.id' not in session:
        flash ("Please log in to see this page")
        return redirect('/')

    recipes = Recipe.recipes_show({'id': recipes_id})

    return render_template('recipes_show.html', recipes = recipes)



@app.route('/recipes/edit/<int:recipe_id>')
def recipes_edit(recipe_id):
    if 'user.id' not in session:
        flash ("Please log in to see this page")
        return redirect('/')

    recipes = Recipe.recipes_show({'id': recipe_id})

    if recipes.user.id != session['user.id']:
        return redirect('/dashboard')
        #this may be a black belt feature

    print(recipes)
    return render_template('recipes_edit.html', recipes = recipes)



@app.route('/recipes/update/<int:recipes_id>', methods = ['POST'])
def recipes_update(recipes_id):

    recipes = Recipe.recipes_show({'id': recipes_id})

    if 'user.id' not in session:
        flash ("Please log in to see this page")
        return redirect('/')

    if Recipe.validate_recipe(request.form):

        data = {
            'id': recipes_id,
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date_made': request.form['date_made'],
            'under_30_minutes': request.form['under_30_minutes'],
        }

        Recipe.recipes_update(data)
        return redirect('/dashboard')

    return redirect(f'/recipes/edit/{recipes_id}')
    # return redirect(f'/recipes/{recipes_id}')



@app.route('/recipes/delete/<int:recipe_id>')
def delete(recipe_id):

    recipes = Recipe.recipes_show({'id': recipe_id})

    if 'user.id' not in session:
        flash ("Please log in to see this page")
        return redirect('/')

    Recipe.recipe_delete({ 'id': recipe_id })

    return redirect('/dashboard')
