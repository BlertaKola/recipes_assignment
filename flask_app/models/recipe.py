from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db_name = 'recipes'
    def __init__(self,data):
        self.id = data['id'],
        self.name = data['name'],
        self.description = data['description'],
        self.instruction = data['instruction'],
        self.dateMade = data['dateMade'],
        self.under30 = data['under30'],
        self.user_id = data['user_id'],
        self.created_at = data['created_at'],
        self.updated_at = data['updated_at']

    


    @classmethod
    def createRecipe(cls,data):
        query = 'INSERT INTO recipes ( name, description, instruction, dateMade, under30, user_id ) VALUES ( %(name)s, %(description)s, %(instruction)s, %(dateMade)s, %(under30)s, %(user_id)s ); '
        return connectToMySQL(cls.db_name).query_db(query,data)

    
    @classmethod                 #you get all the recipes that an user has created
    def getAllRecipesOfUser(cls,data):
        query = 'SELECT * FROM recipes LEFT JOIN users ON users.id = recipes.user_id  WHERE users.id = %(user_id)s ;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        recipes = []
        for row in result:
            recipes.append(row)
        return recipes
    
    @classmethod
    def allRecipes(cls):
        query = 'SELECT * FROM recipes'
        result = connectToMySQL(cls.db_name).query_db(query)
        if result:
            return result
        return False

    @classmethod
    def getRecipeById(cls,data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        result = connectToMySQL(cls.db_name).query_db(query,data)
        return result[0]


    @classmethod
    def updateRecipe(cls,data):
        query = 'UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, dateMade = %(dateMade)s, under30 = %(under30)s, user_id = %(user_id)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def deleteRecipe(cls,data):
        query = 'DELETE FROM recipes WHERE id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query,data)



    #validating the recipe
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True #we assume that every input of the user is correct
        if len(recipe['name']) < 8:
            flash("Name of the recipe must be at least 8 characters long", 'name')
            is_valid = False
        if len(recipe['description']) < 10:
            flash("The description must be at least 10 characters long", 'description')
            is_valid = False
        if len(recipe['instruction']) < 10:
            flash("The instructions must be at least 10 characters long", 'instruction')
            is_valid = False
        if recipe['dateMade'] == '':
            flash("You must include the date you made this recipe", 'dateMade')
            is_valid = False
        if 'under30' not in recipe: 
            flash("You must include the recipe time", 'under30')
            is_valid = False
        return is_valid
