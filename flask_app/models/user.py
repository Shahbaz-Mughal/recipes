from flask_app import app
from flask import flash
import re
from flask_app.config.mysqlconnection import MySQLConnection

class User():

    def __init__(self, data): #data is row of dictionary 3:10 turning into objects
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated = data['updated_at']
        #confirm password only in controller

    # @classmethod
    # def registration_check_user_by_full_name(cls, data):
    #     query = 'SELECT first_name, last_name FROM users WHERE first_name = %(first_name)s AND %(last_name)s;' 

    #     results = MySQLConnection('users').query_db(query, data)

    #     users = []
    #     #want to turn all query objects into python objects
    #     for row in results:
    #         users.append(User(row))
        
    #     return users

    @classmethod
    def registration_check_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'

        results = MySQLConnection('recipes').query_db(query, data)
        
#w/ shawn
        # if len(results) == 0:
        #     return False
        # return cls(results[0])

        users = []
        
        for row in results:
            users.append(User(row))
        
        return users
        #want to turn all query objects into python objects

    @classmethod
    def registration_create_user(cls, data):
        
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'

        result = MySQLConnection('recipes').query_db(query, data)

        #result is the ID of what's created
        return result


    @staticmethod
    def validate_registration_form(data):
        is_valid = True

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(data['first_name']) < 2 or len(data['first_name']) > 255:
            is_valid = False
            flash('Please choose a first name to be at least 2 characters long')

        if len(data['last_name']) < 2 or len(data['last_name']) > 255:
            is_valid = False
            flash('Please choose a last name to be at least 2 characters long')

#if we were checking fo matching names
        # if len(User.registration_check_user_by_full_name(data)) > 0:
        #     is_valid = False
        #     flash('Please should an email address that is not already in use')


#another way, but not right dict format?
        # if len(User.registration_check_user_by_email({'email': data['email']}) > 0:
        #     is_valid = False
        #     flash('Please should an email address that is not already in use')

#adding this one on below later to make sure no match on email
        print(User.registration_check_user_by_email(data))
        if User.registration_check_user_by_email(data):
            is_valid = False
            flash('Please use an email address that is not already in use')

        if not email_regex.match(data['email']):
            is_valid = False
            flash('Please choose an email address in correct formatting')

        if len(data['email']) > 255: #why no min cuz our re does it
            is_valid = False
            flash('Please choose an email less than 255 characters')

        if len(data['password']) < 8:
            is_valid = False
            flash('Please choose a password to be at least 8 characters long')

        if not data['password'] == data['confirm_password']:
            is_valid = False
            flash('Please choose matching passwords')
#could do^ if not instead !=....but this was not working, i think b/c I forgot flash or is_valid

        return is_valid


#First Name - letters only, at least 2 characters and that it was submitted
# Last Name - letters only, at least 2 characters and that it was submitted
# Email - valid Email format, does not already exist in the database, and that it was submitted
# Password - at least 8 characters, and that it was submitted
# Password Confirmation - matches password