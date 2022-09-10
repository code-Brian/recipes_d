from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash
from flask_bcrypt import Bcrypt
import re

BCRYPT = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')

class User:
    def __init__ (self, data:dict)-> None:
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_recipes = []

    # STATIC METHODS

    @staticmethod
    def validate_registration(user:dict) -> dict:
        is_valid = True

        if len(user['first_name']) < 3:
            flash(u'First name must be at least 3 characters', 'register')
            is_valid = False

        if len(user['last_name']) < 1:
            flash(u'Last name must be at least 1 character', 'register')
            is_valid = False

        if not EMAIL_REGEX.match(user['email']):
            flash(u'Email address is not valid', 'register')
            is_valid = False

        if User.get_user_email(user):
                flash(u'Email address is already in use', 'register')
                is_valid = False

        if not PASSWORD_REGEX.match(user['password']):
            flash(u'Password must include: length of 8 characters, one uppercase letter, one digit, and include special character.', 'register')
            is_valid = False

        if not user['password'] == user['confirm_password']:
            flash(u'Passwords entered do not match', 'register')
            is_valid = False

        return is_valid
    
    @staticmethod
    def parse_registration_data(data:dict) -> dict:
        '''This method will parse the data from the registration form and return it with a bcrypted password'''
        parsed_data = {
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'email': data.get('email'),
            'password': BCRYPT.generate_password_hash(data.get('password'))
        }

        return parsed_data

    # CLASS METHODS

    @classmethod
    def get_user_email(cls, data:dict) -> object:
        query = '''
        SELECT * FROM users WHERE email = %(email)s;
        '''
        result = connectToMySQL('recipes').query_db(query,data)
        if not result:
            return False
        
        user = cls(result[0])

        return user

    def check_password(cls, data)  -> object:
        query = '''
        SELECT %(email)s FROM users WHERE password = %(password)s;
        '''

        result = connectToMySQL('recipes').query_db(query, data)
        if not result:
            return False

        user = cls(result[0])

        return user

    @classmethod
    def save(cls, data:dict)  -> object:
        query='''
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        '''

        return connectToMySQL('recipes').query_db(query, data)
    
    @classmethod
    def get_user_by_id(cls, data:dict)  -> object:
        query='''
        SELECT * FROM users WHERE users.id = %(id)s;
        '''
        result = connectToMySQL('recipes').query_db(query, data)
        if not result:
            return False
        
        user = cls(result[0])

        return user
    
    def get_all(cls) -> list:
        query='''
        SELECT * FROM users;
        '''
        results = connectToMySQL('recipes').query_db(query)

        all_users = []

        for row in results:
            all_users.append(cls(row))
        
        return all_users