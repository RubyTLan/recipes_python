from flask_app import app
from flask import Flask, render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe

bcrypt=Bcrypt(app)


@app.route("/recipes/new")
def new_recipe_form():
    if 'user_id' not in session:
        return redirect("/")
    return render_template("new.html")

@app.route("/recipes/new/create", methods=['post'])
def create_recipe():
    if 'user_id' not in session:
        return redirect("/")
    if not Recipe.validator(request.form):
        return redirect("/recipes/new")
    data={
        **request.form,
        'user_id':session['user_id']
    }

    Recipe.create(data)
    return redirect("/dashboard")

@app.route("/recipes/<int:id>/view")
def view(id):
    if 'user_id' not in session:
        return redirect("/")
    data_recipe={
        'id':id
    }
    one_recipe=Recipe.get_one_by_id(data_recipe)
    data_user={
        'id':session['user_id']
    }
    logged_user=User.get_by_id(data_user)
    return render_template("view.html",one_recipe=one_recipe,logged_user=logged_user)

@app.route("/recipes/<int:id>/edit")
def edit_form(id):
    if 'user_id' not in session:
        return redirect("/")
    data={
        'id':id
    }
    one_recipe=Recipe.get_one_by_id(data)
    return render_template("edit.html",one_recipe=one_recipe)

@app.route("/recipes/<int:id>/update",methods=['post'])
def update_recipe(id):
    if 'user_id' not in session:
        return redirect("/")
    if not Recipe.validator(request.form):
        return redirect(f"/recipes/{id}/edit")
    update_data={
        **request.form,
        'id':id
    }
    Recipe.update(update_data)
    return redirect("/dashboard")


@app.route("/recipes/<int:id>/delete")
def delete_recipe(id):
    if 'user_id' not in session:
        return redirect("/")
    data={
        'id':id
    }
    Recipe.delete(data)
    return redirect("/dashboard")
