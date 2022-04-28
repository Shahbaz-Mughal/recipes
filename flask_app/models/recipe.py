from flask_app.config.mysqlconnection import connectToMySQL

# from flask_app import app
from flask import flash
# from flask_app.config.mysqlconnection import MySQLConnection

from flask_app.models.user import User


class Recipe():
    # be mindful matchy match - Denys
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30_minutes = data['under_30_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_id = data['users_id']
        self.user = None



    @classmethod
    def recipes_show_all(cls):

        query = "SELECT * FROM recipes JOIN users ON recipes.users_id = users.id";

        results = connectToMySQL('recipes').query_db(query)

        recipes = []

        for item in results:
            recipe = Recipe(item)
            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at']
            }
            user = User(user_data)
            recipe.user = user
            recipes.append(recipe)

        return recipes



    @classmethod
    def recipe_new(cls, data):

        query = "INSERT INTO recipes (name, description, instructions, date_made, under_30_minutes, users_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30_minutes)s, %(user_id)s);"

        result = connectToMySQL('recipes').query_db(query, data)

        #result is the ID of what's created 
        return result



    @classmethod
    def recipes_show(cls, data):

        query = "SELECT * FROM recipes JOIN users ON recipes.users_id = users.id WHERE recipes.id = %(id)s";

        results = connectToMySQL('recipes').query_db(query, data)
        # other way
        # results = connectToMySQL('recipes').query_db(query, data)[0]
        # and remove all [0] from data

        recipe = Recipe(results[0])
        # recipe = cls(results[0]) -- other way
        # could be result singular b/c just one row

        user_data = {
                'id': (results[0])['users.id'],
                'first_name': (results[0])['first_name'],
                'last_name': (results[0])['last_name'],
                'email': (results[0])['email'],
                'password': (results[0])['password'],
                'created_at': (results[0])['users.created_at'],
                'updated_at': (results[0])['users.updated_at']
            }

        recipe.user = User(user_data)

        return recipe



    @classmethod
    def recipes_update(cls, data):

        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under_30_minutes = %(under_30_minutes)s WHERE id = %(id)s;"

        connectToMySQL('recipes').query_db(query, data)



    @classmethod
    def recipe_delete(cls, data):

        query = "DELETE FROM recipes WHERE id = %(id)s;"

        connectToMySQL('recipes').query_db(query, data)






    @staticmethod
    def validate_recipe(data):
        is_valid = True
#do we need to type 3 times? 
        if len(data['name']) <= 3:
            flash('Recipe name should be at least 3 characters long')
            is_valid = False

        if len(data['description']) <= 3:
            flash('Description should be at least 3 characters long')
            is_valid = False

        if len(data['instructions']) <= 3:
            flash('Instructions should be at least 3 characters long')
            is_valid = False

        return is_valid
