from flask_app.config.mysqlconnection import connectToMySQL
import re	#regex thing
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

from flask import flash

class User:
    db_name = 'recipes'
    def __init__(self,data):
        self.id = data['id'],
        self.first_name = data['first_name'],
        self.last_name = data['last_name'],
        self.email = data['email'],
        self.password = data['password'],
        self.created_at = data['created_at'],
        self.udated_at = data['updated_at']

    @classmethod
    def createUser(cls,data):
        query = 'INSERT INTO users( first_name, last_name, email, password ) VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s );'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def getUserById(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]

    @classmethod
    def getUserByEmail(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        if result:
            return result[0]
        return False
    

    







    #method to validate user
    @staticmethod
    def validate_user(user):
        is_valid = True  #we assume this is true so if there is nothing wrong in the login-register no flash will appear
        if len(user['first_name']) < 1:
            flash("First name is required to register", 'first_name') #you cant register without a first name
            is_valid = False
        if len(user['last_name']) < 1:
            flash("Last name is required to register", 'last_name') #you cant register without a last name
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): #the email is not like this someone@something.something
            flash("Invalid email address!", 'emailRegister')
            is_valid = False
        if len(user['password']) < 8:  #you cant use a password with less than 8 characters
            flash("Password must be at least 8 characters long!", 'passwordRegister')
            is_valid = False
        if user['password']!=user['confirmPassword']: #passwords dont match
            flash("Passwords are not matching", 'passwordConfirm')
            is_valid = False
        return is_valid