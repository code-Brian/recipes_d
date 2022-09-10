from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models import user
from flask import flash
import re

class Recipe:
    def __init__ (self,data:dict) -> object:
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooked_date = data['cooked_date']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @staticmethod
    def parse_recipe_data(data:dict) -> dict:
        '''This method will parse the data from the registration form and return it with a bcrypted password'''
        parsed_data = {
            'user_id': data.get('user_id'),
            'name': data.get('recipe_name'),
            'description': data.get('recipe_description'),
            'instructions': data.get('recipe_instructions'),
            'cooked_date': data.get('recipe_cooked_on'),
            'under_30': data.get('recipe_under_30'),
        }
    
        return parsed_data

    @staticmethod
    def parse_recipe_update(data:dict) -> dict:
        '''This method will parse the data from the registration form and return it with a bcrypted password'''
        parsed_data = {
            'user_id': data.get('user_id'),
            'id': data.get('id'),
            'name': data.get('recipe_name'),
            'description': data.get('recipe_description'),
            'instructions': data.get('recipe_instructions'),
            'cooked_date': data.get('recipe_cooked_on'),
            'under_30': data.get('recipe_under_30'),
        }
    
        return parsed_data

    @staticmethod
    def validate_recipe_data(data:dict) -> dict:
        is_valid = True

        if data['user_id'] == None:
            flash(u'Verify that you are signed in', 'recipe')
            is_valid = False

        if len(data['name']) < 5:
            flash(u"Name: Can you manage to type 5 characters?", 'recipe')
            is_valid = False

        if len(data['description']) < 10:
            flash(u"Description: You can at least do 10 characters, can't you?", 'recipe')
            is_valid = False

        if len(data['instructions']) < 10:
            flash(u"Instructions: You can do more than 10 characters, can't you?", 'recipe')
            is_valid = False

        if len(data['cooked_date']) < 1:
            flash(u'Date Cooked: You gotta tell me when you made this delicious monstrosity.', 'recipe')
            is_valid = False

        if data['under_30'] == None:
            flash(u'Prepped Under 30: At least lie and click one of the buttons!', 'recipe')
            is_valid = False

        return is_valid

    @classmethod
    def get_all(cls:object) -> list:
        query = '''
        SELECT * FROM recipes;
        '''
        results = connectToMySQL('recipes').query_db(query)

        all_recipes = []

        for recipes in results:
            all_recipes.append(cls(recipes))
        
        return all_recipes
    
    @classmethod
    def get_one(cls:object, data:dict) -> object:
        query = '''
        SELECT * FROM recipes WHERE id = %(id)s;
        '''

        result = connectToMySQL('recipes').query_db(query, data)

        if not result:
            return False

        return cls(result[0])

    @classmethod
    def add_recipe(cls, data:dict) -> None:
        query = '''
        INSERT INTO
        recipes ( name, description, instructions, cooked_date, under_30, user_id)
        VALUES(%(name)s, %(description)s, %(instructions)s, %(cooked_date)s, %(under_30)s, %(user_id)s);
        '''

        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def update(cls,data:dict) -> None:
        query = '''
        UPDATE recipes
        SET
        name = %(name)s,
        description = %(description)s,
        instructions = %(instructions)s,
        cooked_date = %(cooked_date)s,
        under_30 = %(under_30)s
        WHERE id = %(id)s;
        '''
        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def delete(cls, data:dict) -> None:
        query = '''
        DELETE FROM recipes WHERE id = %(id)s;
        '''
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_all_recipes_with_creator(cls) -> list:
        query = '''
        SELECT * FROM recipes
        JOIN users ON recipes.user_id = users.id;
        '''
        results = connectToMySQL('recipes').query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)

            user_info = {
                'id': row.get('id'),
                'first_name': row.get('first_name'),
                'last_name': row.get('last_name'),
                'email': row.get('email'),
                'password': row.get('password'),
                'created_at': row.get('created_at'),
                'updated_at': row.get('updated_at')
            }

            one_user = user.User(user_info)
            one_recipe.creator = one_user
            all_recipes.append(one_recipe)

        return all_recipes
    
    @classmethod
    def get_one_recipe_with_creator(cls, data:dict) -> object:
        query = '''
        SELECT * FROM recipes
        JOIN users ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s;
        '''
        results = connectToMySQL('recipes').query_db(query, data)

        user_info = {
            'id': results[0].get('users.id'),
            'first_name': results[0].get('first_name'),
            'last_name': results[0].get('last_name'),
            'email': results[0].get('email'),
            'password': results[0].get('password'),
            'created_at': results[0].get('users.created_at'),
            'updated_at': results[0].get('users.updated_at')
        }

        recipe_info = {
            'id': results[0].get('id'),
            'user_id': results[0].get('user_id'),
            'name': results[0].get('name'),
            'description': results[0].get('description'),
            'instructions': results[0].get('instructions'),
            'cooked_date': results[0].get('cooked_date'),
            'under_30': results[0].get('under_30'),
            'created_at': results[0].get('recipes.created_at'),
            'updated_at': results[0].get('recipes.updated_at')
        }

        print(user_info)
        print(recipe_info)

        one_user = user.User(user_info)
        one_recipe = Recipe(recipe_info)
        one_recipe.creator = one_user

        return one_recipe